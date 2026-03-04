# Referencia de Comentarios "parte-" en la Implementación

Esta es una referencia completa de todos los comentarios explicativos especiales `parte-Nombre` utilizados en la implementación de la cola de prioridad.

## Raíz (Shared Domain)

### Entity
- **parte-Entity** - Explicación de cómo las entidades proporcionan identificación única y comparación de igualdad

### ValueObject
- **parte-ValueObject** - Concepto de Value Objects como objetos inmutables comparables por valor, no por identidad

### UseCase
- **parte-UseCase** - Patrón Use Case: interfaz estándar para operaciones de negocio en capa de aplicación

---

## Capa de Dominio (Queue Domain)

### QueueNode - Value Object del Montículo

**Conceptos principales:**

- **parte-QueueNode** - Propósito: contenedor inmutable para cálculo automático de prioridades en el heap
  
- **parte-Ordering** - Explicación detallada del algoritmo de comparación:
  - Comparación primaria: `priority` (1 < 2 < 3) - menor número = mayor prioridad
  - Comparación secundaria: `arrival_sequence` - orden de llegada para FIFO dentro del mismo nivel

**Detalles de implementación:**

- Operadores `__lt__`, `__le__`, `__gt__`, `__ge__` - Permiten comparación automática para uso en heap

---

### QueuePolicy - Value Object de Política

**Conceptos principales:**

- **parte-TieBreaker** - Estrategias de desempate cuando clientes tienen igual prioridad
  - FIFO (First In, First Out) - Selected strategy

- **parte-Preemption** - Define si se puede interrumpir servicio en curso
  - NON_PREEMPTIVE - Vez que comienza, completa sin interrupciones

**Métodos de validación:**

- **parte-CapacityCheck** - Verificación de límite de capacidad
  - `is_at_capacity()` - Determina si se alcanzó máximo

- **parte-RejectionLogic** - Lógica de aceptación/rechazo de clientes
  - `should_reject()` - Decide si nuevo cliente es rechazado

---

### PriorityQueue - Entidad Principal

**Estructura y almacenamiento:**

- **parte-PriorityQueue** - Entidad raíz que implementa montículo binario con operaciones O(log n)

**Operaciones principales:**

- **parte-Enqueue** - Algoritmo de inserción
  - Verifica capacidad con policy
  - Crea QueueNode con sequence_counter incremental
  - Llama _heapify_up para mantener propiedad del heap

- **parte-Dequeue** - Algoritmo de extracción
  - Extrae root (máxima prioridad)
  - Mueve último elemento a root
  - Llama _heapify_down para restaurar heap property

- **parte-Peek** - Operación de consulta sin destrucción
  - Retorna customer en root sin modificar cola

- **parte-Empty** - Verificación de estado vacío

- **parte-Size** - Retorna cantidad de elementos

**Algoritmos de rebalanciamiento:**

- **parte-HeapifyUp** - Restauración hacia arriba (inserción)
  - Compara con padre
  - Intercambia si actual tienen mayor prioridad que padre
  - Continúa hasta raíz

- **parte-HeapifyDown** - Restauración hacia abajo (extracción)
  - Compara con hijos (izq y der)
  - Intercambia con hijo de menor valor (mayor prioridad)
  - Continúa hasta hoja

---

## Capa de Infraestructura (Infrastructure)

### BinaryHeapQueueAdapter

**Patrón Adapter:**

- **parte-BinaryHeapAdapter** - Adaptador concreto proporciona interfaz user-friendly a PriorityQueue

**Métodos wrapper:**

- **parte-Init** - Inicialización con política opcional

- **parte-EnqueueAdapter** - Wrapper a enqueue() del dominio

- **parte-DequeueAdapter** - Wrapper a dequeue() del dominio

- **parte-PeekAdapter** - Wrapper a peek() del dominio

- **parte-IsEmpty** - Consulta de estado

- **parte-Size** - Retorna cantidad

- **parte-GetId** - Identificador de la cola

- **parte-GetPolicy** - Retorna configuración de política

---

### InMemoryQueueRepository

**Patrón Singleton:**

- **parte-Repository** - Adaptador de salida: almacenamiento centralizado de instancias de colas

- **parte-Singleton** - Garantiza única instancia durante toda la ejecución
  - `get_instance()` - Obtiene o crea la instancia única

**Operaciones CRUD:**

- **parte-Create** - Crea y almacena nueva cola
  - Valida que no exista duplicado

- **parte-Retrieve** - Obtiene cola por ID

- **parte-Delete** - Elimina cola del storage

- **parte-Exists** - Verifica existencia de cola

