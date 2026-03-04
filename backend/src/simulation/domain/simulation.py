import heapq
import uuid
from typing import List, Dict
from dataclasses import dataclass, field

from .simulation_config import SimulationConfig
from .simulation_status import SimulationStatus
from .simulation_event import SimulationEvent, EventType
from src.teller.domain.teller import Teller
from src.customer.domain.customer import Customer
from src.customer.infrastructure.poisson_customer_generator import ConfigurableGenerator

# parte-Mauricio
class DiscreteEventSimulation:
    """
    Entidad raíz: representa una instancia completa de la simulación del banco.
    Actúa como el motor central que coordina el tiempo, procesa la cola de eventos y asigna los recursos.
    """
    def __init__(self, simulation_id: str, config: SimulationConfig):
        self.simulation_id = simulation_id # Identificador único de esta ejecución
        self.config = config # Opciones de configuración provistas por el usuario
        self.status = SimulationStatus.IDLE # Estado inicial inactivo
        self.clock: float = 0.0 # Reloj global de simulación en segundos simulados
        
        # Estado del sistema en un instante de tiempo
        self.tellers: Dict[str, Teller] = {} # Diccionario que almacena todas las ventanillas disponibles por su ID
        self.waiting_queue: List[Customer] = [] # Cola de clientes esperando ser atendidos, ordenados por prioridad
        
        # Cola de prioridad que mantiene la línea temporal cronológica de futuros eventos
        self.event_queue: List[SimulationEvent] = []
        
        # Componente que genera tiempos de llegada y atributos de clientes
        _gen_config = {**self.config.arrival_config, **self.config.service_config}
        self.generator = ConfigurableGenerator(_gen_config)

    def initialize(self) -> None:
        """
        Prepara el sistema antes de iniciar.
        Inicializa las ventanillas, vacía las colas y programa mecánicamente el primer cliente en llegar.
        """
        self.status = SimulationStatus.IDLE
        self.clock = 0.0
        self.waiting_queue.clear()
        self.event_queue.clear()
        
        # Inicializar ventanillas
        for i in range(self.config.num_tellers):
            t_id = f"T-{i+1}"
            self.tellers[t_id] = Teller(id=t_id)
            
        # Programar llegada 1
        first_arrival_time = self.generator.get_next_arrival_interval()
        if first_arrival_time <= self.config.max_simulation_time:
            self.schedule_event(SimulationEvent(first_arrival_time, EventType.ARRIVAL, customer=None))

    def run(self) -> None:
        """
        Bucle principal del motor de simulación.
        Extrae cronológicamente el próximo evento, adelanta el reloj y ejecuta su lógica 
        hasta agotar la cola de eventos o superar el tiempo máximo.
        """
        self.status = SimulationStatus.RUNNING
        while self.event_queue and self.status == SimulationStatus.RUNNING:
            current_event = heapq.heappop(self.event_queue)
            
            # Verificar finalización
            if current_event.time > self.config.max_simulation_time:
                break
                
            # Avanzar reloj
            self.clock = current_event.time
            self.process_next_event(current_event)
            
        self.status = SimulationStatus.FINISHED

    def schedule_event(self, event: SimulationEvent) -> None:
        """
        Añade un nuevo evento futuro a la línea de tiempo.
        Utiliza heappush para mantener la consistencia de eventos ordenados por tiempo.
        """
        heapq.heappush(self.event_queue, event)

    def process_next_event(self, event: SimulationEvent) -> None:
        """
        Conmutador (switch) central que redirige el flujo de procesamiento dependiendo
        de si el evento es una llegada, un inicio de atención, o un fin de servicio.
        """
        if event.event_type == EventType.ARRIVAL:
            self.handle_arrival()
        elif event.event_type == EventType.SERVICE_START:
            self.handle_service_start(event.teller_id, event.customer)
        elif event.event_type == EventType.SERVICE_END:
            self.handle_service_end(event.teller_id)

    def handle_arrival(self) -> None:
        """
        Maneja el evento en el cual un cliente cruza la puerta del banco.
        1. Crea su instancia.
        2. Lo ingresa a la cola de espera, respetando las prioridades.
        3. Programa aleatoriamente la llegada del *siguiente* cliente.
        4. Intenta buscar de inmediato una ventanilla libre que pueda atenderlo.
        """
        # Configurar y crear cliente
        prio, txn = self.generator.get_next_customer_attributes()
        service_time = max(0.1, self.generator.get_service_time())
        
        customer = Customer(
            id=str(uuid.uuid4())[:8],
            arrival_time=self.clock,
            service_time=service_time,
            priority=prio,
            transaction_type=txn
        )
        
        # Encolar cliente
        self.waiting_queue.append(customer)
        # Ordenar por prioridad ascendente (1 es mayor prioridad) si queremos que se respete inmediatamente
        self.waiting_queue.sort(key=lambda c: (c.priority, c.arrival_time))
        
        # Programar SIGUIENTE llegada
        next_interval = self.generator.get_next_arrival_interval()
        next_time = self.clock + next_interval
        if next_time <= self.config.max_simulation_time:
            self.schedule_event(SimulationEvent(next_time, EventType.ARRIVAL))
            
        # Intentar asignar cajero libre
        self._assign_free_teller()

    def handle_service_start(self, teller_id: str, customer: Customer) -> None:
        """
        Inicia oficialmente el tiempo de ventanilla entre un cajero y un cliente particular.
        Programa a futuro el evento que indicará el final del trámite.
        """
        teller = self.tellers.get(teller_id)
        if teller:
            teller.start_service(customer, self.clock)
            # Programar fin de servicio
            end_time = self.clock + customer.service_time
            self.schedule_event(SimulationEvent(end_time, EventType.SERVICE_END, teller_id=teller_id))

    def handle_service_end(self, teller_id: str) -> None:
        """
        Registra el momento en el que el cliente actual se retira de la ventanilla,
        completando su transacción. A continuación, habilita inmediatamente al cajero 
        para atender al siguiente en la cola (si hubiera).
        """
        teller = self.tellers.get(teller_id)
        if teller:
            # cliente_atendido = teller.end_service()
            teller.end_service()
            # el teller ahora está IDLE, intentar asignar a alguien de la cola
            self._assign_free_teller()

    def _assign_free_teller(self) -> None:
        """
        Busca secuencialmente si existe una ventanilla inactiva (IDLE). 
        En caso de encontrar una y haber gente esperando, extrae al primer cliente 
        de la fila y programa el evento SERVICE_START para esa ventanilla en el reloj actual.
        """
        if not self.waiting_queue:
            return
            
        for t_id, teller in self.tellers.items():
            if teller.status == "IDLE" or getattr(teller.status, "value", None) == "IDLE":
                next_customer = self.waiting_queue.pop(0)
                # Programar inicio INMEDIATO
                self.schedule_event(SimulationEvent(self.clock, EventType.SERVICE_START, customer=next_customer, teller_id=t_id))
                return # Sólo asignamos uno a la vez iterativamente
