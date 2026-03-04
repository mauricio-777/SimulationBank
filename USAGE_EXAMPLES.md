# Guía de Uso - Cola de Prioridad Implementada

## Ejemplos de Uso Básicos

### 1. Crear una Cola de Prioridad

```python
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository
from src.queue.domain.queue_policy import QueuePolicy

# Obtener el repositorio singleton
repo = InMemoryQueueRepository.get_instance()

# Crear una política con capacidad máxima de 50 clientes
policy = QueuePolicy(
    max_queue_size=50,
    allow_rejections=True
)

# Crear la cola
queue = repo.create_queue("queue_1", policy)
print(f"Cola creada: {queue.get_queue_id()}")
```

### 2. Encolar un Cliente

```python
from src.customer.domain.customer import Customer
from src.customer.domain.priority import Priority
from src.queue.application.enqueue_customer import EnqueueCustomerUseCase

# Crear un cliente
customer = Customer(
    id="cust_001",
    arrival_time=100.5,
    service_time=5.0,
    priority=Priority.HIGH,  # Priority 1
    transaction_type="DEPOSIT"
)

# Usar el use case para encolar
enqueue_uc = EnqueueCustomerUseCase(queue_id="queue_1")
result = enqueue_uc.execute(customer)

print(result)
# {
#   'success': True,
#   'message': 'Customer cust_001 (priority 1) enqueued successfully',
#   'queue_size': 1,
#   'customer_id': 'cust_001'
# }
```

### 3. Desencolar el Cliente de Mayor Prioridad

```python
from src.queue.application.dequeue_customer import DequeueCustomerUseCase

# Crear cliente 1 (baja prioridad)
c1 = Customer(
    id="c1", arrival_time=100, service_time=5,
    priority=Priority.LOW,  # Priority 3
    transaction_type="DEPOSIT"
)

# Crear cliente 2 (alta prioridad)
c2 = Customer(
    id="c2", arrival_time=101, service_time=5,
    priority=Priority.HIGH,  # Priority 1
    transaction_type="WITHDRAWAL"
)

# Encolar ambos
enqueue_uc = EnqueueCustomerUseCase(queue_id="queue_1")
enqueue_uc.execute(c1)
enqueue_uc.execute(c2)

# Desencolar - extraerá PRIMERO a c2 (prioridad alta) aunque llegó después
dequeue_uc = DequeueCustomerUseCase(queue_id="queue_1")
result = dequeue_uc.execute()

print(result['customer'].id)  # Output: 'c2' (Mayor prioridad)
print(result['customer'].priority)  # Output: 1 (ALTA)
```

### 4. Consultar Cliente Siguiente sin Extracción

```python
from src.queue.application.peek_queue import PeekQueueUseCase

peek_uc = PeekQueueUseCase(queue_id="queue_1")
result = peek_uc.execute()

print(result)
# {
#   'success': True,
#   'customer': <Customer object>,
#   'message': 'Next customer: c1 (priority 3)',
#   'queue_size': 1
# }

# El cliente aún sigue en la cola - puede ser consultado nuevamente
result2 = peek_uc.execute()
print(result2['customer'].id)  # Still 'c1' - sin cambios
```

---

## Ejemplo Integrado con Simulación

### Integración Automática en DiscreteEventSimulation

```python
from src.simulation.domain.simulation import DiscreteEventSimulation
from src.simulation.domain.simulation_config import SimulationConfig

# Crear configuración con capacidad limitada
config = SimulationConfig(
    num_tellers=3,
    max_queue_capacity=100,  # Máximo 100 clientes pueden esperar
    arrival_config={
        "arrival_rate": 1.5,
        "arrival_dist": "exponential",
        "priority_weights": [0.1, 0.3, 0.6]
    },
    service_config={
        "service_mean": 5.0,
        "service_dist": "exponential",
        "service_stddev": 1.0
    },
    max_simulation_time=3600  # 1 hora
)

# La cola se crea automáticamente en el constructor
sim = DiscreteEventSimulation("sim_001", config)

# Inicializar y ejecutar
sim.initialize()
sim.run()

# Las métricas registran automáticamente:
# - Clientes encolados por prioridad
# - Clientes rechazados por capacidad
# - Tiempo de espera (respetando orden de prioridad)
```

---

## Demostración de Ordenamiento por Prioridad + FIFO

```python
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository
from src.queue.domain.queue_policy import QueuePolicy
from src.customer.domain.customer import Customer
from src.customer.domain.priority import Priority
from src.queue.application.enqueue_customer import EnqueueCustomerUseCase
from src.queue.application.dequeue_customer import DequeueCustomerUseCase

# Setup
repo = InMemoryQueueRepository.get_instance()
policy = QueuePolicy(max_queue_size=-1)  # Ilimitado
queue = repo.create_queue("test_queue", policy)

# Crear clientes con tiempos de llegada específicos
clients_data = [
    ("A", 150.0, Priority.MEDIUM),   # timestamp 150 - Media prioridad
    ("B", 100.0, Priority.HIGH),     # timestamp 100 - Alta prioridad
    ("C", 200.0, Priority.MEDIUM),   # timestamp 200 - Media prioridad
    ("D", 110.0, Priority.HIGH),     # timestamp 110 - Alta prioridad
    ("E", 160.0, Priority.LOW),      # timestamp 160 - Baja prioridad
]

enqueue_uc = EnqueueCustomerUseCase(queue_id="test_queue")

# Encolar en orden de llegada
for name, timestamp, priority in clients_data:
    customer = Customer(
        id=name,
        arrival_time=timestamp,
        service_time=5.0,
        priority=priority,
        transaction_type="TEST"
    )
    result = enqueue_uc.execute(customer)
    print(f"Enqueued {name} at {timestamp} with priority {priority}")

# Desencolar en orden respetado
dequeue_uc = DequeueCustomerUseCase(queue_id="test_queue")
order = []
while True:
    result = dequeue_uc.execute()
    if not result['success']:
        break
    customer = result['customer']
    order.append(customer.id)
    print(f"Dequeued: {customer.id} (priority={customer.priority})")

print(f"\nOrden de atención: {order}")
# Output: ['B', 'D', 'A', 'C', 'E']
# Explicación:
#   B, D - Priority 1 (Alta), ordered by timestamp: 100 < 110
#   A, C - Priority 2 (Media), ordered by timestamp: 150 < 200
#   E - Priority 3 (Baja), único con esta prioridad
```

