# Diagrama de Arquitectura - Cola de Prioridad en Simulación Bancaria

## Visión General de la Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DISCRETE EVENT SIMULATION ENGINE                      │
│                      (src/simulation/domain/)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐         ┌─────────────────────────────────────────┐ │
│  │   CONFIG     │         │   EVENT PROCESSING LOOP                 │ │
│  │              │         │   • handle_arrival()                    │ │
│  │ max_queue_   │         │   • handle_service_start()              │ │
│  │ capacity=100 │         │   • handle_service_end()                │ │
│  │              │         │   • _assign_free_teller()               │ │
│  └──────────────┘         └─────────────────────────────────────────┘ │
│         │                                     │                         │
│         │ creates policy                      │ uses queue              │
│         ▼                                     ▼                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │         PRIORITY QUEUE SYSTEM (Queue Layer)                    │   │
│  │                                                                 │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ InMemoryQueueRepository (Singleton)                    │   │   │
│  │  │  - Manages queue instances                             │   │   │
│  │  │  - get_queue(queue_id) → BinaryHeapQueueAdapter        │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  │                          │                                     │   │
│  │                          ▼                                     │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ BinaryHeapQueueAdapter (Infrastructure)                │   │   │
│  │  │ - enqueue(customer) → bool                              │   │   │
│  │  │ - dequeue() → Customer | None                           │   │   │
│  │  │ - peek() → Customer | None                              │   │   │
│  │  │ - is_empty() → bool                                     │   │   │
│  │  │ - size() → int                                          │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  │                          │                                     │   │
│  │                          ▼                                     │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ PriorityQueue (Domain Entity)                           │   │   │
│  │  │ - heap: List[QueueNode]                                 │   │   │
│  │  │ - sequence_counter: int                                 │   │   │
│  │  │ - enqueue() - O(log n)                                  │   │   │
│  │  │   └─ _heapify_up()                                      │   │   │
│  │  │ - dequeue() - O(log n)                                  │   │   │
│  │  │   └─ _heapify_down()                                    │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  │                          │                                     │   │
│  │                          ▼                                     │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ QueueNode (Value Object)                               │   │   │
│  │  │ - customer: Customer                                    │   │   │
│  │  │ - arrival_sequence: float (FIFO)                        │   │   │
│  │  │ - __lt__(): Compare by priority, then sequence          │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  │                                                                 │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │ QueuePolicy (Value Object)                             │   │   │
│  │  │ - tie_breaker: FIFO                                     │   │   │
│  │  │ - preemption: NON_PREEMPTIVE                            │   │   │
│  │  │ - max_queue_size: int (100)                             │   │   │
│  │  │ - allow_rejections: bool                                │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
            ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
            │  Use Cases  │  │  Customer   │  │   Metrics   │
            │             │  │   Domain    │  │   System    │
            │  Enqueue    │  │             │  │             │
            │  Dequeue    │  │  Priority   │  │  WaitTime   │
            │  Peek       │  │  ArrTime    │  │  Rejections │
            └─────────────┘  └─────────────┘  └─────────────┘
```

---

## Flujo de Datos en Operación

### Diagrama de Secuencia: Llegada de Cliente

```
┌─────────────────────────────────────────────────────────────────────┐
│ SIMULACIÓN                                                          │
│ └─ handle_arrival()                                                 │
│    │                                                                │
│    ├─ Crear Customer(priority=P, arrival_time=T)                   │
│    │                                                                │
│    └─ Obtener Queue del Repositorio                                │
│       │                                                            │
│       └─ queue.enqueue(customer)                                   │
│          │                                                         │
│          ├─ Si queue.should_reject() → return False               │
│          │                                                         │
│          └─ Crear QueueNode(customer, arrival_sequence=N)        │
│             │                                                     │
│             ├─ Agregar a heap: heap.append(node)                │
│             │                                                     │
│             └─ _heapify_up(len-1)                               │
│                └─ Bubble up mientras node < parent              │
│                   (Compara: priority, luego timestamp)          │
│                                                                  │
│    └─ Registrar en metrics: record_queue_length()               │
│                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Diagrama de Secuencia: Asignación a Ventanilla

