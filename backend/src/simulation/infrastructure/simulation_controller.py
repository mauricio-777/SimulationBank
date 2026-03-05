# parte-Leandro: Controlador HTTP para los endpoints de simulación
# Este controlador orquesta los use cases de simulación invocados por el Blueprint.
# Se encarga de:
# 1. Iniciar nuevas simulaciones con parámetros personalizados
# 2. Obtener el estado actual de una simulación
# 3. Pausar y reanudar simulaciones
# 4. Detener simulaciones y guardarlas

import uuid
import threading
from src.simulation.domain.simulation import DiscreteEventSimulation
from src.simulation.domain.simulation_config import SimulationConfig
from src.simulation.infrastructure.in_memory_simulation_repository import InMemorySimulationRepository


class SimulationController:
    """
    parte-Leandro: Controlador que gestiona todas las operaciones relacionadas con simulaciones.
    Actúa como intermediario entre las peticiones HTTP (Flask Blueprint) y la lógica de negocio
    de simulación (casos de uso y servicios de dominio).
    
    Responsabilidades:
    - Crear nuevas simulaciones con configuración personalizada
    - Ejecutar simulaciones en hilos separados para no bloquear la API
    - Obtener estado actual de simulaciones en ejecución
    - Recuperar resultados finales de simulaciones completadas
    """
    
    def __init__(self):
        # parte-Leandro: Instancia del repositorio Singleton que mantiene todas las simulaciones en memoria
        self.repo = InMemorySimulationRepository.get_instance()
        
        # parte-Leandro: Diccionario que almacena el estado de cada simulación en ejecución
        # Estructura: {simulation_id: {"status": "running|paused|stopped", "progress": 0-100}}
        self.simulation_states = {}
        
        # parte-Leandro: Diccionario para almacenar los hilos de ejecución de cada simulación
        # Permite controlar y monitorear las simulaciones que se ejecutan en background
        self.simulation_threads = {}
    
    def start_simulation(self, config_dict: dict) -> dict:
        """
        parte-Leandro: Inicia una nueva simulación con la configuración proporcionada.
        
        Parámetros:
        - config_dict: Diccionario con los parámetros de configuración:
            {
                "num_tellers": int (número de ventanillas),
                "arrival_rate": float (λ - tasa de llegadas),
                "service_mean": float (μ - tiempo medio de servicio),
                "max_time": float (horizonte temporal en segundos),
                "max_queue_capacity": int (capacidad máxima de cola),
                "priority_weights": list (pesos de prioridades),
                "service_dist": str (distribución de servicio)
            }
        
        Retorna:
        - Diccionario con simulation_id y estado inicial
        """
        try:
            # parte-Leandro: Generar ID único para la simulación
            simulation_id = f"sim-{uuid.uuid4().hex[:8]}"
            
            # parte-Leandro: Construir objeto SimulationConfig a partir del diccionario recibido
            config = SimulationConfig(
                num_tellers=config_dict.get("num_tellers", 3),
                max_simulation_time=config_dict.get("max_time", 8 * 3600),
                max_queue_capacity=config_dict.get("max_queue_capacity", 100),
                arrival_config={
                    "arrival_rate": config_dict.get("arrival_rate", 1.0),
                    "arrival_dist": config_dict.get("arrival_dist", "exponential"),
                    "priority_weights": config_dict.get("priority_weights", [0.1, 0.3, 0.6])
                },
                service_config={
                    "service_mean": config_dict.get("service_mean", 5.0),
                    "service_dist": config_dict.get("service_dist", "exponential"),
                    "service_stddev": config_dict.get("service_stddev", 1.0)
                }
            )
            
            # parte-Leandro: Crear instancia de simulación con la configuración
            simulation = DiscreteEventSimulation(simulation_id, config)
            
            # parte-Leandro: Guardar la simulación en el repositorio
            self.repo.save(simulation)
            
            # parte-Leandro: Inicializar estado de la simulación
            self.simulation_states[simulation_id] = {
                "status": "initializing",
                "progress": 0,
                "start_time": None,
                "config": config_dict
            }
            
            # parte-Leandro: Crear e iniciar un hilo de ejecución para la simulación
            # Esto permite que el cliente reciba respuesta inmediata y la simulación se ejecute en background
            thread = threading.Thread(
                target=self._run_simulation_in_background,
                args=(simulation_id,),
                daemon=True
            )
            self.simulation_threads[simulation_id] = thread
            thread.start()
            
            return {
                "success": True,
                "simulation_id": simulation_id,
                "message": f"Simulation {simulation_id} started successfully",
                "status": "initializing"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error starting simulation"
            }
    
    def _run_simulation_in_background(self, simulation_id: str):
        """
        parte-Leandro: Ejecuta la simulación en un hilo separado.
        
        Este método:
        1. Inicializa los componentes internos de la simulación
        2. Ejecuta el motor de eventos discretos
        3. Actualiza el estado de progreso
        4. Captura cualquier error que ocurra durante la ejecución
        """
        try:
            # parte-Leandro: Obtener la simulación del repositorio
            simulation = self.repo.get(simulation_id)
            
            # parte-Leandro: Actualizar estado a "running"
            self.simulation_states[simulation_id]["status"] = "running"
            
            # parte-Leandro: Inicializar la simulación (configura eventos iniciales, generadores, etc.)
            simulation.initialize()
            
            # parte-Leandro: Ejecutar la simulación hasta su conclusión
            # El método run() avanza el reloj de la simulación hasta max_simulation_time
            simulation.run()
            
            # parte-Leandro: Al terminar, marcar como "completed"
            self.simulation_states[simulation_id]["status"] = "completed"
            self.simulation_states[simulation_id]["progress"] = 100
            
        except Exception as e:
            # parte-Leandro: Si ocurre un error, registrarlo en el estado
            self.simulation_states[simulation_id]["status"] = "error"
            self.simulation_states[simulation_id]["error"] = str(e)
    
    def get_simulation_state(self, simulation_id: str) -> dict:
        """
        parte-Leandro: Obtiene el estado actual de una simulación.
        
        Retorna información sobre:
        - Estado actual (initializing, running, paused, completed, error)
        - Progreso (porcentaje aproximado)
        - Configuración usada
        - Errores si los hay
        """
        if simulation_id not in self.simulation_states:
            return {
                "error": f"Simulation {simulation_id} not found",
                "success": False
            }
        
        state = self.simulation_states[simulation_id]
        
        # parte-Leandro: Si la simulación se completó, calcular progreso en base a tiempo
        if state["status"] == "running":
            simulation = self.repo.get(simulation_id)
            if simulation:
                # Calcular progreso como porcentaje del tiempo total
                progress = min(100, (simulation.clock / simulation.config.max_simulation_time) * 100)
                state["progress"] = round(progress, 2)
        
        return {
            "success": True,
            "simulation_id": simulation_id,
            **state
        }
    
    def get_simulation_results(self, simulation_id: str) -> dict:
        """
        parte-Leandro: Obtiene los resultados completos de una simulación finalizada.
        
        Si la simulación aún está en ejecución, retorna un error.
        Si está completa, retorna todas las métricas calculadas.
        """
        # parte-Leandro: Verificar que la simulación existe
        simulation = self.repo.get(simulation_id)
        if not simulation:
            return {
                "error": f"Simulation {simulation_id} not found",
                "success": False
            }
        
        # parte-Leandro: Verificar que está completa
        state = self.simulation_states.get(simulation_id, {})
        if state.get("status") != "completed":
            return {
                "error": f"Simulation {simulation_id} is still {state.get('status', 'unknown')}",
                "success": False
            }
        
        # parte-Leandro: Retornar las métricas calculadas por la simulación
        try:
            metrics = simulation.metrics.calculate_statistics(
                max_simulation_time=simulation.clock,
                num_tellers=simulation.config.num_tellers
            )
            return {
                "success": True,
                "simulation_id": simulation_id,
                "metrics": metrics,
                "total_time": simulation.clock
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "simulation_id": simulation_id
            }
