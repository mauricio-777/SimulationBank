# Entidad acumuladora: almacena las métricas de la simulación en tiempo real
# Incluye: longitud de cola, tiempos de espera por prioridad, throughput,
#          utilización de ventanillas, clientes rechazados, inanición
from typing import List, Dict, Any
from .wait_time_record import WaitTimeRecord
from .throughput_record import ThroughputRecord

class SimulationMetrics:
    """
    parte-Jhonny:
    Clase central del módulo de estadísticas. 
    Se encarga de acumular datos durante la simulación interactuando 
    desde el motor de simulación. Al final usa 'calculate_statistics' 
    para procesar y resumir todos estos datos crudos en métricas finales.
    """
    def __init__(self, simulation_id: str):
        self.simulation_id = simulation_id
        self.wait_times: List[WaitTimeRecord] = []
        
        # Historial de longitudes de cola: lista de tuplas (timestamp, longitud)
        self.queue_length_history: List[tuple[float, int]] = []
        
        # Contadores básicos
        self.customers_served: int = 0
        self.customers_rejected: int = 0
        
        # Tiempo acumulado de todos los cajeros trabajando
        # Se actualizará cada vez que un cajero termina una atención
        self.total_teller_work_time: float = 0.0

    def record_queue_length(self, current_time: float, length: int) -> None:
        """
        parte-Jhonny:
        Guarda la longitud de la cola en el instante actual. 
        Este método se llamará en 'simulation.py' cada vez que alguien entra o sale.
        """
        self.queue_length_history.append((current_time, length))

    def record_wait_time(self, record: WaitTimeRecord) -> None:
        """
        parte-Jhonny:
        Registra los tiempos de un cliente que ha completado su atención.
        """
        self.wait_times.append(record)
        self.customers_served += 1

    def record_rejection(self) -> None:
        """
        parte-Jhonny:
        Aumenta el contador de abandonos/rechazos.
        """
        self.customers_rejected += 1

    def record_teller_work_time(self, time_worked: float) -> None:
        """
        parte-Jhonny:
        Acumula el tiempo que los cajeros pasaron ocupados.
        Sirve para luego deducir el porcentaje de utilización.
        """
        self.total_teller_work_time += time_worked

    def calculate_statistics(self, max_simulation_time: float, num_tellers: int) -> Dict[str, Any]:
        """
        parte-Jhonny:
        Procesa todos los datos crudos recopilados.
        Calcula: 
         1. Promedio y máximo de cola.
         2. Tiempo promedio de espera (Global y por prioridad).
         3. Utilización de ventanillas (% de tiempo ocupadas vs capacidad máxima).
         4. Throughput (Clientes servidos por unidad de tiempo).
         5. Porcentaje de abandono.
        Devuelve todo como un diccionario listo para serializar a JSON.
        """
        total_customers = self.customers_served + self.customers_rejected
        abandonment_rate = (self.customers_rejected / total_customers * 100) if total_customers > 0 else 0.0
        
        throughput = (self.customers_served / max_simulation_time) if max_simulation_time > 0 else 0.0
        
        max_queue = max([length for _, length in self.queue_length_history], default=0)
        # Aproximación del promedio de cola (debería ser promedio ponderado por tiempo, aquí usaremos la media simple)
        avg_queue = sum([length for _, length in self.queue_length_history]) / len(self.queue_length_history) if self.queue_length_history else 0.0

        avg_wait_time_global = sum([r.wait_time for r in self.wait_times]) / len(self.wait_times) if self.wait_times else 0.0

        # Tiempos promedio agrupados por prioridad
        wait_times_by_priority: Dict[int, List[float]] = {}
        for r in self.wait_times:
            if r.priority not in wait_times_by_priority:
                wait_times_by_priority[r.priority] = []
            wait_times_by_priority[r.priority].append(r.wait_time)
            
        avg_wait_by_priority = {
            f"Prioridad {p}": sum(times) / len(times) for p, times in wait_times_by_priority.items()
        }

        # Utilización de ventanillas (Tiempo trabajado / Tiempo total disponible entre todos los cajeros)
        total_teller_capacity = max_simulation_time * num_tellers
        teller_utilization = (self.total_teller_work_time / total_teller_capacity * 100) if total_teller_capacity > 0 else 0.0

        # Estructura del reporte
        return {
            "estadisticas_globales": {
                "max_cola": max_queue,
                "promedio_cola": round(avg_queue, 2),
                "tiempo_espera_promedio": round(avg_wait_time_global, 2),
                "utilizacion_ventanillas_porcentaje": round(teller_utilization, 2),
                "throughput_clientes_por_segundo": round(throughput, 4),
                "porcentaje_abandono": round(abandonment_rate, 2),
                "total_servidos": self.customers_served,
                "total_rechazados": self.customers_rejected
            },
            "tiempo_espera_por_prioridad": {k: round(v, 2) for k, v in avg_wait_by_priority.items()},
            "historial_cola": [{"minuto": round(t, 2), "longitud": l} for t, l in self.queue_length_history]
        }