```
┌─────────────────────────────────────────────────────────────────────┐
│ SIMULACIÓN                                                          │
│ └─ _assign_free_teller()                                            │
│    │                                                                │
│    └─ Para cada Teller:                                            │
│       │                                                            │
│       ├─ Si teller.IDLE:                                          │
│       │  │                                                        │
│       │  └─ queue.dequeue()                                       │
│       │     │                                                     │
│       │     ├─ Guardar root: best_node = heap[0]                │
│       │     │                                                     │
│       │     ├─ Mover último a root: heap[0] = heap[-1]          │
│       │     │                                                     │
│       │     └─ _heapify_down(0)                                  │
│       │        └─ Bubble down comparando con hijos              │
│       │           (Propiedad: padre < hijos en prioridad)       │
│       │                                                        │
│       └─ Retornar customer.priority MÁXIMA AUTOMÁTICAMENTE      │
│          (FIFO dentro del mismo nivel por arrival_sequence)     │
│                                                                  │
│    └─ Programar SERVICE_START event                              │
│       └─ Registrar wait_time en metrics                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Propiedades de Ordenamiento del Heap

### Relación de Nodos en QueueNode.__lt__()

```
Para dos nodos A y B:

A < B si:
  1. A.customer.priority < B.customer.priority
     (A tiene MAYOR prioridad que B)
     
  -o-
  
  2. A.customer.priority == B.customer.priority
     AND A.arrival_sequence < B.arrival_sequence
     (Mismo nivel de prioridad, A llegó PRIMERO → FIFO)


HIERARQUÍA DE PRIORIDAD:
═══════════════════════════════════════════════════════════════

Priority 1 (ALTA)    ← Extraído PRIMERO
    │
    ├─ Cliente A (timestamp=100)
    ├─ Cliente B (timestamp=150)
    └─ Cliente C (timestamp=200)
    
Priority 2 (MEDIA)   ← Extraído SEGUNDO (respeta FIFO)
    │
    ├─ Cliente D (timestamp=110)
    └─ Cliente E (timestamp=120)
    
Priority 3 (BAJA)    ← Extraído ÚLTIMO
    │
    └─ Cliente F (timestamp=105)


ORDEN DE DEQUEUE: A → B → C → D → E → F
```

---## Gestión de Capacidad y Rechazos

```
┌─────────────────────────────────────────────────┐
│ INICIO DE HANDEL ARRIVAL                        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ Crear Customer│
         └───────┬───────┘
                 │
                 ▼
     ┌───────────────────────────┐
     │ queue.enqueue(customer)   │
     └─────────┬─────────────────┘
               │
               ▼
     ┌─────────────────────────────────────┐
     │ queue.should_reject()?              │
     │ (current_size >= max_queue_size)    │
     └─────────┬──────────────┬────────────┘
             YES │            │ NO
               │  │            │  │
               │  │            │  ▼
               │  │    ┌─────────────────────┐
               │  │    │ queue.enqueue()     │
               │  │    │ Add to heap         │
               │  │    │ return True         │
               │  │    └─────────────────────┘
               │  │            │
               │  │            ▼
               │  │    Registrar en metrics
               │  │    queue_length ↑
               │  │
               ▼  │
       ┌────────────────────┐
       │ return False       │
       │ Customer RECHAZADO │
       └────────────────────┘
               │
               ▼
       Registrar rejection
       in metrics
```

---

## Patrones de Arquitectura Utilizados

### Clean Architecture / DDD (Domain Driven Design)

```
┌──────────────────────────────────────────────────────────┐
│ ARQUITECTURA POR CAPAS                                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Application Layer (Orchestration)                      │
│  ├─ EnqueueCustomerUseCase                             │
│  ├─ DequeueCustomerUseCase                             │
│  └─ PeekQueueUseCase                                   │
│                                                          │
│  Domain Layer (Business Logic)                          │
│  ├─ PriorityQueue (Entity)                             │
│  ├─ QueueNode (Value Object)                           │
│  └─ QueuePolicy (Value Object)                         │
│                                                          │
│  Infrastructure Layer (Implementation)                  │
│  ├─ BinaryHeapQueueAdapter (Adapter)                   │
│  └─ InMemoryQueueRepository (Repository)               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Patrones Utilizados

1. **Singleton Pattern** - InMemoryQueueRepository
2. **Adapter Pattern** - BinaryHeapQueueAdapter a PriorityQueue
3. **Repository Pattern** - InMemoryQueueRepository
4. **Value Object Pattern** - QueueNode, QueuePolicy
5. **Entity Pattern** - PriorityQueue
6. **Use Case Pattern** - Enqueue, Dequeue, Peek

---

## Complejidad Computacional

| Operación | Complejidad | Justificación |
|-----------|--|---|
| enqueue() | O(log n) | Heapify-up desde hoja hasta raíz |
| dequeue() | O(log n) | Heapify-down desde raíz hasta hoja |
| peek() | O(1) | Acceso directo a heap[0] |
| is_empty() | O(1) | Verificación de longitud |
| size() | O(1) | Longitud de lista |

**Capacidad:** Sin límite teórico (limitado por memoria disponible)
**Máximo configurado:** 100 clientes por defecto