- **parte-All** - Retorna todas las colas

- **parte-Clear** - Limpia todo el storage (útil para reset)

- **parte-Reset** - Resetea la instancia singleton (testing)

---

## Capa de Aplicación (Application / Use Cases)

### EnqueueCustomerUseCase

**Orquestación de inserción:**

- **parte-EnqueueUseCase** - Coordinación completa de encolamiento de cliente

- **parte-Init** - Configuración del use case con ID de cola

- **parte-Execute** - Operación principal:
  1. Obtiene cola del repositorio
  2. Intenta enqueue
  3. Retorna resultado con estado

---

### DequeueCustomerUseCase

**Orquestación de extracción:**

- **parte-DequeueUseCase** - Coordinación de desencolamiento respetando prioridad

- **parte-Execute** - Operación principal:
  1. Obtiene cola del repositorio
  2. Dequeue automático respeatiendo orden
  3. Retorna cliente o None

---

### PeekQueueUseCase

**Orquestación de consulta:**

- **parte-PeekUseCase** - Coordinación de lookahead sin modificación

- **parte-Execute** - Operación principal:
  1. Obtiene cola del repositorio
  2. Consulta cliente siguiente sin extraer
  3. Retorna cliente o None

---

## Integración en Simulación (DiscreteEventSimulation)

### Constructor

- **parte-QueueSetup** - Inicialización de sistema de cola
  - Obtiene repositorio singleton
  - Crea política con max_queue_capacity de config
  - Inicializa dequeue use case

### Método initialize()

- **parte-QueueReset** - Limpieza y preparación de cola fresca
  - Elimina cola anterior si existe
  - Crea nueva cola con policy
  - Reinicializa use case

### Método handle_arrival()

- **parte-EnqueueOperation** - Inserción de cliente en cola de prioridad
  - Valida capacidad
  - Respeta orden automático
  - Registra rechazos si aplica

- **parte-Jhonny** Hook - Integración con sistema de métricas
  - Registra long itud de cola después de enqueue

### Método _assign_free_teller()

- **parte-AssignLogic** - Búsqueda de ventanilla disponible

- **parte-DequeuePriority** - Extracción respetando orden de prioridad
  - Dequeue automático respeta:
    1. Prioridad (1 > 2 > 3)
    2. FIFO dentro del nivel (timestamp)

- **parte-Jhonny** Hook - Integración con métricas
  - Registra cambio de longitud al desencolar

### Método run()

- **parte-FinalMetrics** - Contabilización de clientes rechazados al final
  - Cuenta remanentes en cola
  - Registra como rechazados

---

## Patrones de Comentarios

### Estructura de Parte-Comentario

```python
# parte-NombreSignificativo: descripción breve de funcionalidad
# Explicación detallada de qué hace este código y por qué
# - Punto 1 sobre la implementación
# - Punto 2 sobre la implementación
```

### Ejemplos en Contexto

#### Para Algoritmos
```python
def _heapify_down(self, index: int) -> None:
    """
    parte-HeapifyDown: Restores min-heap property after removal.
    Bubbles element at 'index' downward until heap property is satisfied.
    """
```

#### Para Decisiones de Diseño
```python
# parte-Ordering: Compares first by priority, then by arrival_sequence for FIFO
```

#### Para Hooks de Integración
```python
# parte-Jhonny: Register final queue length as cleared
```

---

## Resumen de Comentarios por Categoría

### Estructura (16)
- Entity, ValueObject, UseCase, QueueNode, TieBreaker, Preemption, PriorityQueue, BinaryHeapAdapter, Repository, Singleton, EnqueueUseCase, DequeueUseCase, PeekUseCase, QueueSetup, AssignLogic, FinalMetrics

### Algoritmos (5)
- Ordering, Enqueue, Dequeue, HeapifyUp, HeapifyDown

### Validación (2)
- CapacityCheck, RejectionLogic

### CRUD (7)
- Create, Retrieve, Delete, Exists, All, Clear, Reset

### Implementación (18)
- Init (aparece 6 veces), EnqueueOperation, DequeuePriority, QueueReset, Execute (aparece 3 veces), Peek, Empty, Size, GetId, GetPolicy, Jhonny (aparece 3 veces), Adapter (aparece 3 veces)

---

## Notas de Estilo

- Todos los comentarios `parte-` están en INGLÉS (estándar de desarrollo)
- Describen el QUÉ y el POR QUÉ, no el CÓMO (que está en el código)
- Son lo suficientemente concisos para lectura rápida
- Se agrupan con explana ciones de contexto más amplias

