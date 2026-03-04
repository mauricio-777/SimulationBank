# Implementación: Cola de Prioridad con Montículo Binario

## Resumen de la Implementación

Se ha implementado correctamente una **estructura de cola con prioridad utilizando un montículo binario (binary heap)** que respeta:
1. ✅ Orden de prioridad (1=Alta, 2=Media, 3=Baja)
2. ✅ FIFO dentro del mismo nivel de prioridad (por timestamp de llegada)
3. ✅ Gestión de capacidad limitada con rechazo de clientes
4. ✅ Integración completa con el motor de simulación

---

## Archivos Implementados

### 1. **Clases Base (Shared Layer)**

#### `src/shared/domain/entity.py`
- **Responsable:** Clase base para todas las entidades del dominio
- **Funcionalidad:** Proporciona identificación única y comparación de igualdad
- **Comentarios:** parte-Entity (explicación de la identificación única)

#### `src/shared/domain/value_object.py`
- **Responsable:** Clase base para Value Objects
- **Funcionalidad:** Define contrato para objetos inmutables comparables por valor
- **Comentarios:** parte-ValueObject (comparación por valor, no identidad)

#### `src/shared/application/use_case.py`
- **Responsable:** Clase base abstracta para todos los Use Cases
- **Funcionalidad:** Define interfaz standard del patrón Use Case
- **Comentarios:** parte-UseCase (interfaz de lógica de negocio)

---

### 2. **Capa de Dominio (Domain Layer)**

#### `src/queue/domain/queue_node.py`
**Value Object inmutable representa un nodo en el montículo**
- `customer` - Cliente almacenado en el nodo
- `arrival_sequence` - Timestamp/contador para desempate FIFO
- **Operadores de comparación:** Implementa `__lt__`, `__le__`, `__gt__`, `__ge__` para ordenamiento automático
- **Comentarios:**
  - parte-QueueNode (contenedor inmutable para cálcula de prioridades)
  - parte-Ordering (comparación primaria por prioridad, secundaria por timestamp)

#### `src/queue/domain/queue_policy.py`
**Value Object que encapsula las reglas de comportamiento de la cola**
- `tie_breaker` - Estrategia de desempate (FIFO)
- `preemption` - Política de interrupción de servicio (NO_PREEMPTIVE)
- `max_queue_size` - Capacidad máxima (-1 = ilimitada)
- `allow_rejections` - Si se rechazan clientes que exceden capacidad
- **Métodos principales:**
  - `is_at_capacity()` - Verifica si la cola alcanzó capacidad máxima
  - `should_reject()` - Determina si un cliente debe ser rechazado
- **Comentarios:**
  - parte-TieBreaker (estrategias para determinar orden con igual prioridad)
  - parte-Preemption (define si servicio puede ser interrumpido)
  - parte-CapacityCheck (verifica límites de capacidad)
  - parte-RejectionLogic (lógica de aceptación/rechazo)

#### `src/queue/domain/priority_queue.py`
**Entidad principal: implementación del montículo binario**
- **Estructura:** Heap (lista Python) + contador de secuencia
- **Algoritmos de complejidad O(log n):**
  - `enqueue()` - Inserción con heapify-up
  - `dequeue()` - Extracción con heapify-down
  - `peek()` - Consulta sin extracción
- **Métodos auxiliares:**
  - `_heapify_up(index)` - Restaura propiedad heap hacia arriba
  - `_heapify_down(index)` - Restaura propiedad heap hacia abajo
- **Comentarios:**
  - parte-PriorityQueue (entidad con montículo binario)
  - parte-Enqueue (algoritmo de inserción con verificación de capacidad)
  - parte-Dequeue (algoritmo de extracción del máximo)
  - parte-Peek (consulta sin destrucción)
  - parte-HeapifyUp (restauración hacia arriba)
  - parte-HeapifyDown (restauración hacia abajo)

---

### 3. **Capa de Infraestructura (Infrastructure Layer)**

#### `src/queue/infrastructure/binary_heap_queue.py`
**Adaptador concreto de la cola usando heap binario**
- Proporciona interfaz user-friendly a PriorityQueue
- Implementa patrón Adapter
- Métodos públicos: enqueue, dequeue, peek, is_empty, size
- **Comentarios:**
  - parte-BinaryHeapAdapter (interfaz de usuario al dominio)
  - parte-EnqueueAdapter (wrapper a enqueue del dominio)
  - parte-DequeueAdapter (wrapper a dequeue del dominio)
  - parte-PeekAdapter (wrapper a peek del dominio)

#### `src/queue/infrastructure/in_memory_queue_repository.py`
**Repositorio Singleton que almacena instancias de colas en memoria**
- Patrón Singleton para instancia única durante ejecución
- Almacena múltiples colas por ID
- Métodos: create_queue, get_queue, delete_queue, queue_exists, all_queues, clear_all
- **Comentarios:**
  - parte-Repository (patrón Singleton para almacenamiento)
  - parte-Singleton (garant ía de instancia única)
  - parte-Create (creación de nuevas colas)
  - parte-Retrieve (obtención de colas existentes)
  - parte-Delete (eliminación de colas)

---

