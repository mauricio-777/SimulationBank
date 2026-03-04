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
from src.metrics.domain.simulation_metrics import SimulationMetrics
from src.metrics.domain.wait_time_record import WaitTimeRecord
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository
from src.queue.domain.queue_policy import QueuePolicy
from src.queue.application.dequeue_customer import DequeueCustomerUseCase

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
        
        # parte-Jhonny: Inicializamos el recolector de métricas para esta simulación
        self.metrics = SimulationMetrics(simulation_id=self.simulation_id)
        
        # Estado del sistema en un instante de tiempo
        self.tellers: Dict[str, Teller] = {} # Diccionario que almacena todas las ventanillas disponibles por su ID
        
        # parte-QueueSetup: Initialize priority queue with optional capacity constraints
        # The queue uses binary heap for O(log n) insertion/extraction operations
        # Respects FIFO ordering within same priority level using arrival timestamp
        self.queue_repo = InMemoryQueueRepository.get_instance()
        self.queue_id = f"queue_{simulation_id}"
        # Create queue with optional max capacity from config, defaults to unlimited if not specified
        max_queue_capacity = getattr(config, 'max_queue_capacity', -1)
        self.queue_policy = QueuePolicy(
            max_queue_size=max_queue_capacity if max_queue_capacity > 0 else -1,
            allow_rejections=(max_queue_capacity > 0)  # Enable rejections only if capacity is limited
        )
        self.dequeue_use_case = DequeueCustomerUseCase(queue_id=self.queue_id)
        
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
        self.event_queue.clear()
        
        # parte-QueueReset: Clear and recreate the priority queue for fresh simulation
        # Delete old queue if it existed and create new one with policy constraints
        self.queue_repo.delete_queue(self.queue_id)
        self.queue_repo.create_queue(self.queue_id, self.queue_policy)
        self.dequeue_use_case = DequeueCustomerUseCase(queue_id=self.queue_id)
        
        # parte-Jhonny: Reiniciamos las métricas al iniciar para no mezclar ejecuciones
        self.metrics = SimulationMetrics(simulation_id=self.simulation_id)
        
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
        
        # parte-FinalMetrics: Get remaining customers in priority queue and record as rejected
        queue = self.queue_repo.get_queue(self.queue_id)
        if queue:
            # Count remaining customers in the priority queue (binary heap)
            remaining_count = queue.size()
            for _ in range(remaining_count):
                self.metrics.record_rejection()
            # parte-Jhonny: Register final queue length as cleared
            self.metrics.record_queue_length(self.clock, 0)

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
        2. Lo ingresa a la cola de espera con prioridad, respetando FIFO dentro del mismo nivel.
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
        
        # parte-EnqueueOperation: Use priority queue to enqueue customer
        # Queue respects: 1) priority level (1=high, 2=medium, 3=low)
        #                 2) FIFO order within same priority using arrival_time
        queue = self.queue_repo.get_queue(self.queue_id)
        if queue:
            enqueued = queue.enqueue(customer)
            if enqueued:
                # Customer successfully enqueued
                # parte-Jhonny: Update queue length metric after successful enqueue
                self.metrics.record_queue_length(self.clock, queue.size())
            else:
                # Customer rejected if queue is at capacity
                self.metrics.record_rejection()
        else:
            # Queue not found - should not happen in normal operation
            self.metrics.record_rejection()
        
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
            
            # parte-Jhonny: Hook - Calculamos tiempo de espera y registramos
            wait_time = self.clock - customer.arrival_time
            record = WaitTimeRecord(
                customer_id=customer.id,
                priority=customer.priority,
                wait_time=wait_time,
                service_time=customer.service_time,
                total_time=wait_time + customer.service_time
            )
            self.metrics.record_wait_time(record)
            self.metrics.record_teller_work_time(customer.service_time) # Sabemos que lo va a atender este rato
            
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
        En caso de encontrar una y haber gente esperando, extrae al cliente de mayor prioridad 
        de la cola y programa el evento SERVICE_START para esa ventanilla en el reloj actual.
        """
        # parte-AssignLogic: Iterate through tellers to find the first available one
        for t_id, teller in self.tellers.items():
            if teller.status == "IDLE" or getattr(teller.status, "value", None) == "IDLE":
                # Found an idle teller, try to get next customer from priority queue
                queue = self.queue_repo.get_queue(self.queue_id)
                if queue and not queue.is_empty():
                    # parte-DequeuePriority: Extract highest-priority customer respecting FIFO within level
                    next_customer = queue.dequeue()
                    
                    # parte-Jhonny: Update queue length metric after dequeue operation
                    self.metrics.record_queue_length(self.clock, queue.size())
                    
                    # Programar inicio INMEDIATO de servicio
                    self.schedule_event(SimulationEvent(self.clock, EventType.SERVICE_START, customer=next_customer, teller_id=t_id))
                    return  # Assign only one customer per iteration