---

## Manejo de Capacidad Limitada y Rechazos

```python
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository
from src.queue.domain.queue_policy import QueuePolicy
from src.customer.domain.customer import Customer
from src.customer.domain.priority import Priority
from src.queue.application.enqueue_customer import EnqueueCustomerUseCase

# Crear cola con capacidad máxima de 3 clientes
repo = InMemoryQueueRepository.get_instance()
policy = QueuePolicy(
    max_queue_size=3,
    allow_rejections=True
)
queue = repo.create_queue("limited_queue", policy)

enqueue_uc = EnqueueCustomerUseCase(queue_id="limited_queue")

# Intentar encolar 5 clientes
for i in range(5):
    customer = Customer(
        id=f"cust_{i}",
        arrival_time=float(i),
        service_time=5.0,
        priority=Priority.MEDIUM,
        transaction_type="TEST"
    )
    result = enqueue_uc.execute(customer)
    status = "✓ ENQUEUED" if result['success'] else "✗ REJECTED"
    print(f"{status} - {customer.id} (queue_size={result['queue_size']})")

# Output:
# ✓ ENQUEUED - cust_0 (queue_size=1)
# ✓ ENQUEUED - cust_1 (queue_size=2)
# ✓ ENQUEUED - cust_2 (queue_size=3)
# ✗ REJECTED - cust_3 (queue_size=3)
# ✗ REJECTED - cust_4 (queue_size=3)
```

---

## Consultas sobre el Estado de la Cola

```python
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository

repo = InMemoryQueueRepository.get_instance()
queue = repo.get_queue("queue_1")

# Información de la cola
print(f"Queue ID: {queue.get_queue_id()}")
print(f"Queue size: {queue.size()}")
print(f"Is empty: {queue.is_empty()}")

# Información de política
policy = queue.get_policy()
print(f"Max capacity: {policy.max_queue_size}")
print(f"Rejections enabled: {policy.allow_rejections}")
print(f"At capacity: {policy.is_at_capacity(queue.size())}")
```

---

## Limpiar y Resetear

```python
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository

repo = InMemoryQueueRepository.get_instance()

# Eliminar una cola específica
repo.delete_queue("queue_1")

# O limpiar todas las colas
repo.clear_all()

# Resetear la instancia singleton (para testing)
InMemoryQueueRepository.reset_instance()
```

---

## Errores Comunes y Soluciones

### Error 1: Queue Not Found
```python
# ❌ INCORRECTO
dequeue_uc = DequeueCustomerUseCase(queue_id="queue_999")
result = dequeue_uc.execute()  # Falla: queue no existe

# ✅ CORRECTO
repo = InMemoryQueueRepository.get_instance()
if repo.queue_exists("queue_999"):
    dequeue_uc = DequeueCustomerUseCase(queue_id="queue_999")
    result = dequeue_uc.execute()
```

### Error 2: Comparar Instancias de Customer Directamente
```python
# ❌ INCORRECTO
if customer1 == customer2:  # Compara por identidad, no por ID

# ✅ CORRECTO
if customer1.id == customer2.id:  # Compara por ID
```

### Error 3: Modificar Customer Encolado
```python
# ❌ INCORRECTO - No se debe cambiar customer encolado
customer.priority = Priority.LOW  # Rompe heap property!

# ✅ CORRECTO - Quitarlo y re-encolarlo si es necesario
from src.queue.application.dequeue_customer import DequeueCustomerUseCase
dequeue_uc = DequeueCustomerUseCase(queue_id="queue_1")
old_customer = dequeue_uc.execute()['customer']
old_customer.priority = Priority.LOW
enqueue_uc.execute(old_customer)
```

---

## Integración con Flask (main.py)

La simulación usa Flask para servir endpoints. La cola se integra automáticamente:

```python
# En main.py, el endpoint test_run ejecuta:
@app.route('/api/simulation/test_run', methods=['POST'])
def test_run():
    config = SimulationConfig(num_tellers=3)  # default: max_queue_capacity=100
    sim = DiscreteEventSimulation("test-sim-123", config)
    
    sim.initialize()  # Cola inicializada aquí
    sim.run()         # Cola usada durante simulación
    
    return jsonify({
        "message": "Simulation completed",
        "simulation_id": sim.simulation_id,
        "queue_statistics": {
            "max_size": 100,
            "final_size": 0,  # Desocupada al final
            "rejections_recorded": sim.metrics.rejection_count
        }
    })
```