### 4. **Capa de Aplicación (Application Layer)**

#### `src/queue/application/enqueue_customer.py`
**Use Case: encolar un cliente en la cola de prioridad**
- Valida capacidad según política
- Respeta orden de prioridad + FIFO
- Retorna diccionario con estado de operación
- **Comentarios:**
  - parte-EnqueueUseCase (orquestación de inserción)
  - parte-Init (inicialización con ID de cola)
  - parte-Execute (operación principal)

#### `src/queue/application/dequeue_customer.py`
**Use Case: extraer el cliente de mayor prioridad**
- Extrae cliente con máxima priodidad
- Respeta FIFO dentro del nivel
- Retorna cliente o None si está vacía
- **Comentarios:**
  - parte-DequeueUseCase (orquestación de extracción)
  - parte-Execute (operación de dequeue)

#### `src/queue/application/peek_queue.py`
**Use Case: consultar el próximo cliente sin extraer**
- Lookahead sin modificar estado
- Útil para operaciones de ventanilla
- **Comentarios:**
  - parte-PeekUseCase (orquestación de consulta)
  - parte-Execute (operación de peek)

---

## Integración en la Simulación

### Cambios en `src/simulation/domain/simulation.py`

#### Importaciones Agregadas
```python
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository
from src.queue.domain.queue_policy import QueuePolicy
from src.queue.application.dequeue_customer import DequeueCustomerUseCase
```

#### Constructor Actualizado
- **parte-QueueSetup:** Inicializa repositorio, crea política de cola y use case
- Integra `max_queue_capacity` de SimulationConfig
- Crea identificador único de cola por simulación

#### Método `initialize()`
- **parte-QueueReset:** Limpia y recrea cola para simulación fresca
- Garantiza estado limpio en cada inicialización

#### Método `handle_arrival()`
- **parte-EnqueueOperation:** Usa cola de prioridad en lugar de lista simple
- Respeta orden de prioridad automáticamente
- Registra rechazos si cola alcanza capacidad
- **parte-Jhonny:** Registra longitud de cola en métricas

#### Método `_assign_free_teller()`
- **parte-AssignLogic:** Itera ventanillas para buscar disponibles
- **parte-DequeuePriority:** Extrae cliente de mayor prioridad de la cola
- Respeta automáticamente FIFO dentro de nivel

#### Método `run()`
- **parte-FinalMetrics:** Cuenta clientes restantes en cola como rechazados
- Registra longitud final en métricas

---

## Características Implementadas

### ✅ 2.1 Implementar cola de prioridad (montículo)
**Estado:** COMPLETO
- Estructura de heap binario O(log n) para inserción y extracción
- Almacenamiento eficiente en lista de Python
- Comparadores automáticos en QueueNode

### ✅ 2.2 Integrar cola de prioridad en simulación
**Estado:** COMPLETO
- Reemplaza lista simple por cola de prioridad
- handle_arrival() usa enqueue()
- _assign_free_teller() usa dequeue()
- Métricas actualizadas para reflejar cambios de cola

### ✅ 2.3 Implementar política de desempate
**Estado:** COMPLETO
- QueueNode compara primero por priority (1 < 2 < 3)
- Luego por arrival_sequence para FIFO
- arrival_sequence es counter incremental garantizando orden

### ✅ 2.4 Manejo de capacidad limitada
**Estado:** COMPLETO
- QueuePolicy.max_queue_size configurable (-1 = ilimitado)
- QueuePolicy.allow_rejections habilita/deshabilita rechazos
- Clientes rechazados registrados en metrics
- SimulationConfig.max_queue_capacity = 100 (predeterminado)

---

## Estructura de Código en Inglés

Toda el código está comentado en **inglés estándar de desarrollo** como es la práctica industrial, con las anotaciones clarificativas adicionales en español siguiendo el patrón "parte-Nombre".

### Ejemplo de estilo de comentarios:
```python
# parte-Enqueue: Adds a customer to the queue respecting priority and capacity
# Uses heapify-up algorithm to maintain heap property
```

---

## Validación y Pruebas

✅ **Todos los archivos compilaron sin errores**
✅ **Imports funcionan correctamente**
✅ **Integración con simulación verificada**
✅ **Instanciación de cola en simulación correcta**
✅ **Política de cola se crea con parámetros correctos (max_queue_capacity=100)**

---

## Notas Importantes

1. **Montículo binario:** Implementación manual (no usa heapq) para purposes académicos
2. **FIFO garantizado:** arrival_sequence es contador monotónicamente incremental
3. **Sin preemption:** Clientes en servicio no pueden ser interrumpidos
4. **Capacidad configurable:** Configurable vía SimulationConfig.max_queue_capacity
5. **Métricas integradas:** Cambios de cola reflejados en metrics del sistema

---

## Archivos No Modificados (Mantienen Coherencia)

- `src/customer/domain/customer.py` - Sin cambios requeridos
- `src/teller/domain/teller.py` - Sin cambios requeridos
- `src/metrics/domain/simulation_metrics.py` - Sin cambios requeridos
- `main.py` - Sin cambios, Flask funcionando sin modificaciones
- `requirements.txt` - Sin nuevas dependencias externas

