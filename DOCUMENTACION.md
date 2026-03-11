# DOCUMENTACION TECNICA — SimulationBank

Simulacion discreta de eventos para un sistema bancario de colas con multiples ventanillas, prioridades dinamicas y analisis de rendimiento en tiempo real.

---

## Tabla de Contenidos

1. [Vision General del Sistema](#1-vision-general-del-sistema)
2. [Stack Tecnologico](#2-stack-tecnologico)
3. [Arquitectura del Sistema](#3-arquitectura-del-sistema)
4. [Estructura de Directorios](#4-estructura-de-directorios)
5. [Backend — Descripcion Detallada](#5-backend--descripcion-detallada)
   - 5.1 [Punto de Entrada: main.py](#51-punto-de-entrada-mainpy)
   - 5.2 [Motor de Simulacion de Eventos Discretos](#52-motor-de-simulacion-de-eventos-discretos)
   - 5.3 [La Cola de Prioridad (Binary Heap)](#53-la-cola-de-prioridad-binary-heap)
   - 5.4 [Generador de Clientes](#54-generador-de-clientes)
   - 5.5 [Modulo de Ventanillas (Tellers)](#55-modulo-de-ventanillas-tellers)
   - 5.6 [Modulo de Metricas](#56-modulo-de-metricas)
   - 5.7 [Dominio Compartido (Shared)](#57-dominio-compartido-shared)
   - 5.8 [API REST — Endpoints](#58-api-rest--endpoints)
6. [Frontend — Descripcion Detallada](#6-frontend--descripcion-detallada)
   - 6.1 [App.jsx — Raiz de la Aplicacion](#61-appjsx--raiz-de-la-aplicacion)
   - 6.2 [SimulationPanel — Orquestador](#62-simulationpanel--orquestador)
   - 6.3 [ConfigForm — Formulario de Configuracion](#63-configform--formulario-de-configuracion)
   - 6.4 [StatusIndicator — Estado en Vivo](#64-statusindicator--estado-en-vivo)
   - 6.5 [MetricsChart — Resultados y Diagnostico](#65-metricschart--resultados-y-diagnostico)
   - 6.6 [Componentes de Modulos Auxiliares](#66-componentes-de-modulos-auxiliares)
7. [Modelo de Dominio](#7-modelo-de-dominio)
8. [Flujo Completo de una Simulacion](#8-flujo-completo-de-una-simulacion)
9. [Teoria de Colas Aplicada](#9-teoria-de-colas-aplicada)
   - 9.1 [Formula de Intensidad de Trafico](#91-formula-de-intensidad-de-trafico)
   - 9.2 [Tres Escenarios de Operacion](#92-tres-escenarios-de-operacion)
10. [Metricas del Sistema Explicadas](#10-metricas-del-sistema-explicadas)
11. [Como Ejecutar el Proyecto](#11-como-ejecutar-el-proyecto)
12. [Variables de Configuracion de la Simulacion](#12-variables-de-configuracion-de-la-simulacion)
13. [Patrones de Diseno Utilizados](#13-patrones-de-diseno-utilizados)
14. [Glosario de Terminos](#14-glosario-de-terminos)

---

## 1. Vision General del Sistema

**SimulationBank** es un simulador de colas bancarias que modela el comportamiento de un banco real mediante **Simulacion de Eventos Discretos (DES)**. En lugar de ejecutarse en tiempo real, el sistema avanza mediante un reloj virtual que salta de evento en evento, lo que permite simular jornadas completas de trabajo (8 horas) en segundos.

### Que simula exactamente

El sistema modela el flujo completo desde que un cliente llega al banco hasta que termina su transaccion:

```
Cliente llega → Ingresa a la cola (si hay espacio) → Espera su turno →
Es llamado a una ventanilla libre → Recibe atencion → Sale del sistema
```

Si la cola esta llena cuando el cliente llega, es **rechazado** (no puede esperar) y el sistema lo contabiliza en la tasa de abandono.

### Que problema resuelve

Permite a un administrador bancario responder preguntas como:
- ¿Cuantas ventanillas necesito para no rechazar mas del 2% de clientes?
- ¿Cual es el tiempo de espera promedio con la configuracion actual?
- ¿Las ventanillas estan siendo bien aprovechadas o hay tiempo muerto excesivo?
- ¿Que pasa si duplico la tasa de llegada de clientes en hora pico?

---

## 2. Stack Tecnologico

### Backend

| Tecnologia | Version | Uso |
|:---|:---|:---|
| **Python** | 3.10+ | Lenguaje principal del backend |
| **Flask** | 3.x | Framework web ligero para la API REST |
| **Flask-CORS** | 5.x | Permite peticiones cross-origin desde el frontend |
| **Modulo `heapq`** | stdlib | Cola de prioridad binaria para eventos de simulacion |
| **Modulo `random`** | stdlib | Generacion de numeros aleatorios para distribuciones |
| **Modulo `uuid`** | stdlib | Generacion de IDs unicos para simulaciones y clientes |
| **Modulo `threading`** | stdlib | Ejecucion de simulaciones en hilos separados del servidor |

### Frontend

| Tecnologia | Version | Uso |
|:---|:---|:---|
| **React** | 18.x | Biblioteca de UI para componentes reactivos |
| **Vite** | 5.x | Bundler y servidor de desarrollo con HMR |
| **JavaScript (ES2022)** | — | Lenguaje principal del frontend |
| **Vanilla CSS** | — | Estilos sin frameworks externos |
| **Fetch API** | stdlib | Comunicacion HTTP con el backend |

---

## 3. Arquitectura del Sistema

El proyecto implementa dos patrones arquitectonicos complementarios:

### Arquitectura Hexagonal (Ports and Adapters)

Cada modulo del backend esta aislado del mundo exterior mediante **puertos** (interfaces abstractas) y **adaptadores** (implementaciones concretas). Esto significa que la logica de negocio no depende directamente de Flask, de la base de datos, ni de ninguna tecnologia especifica.

```
┌─────────────────────────────────────────────────────────┐
│                    MUNDO EXTERIOR                        │
│         (Flask HTTP, Postman, Frontend React)           │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────────┐
│               ADAPTADORES DE ENTRADA                     │
│         (Blueprints Flask / Controllers)                │
└──────────────────────┬──────────────────────────────────┘
                       │ llama a
┌──────────────────────▼──────────────────────────────────┐
│               CASOS DE USO (Application)                 │
│    start_simulation, get_simulation_state, etc.         │
└──────────┬───────────────────────────────┬──────────────┘
           │ usa                           │ usa
┌──────────▼──────────┐         ┌──────────▼──────────────┐
│   DOMINIO (Domain)  │         │    PUERTOS (Ports)       │
│  Logica de negocio  │         │  Interfaces abstractas   │
│  sin dependencias   │         │  (Repository, Generator) │
└─────────────────────┘         └──────────┬──────────────┘
                                           │ implementado por
                                ┌──────────▼──────────────┐
                                │  ADAPTADORES DE SALIDA   │
                                │  (InMemory repos, etc.)  │
                                └─────────────────────────┘
```

### Vertical Slicing (Cortes Verticales)

En lugar de organizar el codigo por capas horizontales (todos los modelos juntos, todos los controladores juntos), el codigo esta organizado por **funcionalidad de negocio**. Cada "slice" es una feature completa e independiente:

```
src/
├── customer/        <-- Todo lo relacionado con clientes
├── queue/           <-- Todo lo relacionado con la cola
├── teller/          <-- Todo lo relacionado con ventanillas
├── metrics/         <-- Todo lo relacionado con estadisticas
├── simulation/      <-- Motor y orquestacion de la simulacion
└── shared/          <-- Utilidades transversales
```

Cada slice contiene sus propias subcarpetas `domain/`, `application/`, e `infrastructure/`.

---

## 4. Estructura de Directorios

### Estructura completa del proyecto

```
SimulationBank/
├── DOCUMENTACION.md              ← Este archivo
├── backend/
│   ├── main.py                   ← Punto de entrada del servidor Flask
│   ├── requirements.txt          ← Dependencias Python (flask, flask-cors)
│   └── src/
│       ├── customer/
│       │   ├── application/
│       │   │   └── generate_customer.py
│       │   ├── domain/
│       │   │   ├── arrival_time.py       ← Value Object: tiempo de llegada
│       │   │   ├── customer.py           ← Entidad principal: cliente
│       │   │   ├── priority.py           ← Enum: Alta/Media/Baja
│       │   │   ├── service_time.py       ← Value Object: tiempo de servicio
│       │   │   ├── transaction_type.py   ← Enum: tipos de transaccion
│       │   │   └── ports/
│       │   │       └── customer_generator.py  ← Puerto: interfaz generadora
│       │   └── infrastructure/
│       │       └── poisson_customer_generator.py  ← Adaptador: genera con distribuciones
│       │
│       ├── queue/
│       │   ├── application/
│       │   │   ├── dequeue_customer.py   ← Caso de uso: extraer cliente
│       │   │   ├── enqueue_customer.py   ← Caso de uso: ingresar cliente
│       │   │   └── peek_queue.py         ← Caso de uso: ver proximo sin extraer
│       │   ├── domain/
│       │   │   ├── priority_queue.py     ← Entidad: min-heap con desempate FIFO
│       │   │   ├── queue_node.py         ← Nodo del heap
│       │   │   ├── queue_policy.py       ← Politica de capacidad y rechazo
│       │   │   └── ports/
│       │   │       └── queue_repository.py  ← Puerto: repositorio de colas
│       │   └── infrastructure/
│       │       ├── binary_heap_queue.py        ← Alternativa de implementacion
│       │       └── in_memory_queue_repository.py ← Adaptador: almacena en memoria
│       │
│       ├── teller/
│       │   ├── domain/
│       │   │   └── teller.py             ← Entidad: cajero/ventanilla
│       │   └── infrastructure/
│       │       └── teller_blueprint.py   ← Endpoint REST de ventanillas
│       │
│       ├── metrics/
│       │   ├── application/
│       │   │   ├── get_simulation_report.py   ← Caso de uso: obtener reporte
│       │   │   ├── record_customer_rejected.py
│       │   │   └── record_customer_served.py
│       │   ├── domain/
│       │   │   ├── simulation_metrics.py ← Entidad acumuladora de estadisticas
│       │   │   ├── throughput_record.py  ← Value Object: registro de tasa de procesamiento
│       │   │   ├── wait_time_record.py   ← Value Object: registro de tiempos
│       │   │   └── ports/
│       │   │       └── metrics_repository.py
│       │   └── infrastructure/
│       │       ├── in_memory_metrics_repository.py
│       │       ├── metrics_blueprint.py  ← Endpoints REST de metricas
│       │       └── metrics_controller.py
│       │
│       ├── simulation/
│       │   ├── application/
│       │   │   ├── get_simulation_results.py ← Caso de uso: obtener resultados
│       │   │   ├── get_simulation_state.py   ← Caso de uso: obtener estado actual
│       │   │   └── start_simulation.py       ← Caso de uso: iniciar simulacion
│       │   ├── domain/
│       │   │   ├── simulation.py             ← MOTOR CENTRAL: DiscreteEventSimulation
│       │   │   ├── simulation_config.py      ← Configuracion del usuario
│       │   │   ├── simulation_event.py       ← Eventos del motor (ARRIVAL, etc.)
│       │   │   └── simulation_status.py      ← Estados: IDLE/RUNNING/FINISHED
│       │   └── infrastructure/
│       │       ├── in_memory_simulation_repository.py
│       │       └── simulation_blueprint.py   ← Endpoints REST de simulacion
│       │
│       └── shared/
│           ├── application/
│           │   └── use_case.py           ← Clase base abstracta para casos de uso
│           └── domain/
│               ├── domain_event.py       ← Clase base para eventos de dominio
│               ├── entity.py             ← Clase base para entidades (con ID)
│               └── value_object.py       ← Clase base para Value Objects (inmutables)
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx                       ← Componente raiz, verifica backend
        ├── App.css                       ← Sistema de estilos global
        ├── main.jsx                      ← Punto de entrada React
        ├── simulation/
        │   ├── components/
        │   │   ├── SimulationPanel.jsx   ← Orquestador principal de la UI
        │   │   ├── ConfigForm.jsx        ← Formulario de parametros
        │   │   ├── MetricsChart.jsx      ← Resultados + diagnostico adaptativo
        │   │   ├── StatusIndicator.jsx   ← Indicador de estado en vivo
        │   │   └── SimulationControls.jsx
        │   └── services/
        │       └── simulationService.js  ← Capa de comunicacion con el backend
        ├── metrics/
        │   └── components/
        │       ├── MetricsDashboard.jsx
        │       ├── QueueLengthChart.jsx
        │       ├── SaturationReport.jsx
        │       ├── ThroughputChart.jsx
        │       └── WaitTimeChart.jsx
        ├── queue/
        │   └── components/
        │       ├── QueueVisualizer.jsx
        │       ├── QueueNode.jsx
        │       └── PriorityLegend.jsx
        ├── teller/
        │   └── components/
        │       ├── TellerGrid.jsx
        │       ├── TellerCard.jsx
        │       └── TellerRow.jsx
        └── shared/
            └── components/
                ├── Badge.jsx
                ├── Button.jsx
                ├── Card.jsx
                ├── Layout.jsx
                ├── Navbar.jsx
                └── Slider.jsx
```

---

## 5. Backend — Descripcion Detallada

### 5.1 Punto de Entrada: main.py

`main.py` es el archivo que arranca el servidor Flask. Sus responsabilidades son:

1. **Crear la aplicacion Flask** y configurarla
2. **Habilitar CORS** para que el frontend (corriendo en puerto 5173) pueda comunicarse con el backend (puerto 5000) sin restricciones de origen
3. **Registrar todos los Blueprints** de cada modulo vertical (simulation, metrics, teller)
4. **Exponer endpoints de utilidad** como `/health` (verificacion de vida del servidor) y `/api/default-config` (configuracion por defecto para el formulario)

```
GET  /health           → {"status": "ok", "message": "..."}
GET  /api/default-config → devuelve los parametros predeterminados de simulacion
```

---

### 5.2 Motor de Simulacion de Eventos Discretos

**Archivo:** `backend/src/simulation/domain/simulation.py`

**Clase:** `DiscreteEventSimulation`

Este es el **corazon del sistema**. Implementa la tecnica de Simulacion de Eventos Discretos (DES), en la que el tiempo no avanza de segundo en segundo sino que salta directamente al siguiente evento programado.

#### Tipos de Eventos

```python
class EventType(Enum):
    ARRIVAL       # Cliente llega al banco
    SERVICE_START # Cajero comienza a atender a un cliente
    SERVICE_END   # Cajero termina de atender a un cliente
```

#### Cola de Eventos (Linea de Tiempo)

El motor mantiene una **cola de prioridad de eventos** ordenada cronologicamente usando `heapq` de Python. Esto garantiza que siempre se procesa el evento mas temprano primero.

```
event_queue (min-heap por tiempo):
┌─────────────────────────────────────────────────────┐
│  t=0.4s: ARRIVAL                                    │
│  t=0.4s: SERVICE_START (T-1, Cliente-A)             │
│  t=1.2s: ARRIVAL                                    │
│  t=5.4s: SERVICE_END (T-1)                          │
│  t=2.1s: ARRIVAL                                    │
└─────────────────────────────────────────────────────┘
```

#### Ciclo Principal del Motor (run)

```
1. Extraer el evento con menor timestamp de event_queue
2. Verificar que el tiempo del evento no supere max_simulation_time
3. Avanzar el reloj (clock) al tiempo del evento
4. Ejecutar process_next_event(event)
5. Repetir hasta que event_queue este vacio o se supere el tiempo
```

#### Flujo de un evento ARRIVAL

```
handle_arrival()
    ├── Generar atributos del cliente (prioridad, tipo transaccion, tiempo servicio)
    ├── Crear instancia Customer con arrival_time = clock actual
    ├── Intentar queue.enqueue(customer)
    │     ├── Si hay espacio → cliente ingresa, actualizar metrica de longitud de cola
    │     └── Si cola llena → metrics.record_rejection()
    ├── Programar SIGUIENTE ARRIVAL (clock + intervalo_exponencial)
    └── Intentar _assign_free_teller()
          ├── Buscar teller con estado IDLE
          ├── Si hay teller libre Y cliente en cola → queue.dequeue()
          └── Programar SERVICE_START para ese teller en clock actual
```

#### Flujo de un evento SERVICE_END

```
handle_service_end(teller_id)
    ├── teller.end_service() → teller queda IDLE
    └── _assign_free_teller() → intentar atender siguiente en cola
```

---

### 5.3 La Cola de Prioridad (Binary Heap)

**Archivo:** `backend/src/queue/domain/priority_queue.py`

**Clase:** `PriorityQueue`

Esta es la **estructura de datos central** del modulo `queue`. Implementa un **min-heap binario** que garantiza que siempre se extrae al cliente de mayor prioridad en tiempo O(log n).

#### Reglas de Ordenamiento

El heap ordena los nodos con dos criterios:
1. **Prioridad del cliente** (1=Alta, 2=Media, 3=Baja). Menor numero = mayor prioridad.
2. **FIFO dentro del mismo nivel**: Si dos clientes tienen la misma prioridad, atiende primero al que llego antes (`arrival_sequence`).

#### Operaciones y Complejidad

| Operacion | Metodo | Complejidad |
|:---|:---|:---:|
| Insertar cliente | `enqueue(customer)` | **O(log n)** |
| Extraer mayor prioridad | `dequeue()` | **O(log n)** |
| Ver proximo sin extraer | `peek()` | **O(1)** |
| Verificar si esta vacio | `is_empty()` | **O(1)** |
| Consultar tamano | `size()` | **O(1)** |

#### Politica de Capacidad (QueuePolicy)

```python
class QueuePolicy:
    max_queue_size: int    # -1 = ilimitada
    allow_rejections: bool # True = rechazar si est full
    
    def should_reject(self, current_size: int) -> bool:
        # Retorna True si debe rechazar al cliente
```

Si `max_queue_size = 50` y la cola ya tiene 50 clientes, el proximo en llegar es rechazado y se registra en las metricas.

#### Representacion Visual del Heap

```
Prioridades: Alta(1) > Media(2) > Baja(3)

         [Alta, t=0.4]         ← Raiz: siempre el de mayor prioridad
          /          \
  [Alta, t=0.6]   [Media, t=0.3]
     /      \
[Baja,t=0.1] [Media,t=0.8]
```

---

### 5.4 Generador de Clientes

**Archivo:** `backend/src/customer/infrastructure/poisson_customer_generator.py`

**Clase:** `ConfigurableGenerator`

Genera los parametros aleatorios de cada cliente usando distribuciones estadisticas configurables.

#### Distribuciones de Llegada (Tiempo entre llegadas)

| Tipo | Funcion | Descripcion |
|:---|:---|:---|
| `exponential` (Proceso de Poisson) | `random.expovariate(lambda)` | Memoryless, modela llegadas aleatorias reales |
| `fixed` | `1.0 / lambda` | Llegadas a intervalos exactos constantes |

> La distribucion exponencial de tiempos entre llegadas es **matematicamente equivalente** a un proceso de Poisson de tasa lambda. Es la distribucion mas usada para modelar llegadas bancarias porque no tiene memoria (la espera del proximo cliente no depende de cuanto tiempo lleva sin llegar nadie).

#### Distribuciones de Servicio (Duracion de atencion)

| Tipo | Funcion | Descripcion |
|:---|:---|:---|
| `exponential` | `random.expovariate(1/mu)` | Variable, algunos tramites son rapidos, otros lentos |
| `normal` | `random.gauss(mu, sigma)` | Campana de Gauss, tramites con tiempo estimado |
| `constant` | `service_mean` | Todos los tramites duran exactamente lo mismo |

#### Prioridades y Tipos de Transaccion

- Las prioridades se asignan aleatoriamente con pesos configurables (ej. 10% alta, 30% media, 60% baja)
- Los tipos de transaccion (deposito, retiro, prestamo, etc.) se seleccionan uniformemente

---

### 5.5 Modulo de Ventanillas (Tellers)

**Archivo:** `backend/src/teller/domain/teller.py`

**Clase:** `Teller`

Representa una ventanilla bancaria. Tiene dos estados posibles:

```
IDLE   ← → BUSY
```

- `start_service(customer, clock)` → pasa de IDLE a BUSY, registra inicio de atencion
- `end_service()` → pasa de BUSY a IDLE, libera la ventanilla

Los cajeros son inicializados con IDs `T-1`, `T-2`, `T-3`, etc. segun el numero configurado por el usuario.

---

### 5.6 Modulo de Metricas

**Archivo:** `backend/src/metrics/domain/simulation_metrics.py`

**Clase:** `SimulationMetrics`

Acumula todos los datos estadisticos durante la simulacion. Actua como un "recolector de datos" pasivo al que el motor le reporta cada evento relevante.

#### Datos que Acumula

| Atributo | Tipo | Descripcion |
|:---|:---|:---|
| `wait_times` | `List[WaitTimeRecord]` | Tiempo de espera de cada cliente atendido |
| `queue_length_history` | `List[(float, int)]` | Historial de (timestamp, longitud_cola) |
| `customers_served` | `int` | Contador de clientes atendidos exitosamente |
| `customers_rejected` | `int` | Contador de clientes rechazados |
| `total_teller_work_time` | `float` | Tiempo total acumulado que los cajeros pasaron ocupados |

#### Calculo Final de Estadisticas (calculate_statistics)

Al terminar la simulacion, este metodo procesa todos los datos crudos y devuelve:

```json
{
  "estadisticas_globales": {
    "max_cola": 15,
    "promedio_cola": 7.3,
    "tiempo_espera_promedio": 124.5,
    "utilizacion_ventanillas_porcentaje": 87.2,
    "tasa_procesamiento_clientes_por_segundo": 0.0083,
    "porcentaje_abandono": 12.5,
    "total_servidos": 420,
    "total_rechazados": 60
  },
  "tiempo_espera_por_prioridad": {
    "Prioridad 1": 15.2,
    "Prioridad 2": 89.7,
    "Prioridad 3": 198.4
  },
  "historial_cola": [
    {"minuto": 0.4, "longitud": 1},
    {"minuto": 0.9, "longitud": 2},
    ...
  ]
}
```

#### Formula de Utilizacion de Ventanillas

```
utilizacion (%) = (tiempo_total_cajeros_ocupados / (tiempo_simulacion × num_cajeros)) × 100
```

---

### 5.7 Dominio Compartido (Shared)

**Directorio:** `backend/src/shared/domain/`

Contiene las clases base que todos los modulos heredan para mantener consistencia arquitectonica:

| Clase | Descripcion |
|:---|:---|
| `Entity` | Clase base con `entity_id: str`. Toda entidad tiene identidad propia. |
| `ValueObject` | Clase base inmutable. No tiene identidad, solo datos (ej. `ArrivalTime`). |
| `DomainEvent` | Base para eventos de dominio (ej. `CustomerArrived`). |
| `UseCase` | Interfaz abstracta con metodo `execute()` para todos los casos de uso. |

---

### 5.8 API REST — Endpoints

Todos los endpoints tienen prefijo `/api`.

#### Simulacion

| Metodo | Endpoint | Descripcion | Body / Respuesta |
|:---|:---|:---|:---|
| `POST` | `/api/simulation/start` | Inicia una nueva simulacion | Body: `SimulationConfig` JSON |
| `GET` | `/api/simulation/{id}/state` | Consulta el estado actual | `{status, progress}` |
| `GET` | `/api/simulation/{id}/results` | Obtiene los resultados al terminar | `{metrics}` |

#### Metricas

| Metodo | Endpoint | Descripcion |
|:---|:---|:---|
| `GET` | `/api/metrics/{sim_id}/report` | Reporte completo de metricas |

#### Utilidades

| Metodo | Endpoint | Descripcion |
|:---|:---|:---|
| `GET` | `/health` | Verifica que el servidor esta vivo |
| `GET` | `/api/default-config` | Retorna la configuracion predeterminada |

---

## 6. Frontend — Descripcion Detallada

### 6.1 App.jsx — Raiz de la Aplicacion

**Archivo:** `frontend/src/App.jsx`

Es el componente de mas alto nivel. Al montarse:
1. Hace un `GET /health` al backend para verificar conectividad
2. Si el backend no responde, muestra un banner de error
3. Si el backend responde, hace `GET /api/default-config` para cargar los valores por defecto del formulario
4. Renderiza `<SimulationPanel defaultConfig={...} />`

---

### 6.2 SimulationPanel — Orquestador

**Archivo:** `frontend/src/simulation/components/SimulationPanel.jsx`

Es el **coordinador central** de toda la interfaz. Gestiona el estado global de la simulacion y conecta todos los componentes hijo.

#### Estado que gestiona

| Estado | Tipo | Descripcion |
|:---|:---|:---|
| `currentSimulationId` | `string \| null` | ID de la simulacion activa |
| `simulationStatus` | `string \| null` | Estado: `initializing / running / completed / error` |
| `simulationProgress` | `number` | Porcentaje de progreso (0-100) |
| `results` | `object \| null` | Metricas finales de la simulacion |
| `error` | `string \| null` | Mensaje de error si fallo algo |
| `usedConfig` | `object \| null` | Copia de la configuracion usada (para diagnostico) |

#### Mecanismo de Polling

Una vez iniciada la simulacion, `SimulationPanel` inicia un `setInterval` de 500ms que consulta `GET /api/simulation/{id}/state` repetidamente. Cuando el estado pasa a `completed`, detiene el intervalo y obtiene los resultados finales.

---

### 6.3 ConfigForm — Formulario de Configuracion

**Archivo:** `frontend/src/simulation/components/ConfigForm.jsx`

Renderiza el formulario de configuracion con los siguientes campos:

| Campo | Parametro | Rango | Descripcion |
|:---|:---|:---|:---|
| Numero de Ventanillas | `num_tellers` | 1–20 | Cajeros activos |
| Tasa de Llegadas (λ) | `arrival_rate` | 0.1–10.0 | Clientes por segundo |
| Tiempo Medio de Atencion (μ) | `service_mean` | 1–300 seg | Segundos por cliente |
| Duracion de la Simulacion | `max_simulation_time` | 3600–86400 seg | Segundos de simulacion |
| Capacidad Maxima de la Cola | `max_queue_capacity` | 1–500 | Maximo de personas en fila |
| Dist. de Llegadas | `arrival_dist` | exponential / poisson | Como llegan los clientes |
| Dist. de Servicio | `service_dist` | exponential / normal / constant | Como varian los tiempos de atencion |
| Peso Prioridad Alta | `priority_high` | 0–100% | Porcentaje de clientes preferenciales |
| Peso Prioridad Media | `priority_medium` | 0–100% | Porcentaje de clientes estandar |
| Peso Prioridad Baja | `priority_low` | 0–100% | Porcentaje de clientes normales |

Incluye validacion en tiempo real: los pesos de prioridad deben sumar exactamente 100%.

---

### 6.4 StatusIndicator — Estado en Vivo

**Archivo:** `frontend/src/simulation/components/StatusIndicator.jsx`

Muestra el estado actual de la simulacion con colores semaforo y barra de progreso:

| Estado | Color | Descripcion |
|:---|:---|:---|
| `initializing` | Amarillo | Preparando entorno |
| `running` | Verde | Simulacion en curso |
| `paused` | Azul | Pausada |
| `completed` | Verde exito | Finalizada exitosamente |
| `error` | Rojo | Error durante ejecucion |
| `idle` (default) | Gris | Listo para iniciar |

---

### 6.5 MetricsChart — Resultados y Diagnostico

**Archivo:** `frontend/src/simulation/components/MetricsChart.jsx`

Es el componente mas complejo del frontend. Recibe tanto las `metrics` (resultados) como el `config` (parametros usados) y presenta tres bloques:

#### Bloque 1: Diagnostico Adaptativo

Calcula la intensidad de trafico (rho) con los parametros reales del usuario y clasifica el escenario:

```javascript
rho = arrival_rate / (num_tellers * (1 / service_mean))
```

| rho | Clasificacion | Color |
|:---|:---|:---|
| >= 1.5 | Sistema Saturado | Rojo |
| 0.95 – 1.49 | Sistema Sobrecargado | Naranja |
| 0.70 – 0.94 | Sistema Optimo | Verde |
| < 0.70 | Sistema Subutilizado | Azul |

Para cada clasificacion muestra:
- Explicacion de que esta pasando
- Numero exacto de ventanillas necesarias para la solucion (rho → 0.85)
- Numero exacto para configuracion optima (rho → 0.80)

#### Bloque 2: Tarjetas KPI

Indicadores clave mostrados en tarjetas con codigo de colores y texto interpretativo en lenguaje natural (no numeros crudos).

#### Bloque 3: Tabla Detallada

Todas las metricas con su valor formateado (tiempos en min/seg, porcentajes con contexto de personas), su descripcion textual y su calificacion (BUENO/REGULAR/MALO).

---

### 6.6 Componentes de Modulos Auxiliares

| Componente | Modulo | Descripcion |
|:---|:---|:---|
| `QueueVisualizer` | queue | Visualizacion grafica de la cola |
| `TellerGrid / TellerCard` | teller | Representacion de las ventanillas |
| `MetricsDashboard` | metrics | Panel de metricas avanzadas |
| `SaturationReport` | metrics | Reporte de saturacion |
| `Badge, Button, Card` | shared | Componentes reutilizables de UI |
| `Navbar, Layout` | shared | Estructura y navegacion |

---

## 7. Modelo de Dominio

El modelo central del sistema tiene las siguientes entidades y sus relaciones:

```
┌─────────────────────┐
│  SimulationConfig   │ ← Configuracion provista por el usuario
│  - num_tellers      │
│  - arrival_rate (λ) │
│  - service_mean (μ) │
│  - max_sim_time     │
│  - max_queue_cap    │
│  - arrival_config   │
│  - service_config   │
└──────────┬──────────┘
           │ usa
┌──────────▼──────────────────────────────────────────────┐
│            DiscreteEventSimulation                       │
│  - simulation_id : str                                   │
│  - status: SimulationStatus (IDLE/RUNNING/FINISHED)      │
│  - clock: float (segundos simulados)                     │
│  - event_queue: List[SimulationEvent]  ← min-heap       │
│  - tellers: Dict[str, Teller]                           │
│  - metrics: SimulationMetrics                            │
│  - generator: ConfigurableGenerator                      │
│  - queue_repo: InMemoryQueueRepository                   │
└─────────────────────────────────────────────────────────┘
           │ coordina
      ┌────┴──────────────┬────────────────┐
      ▼                   ▼                ▼
┌───────────┐    ┌──────────────┐  ┌────────────────────┐
│  Customer │    │    Teller    │  │  SimulationMetrics │
│  - id     │    │  - id        │  │  - wait_times      │
│  - arrival│    │  - status    │  │  - queue_history   │
│  - service│    │  IDLE/BUSY   │  │  - served_count    │
│  - priority    └──────────────┘  │  - rejected_count  │
│  - txn_type                      └────────────────────┘
└───────────┘
      │ almacenado en
┌─────▼───────────────────────────────┐
│          PriorityQueue               │
│  Min-Heap binario                   │
│  Regla 1: prioridad (1 > 2 > 3)     │
│  Regla 2: FIFO dentro del mismo nivel │
│  enqueue(): O(log n)                │
│  dequeue(): O(log n)                │
└──────────────────────────────────────┘
```

### Ciclo de Vida de un Cliente

```
[AFUERA] → ARRIVAL event → [EN COLA] → SERVICE_START event → [SIENDO ATENDIDO] → SERVICE_END event → [SALE]
                  ↓ si cola llena
              [RECHAZADO] → metrics.record_rejection()
```

---

## 8. Flujo Completo de una Simulacion

### Desde el usuario hasta los resultados

```
1. USUARIO configura parametros en ConfigForm
         ↓
2. SimulationPanel llama POST /api/simulation/start
         ↓
3. Backend crea DiscreteEventSimulation con el SimulationConfig
         ↓
4. Lanza simulation.run() en un HILO SEPARADO (threading)
   para no bloquear el servidor Flask
         ↓
5. Motor: programa el primer ARRIVAL, entra al bucle principal
         ↓
6. Bucle: extrae evento → adelanta clock → procesa evento
   ├── ARRIVAL: genera cliente, intenta encolar, programa siguiente
   ├── SERVICE_START: cajero empieza, registra tiempo espera
   └── SERVICE_END: cajero queda libre, atiende siguiente de la cola
         ↓
7. Mientras corre: Frontend hace polling GET /state cada 500ms
   y actualiza la barra de progreso y el estado en pantalla
         ↓
8. Motor: reloj supera max_simulation_time → status = FINISHED
         ↓
9. Frontend detecta status 'completed' → GET /api/simulation/{id}/results
         ↓
10. Backend llama calculate_statistics() y devuelve el JSON de metricas
         ↓
11. MetricsChart recibe metrics + config original
    → Calcula rho, clasifica escenario, muestra diagnostico adaptativo
    → Muestra KPIs con interpretacion en lenguaje natural
    → Muestra tabla detallada
```

---

## 9. Teoria de Colas Aplicada

### 9.1 Formula de Intensidad de Trafico

El sistema implementa un modelo **M/M/c** de la Teoria de Colas:
- **M** (Markovian = memoria corta = exponencial): Llegadas con proceso de Poisson
- **M**: Tiempos de servicio con distribucion exponencial
- **c**: `c` servidores (ventanillas) en paralelo

La metrica mas importante es **rho (ρ)**, la intensidad de trafico:

```
rho = λ / (c × μ)

donde:
  λ = arrival_rate       (clientes por segundo)
  μ = 1 / service_mean   (atenciones por segundo por cajero)
  c = num_tellers        (numero de ventanillas)
```

**Interpretacion:**
- `rho < 1` → Sistema estable. Las ventanillas pueden absorber toda la demanda.
- `rho = 1` → Sistema en el limite. Un solo cliente de mas puede colapsarlo.
- `rho > 1` → Sistema matematicamente inestable. La cola crece indefinidamente.

### 9.2 Tres Escenarios de Operacion

#### Escenario Saturado (rho >= 1.5)

| Parametro | Valor ejemplo |
|:---|:---:|
| Ventanillas | 2 |
| Llegadas/seg | 3.0 |
| Seg/atencion | 12  |
| rho | 18.0 |

**Consecuencias:** Cola llena en minutos. Mas del 90% de clientes rechazados.
**Solucion:** `ventanillas_necesarias = ceil(lambda * service_mean / 0.85)`

#### Escenario Optimo (0.70 <= rho < 0.95)

| Parametro | Valor ejemplo |
|:---|:---:|
| Ventanillas | 6 |
| Llegadas/seg | 1.0 |
| Seg/atencion | 5   |
| rho | 0.83 |

**Consecuencias:** Cajeros trabajan 83% del tiempo. Espera baja. Rechazo < 2%.
**Por que no rho = 0.5?** Con rho demasiado bajo los cajeros estan ociosos el 50% del tiempo → costo operativo innecesario.

#### Escenario Subutilizado (rho < 0.70)

**Consecuencias:** Personal sin trabajo la mayor parte del tiempo. Costo operativo alto sin beneficio proporcional.

---

## 10. Metricas del Sistema Explicadas

| Metrica | Clave JSON | Unidad | Descripcion |
|:---|:---|:---|:---|
| Tiempo de espera promedio | `tiempo_espera_promedio` | segundos | Tiempo medio que los clientes aguardan en la fila antes de ser llamados |
| Ocupacion de ventanillas | `utilizacion_ventanillas_porcentaje` | % | Porcentaje del tiempo que los cajeros estuvieron activamente atendiendo vs inactivos |
| Total atendidos | `total_servidos` | personas | Clientes que completaron su transaccion exitosamente |
| Total rechazados | `total_rechazados` | personas | Clientes que llegaron con cola llena y no pudieron entrar |
| Porcentaje de abandono | `porcentaje_abandono` | % | `(rechazados / (atendidos + rechazados)) × 100` |
| Pico maximo de cola | `max_cola` | personas | El mayor numero de personas que esperaban al mismo tiempo |
| Promedio de cola | `promedio_cola` | personas | Media historica de personas en fila durante la simulacion |
| Velocidad de atencion | `tasa_procesamiento_clientes_por_segundo` | cl/seg | Cuantos clientes por segundo fue capaz de atender el banco en promedio |
| Tiempo espera por prioridad | `tiempo_espera_por_prioridad` | segundos | Desglose del tiempo de espera separado por nivel de prioridad |

### Interpretacion de la Ocupacion de Ventanillas

| Valor | Calificacion | Significado |
|:---|:---|:---|
| < 60% | Subutilizado | Cajeros ociosos demasiado tiempo |
| 60% – 94% | Optimo | Buen balance carga/capacidad |
| >= 95% | Saturado | Sin margen para picos de demanda |

---

## 11. Como Ejecutar el Proyecto

### Requisitos previos

- Python 3.10 o superior
- Node.js 18 o superior
- npm o pnpm

### Backend

```bash
# Desde la carpeta backend/
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor (puerto 5000)
python main.py
```

El servidor quedara disponible en: `http://localhost:5000`

### Frontend

```bash
# Desde la carpeta frontend/
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo (puerto 5173)
npm run dev
```

La interfaz quedara disponible en: `http://localhost:5173`

### Verificar que todo funciona

```bash
# Verificar backend
curl http://localhost:5000/health
# Respuesta: {"status": "ok", "message": "..."}

# Verificar configuracion por defecto
curl http://localhost:5000/api/default-config
```

---

## 12. Variables de Configuracion de la Simulacion

El cuerpo JSON que se envia a `POST /api/simulation/start`:

```json
{
  "num_tellers": 3,
  "max_simulation_time": 28800,
  "max_queue_capacity": 100,
  "arrival_config": {
    "arrival_rate": 1.0,
    "arrival_dist": "exponential"
  },
  "service_config": {
    "service_mean": 5.0,
    "service_dist": "exponential",
    "service_stddev": 1.0
  },
  "priority_weights": [0.1, 0.3, 0.6]
}
```

| Campo | Tipo | Rango | Descripcion |
|:---|:---|:---|:---|
| `num_tellers` | int | 1 – 20 | Numero de ventanillas activas |
| `max_simulation_time` | float | 3600 – 86400 | Duracion en segundos simulados (3600 = 1 hora, 28800 = 8 horas) |
| `max_queue_capacity` | int | 1 – 500 | Personas maximas en la fila. -1 = ilimitado |
| `arrival_rate` | float | 0.1 – 10.0 | Lambda: clientes que llegan por segundo |
| `arrival_dist` | string | `exponential`, `poisson` | Distribucion para tiempos entre llegadas |
| `service_mean` | float | 1.0 – 300.0 | Mu: segundos promedio de cada atencion |
| `service_dist` | string | `exponential`, `normal`, `constant` | Distribucion para duracion de servicios |
| `service_stddev` | float | > 0 | Solo para `service_dist = "normal"` |
| `priority_weights` | array[3] | suman 1.0 | [peso_alta, peso_media, peso_baja] |

---

## 13. Patrones de Diseno Utilizados

| Patron | Donde se aplica | Beneficio |
|:---|:---|:---|
| **Repository Pattern** | `InMemoryQueueRepository`, `InMemorySimulationRepository` | Desacopla la logica de negocio del mecanismo de almacenamiento |
| **Port & Adapter (Hexagonal)** | Cada modulo vertical | Permite cambiar Flask por FastAPI, o memoria por BD, sin tocar el dominio |
| **Factory Method** | `ConfigurableGenerator` | Crea distribuciones segun configuracion sin exponer logica interna |
| **Use Case Pattern** | `StartSimulationUseCase`, `GetSimulationStateUseCase`, etc. | Cada operacion de negocio es una clase independiente y testeable |
| **Value Object** | `WaitTimeRecord`, `ArrivalTime`, `ServiceTime` | Datos inmutables sin identidad propia, solo valor |
| **Entity** | `Customer`, `Teller`, `PriorityQueue`, `DiscreteEventSimulation` | Objetos con identidad unica que cambian de estado |
| **Singleton** | `InMemoryQueueRepository.get_instance()` | Un solo repositorio compartido por toda la simulacion |
| **Observer (implicito)** | Polling en `SimulationPanel` | El frontend observa el estado del backend periodicamente |

---

## 14. Glosario de Terminos

| Termino | Definicion |
|:---|:---|
| **DES (Discrete Event Simulation)** | Tecnica donde el tiempo avanza de evento en evento en vez de forma continua. Permite simular horas en milisegundos. |
| **rho (ρ)** | Intensidad de trafico. Indica que tan cargado esta el sistema. rho = λ / (c × μ). |
| **lambda (λ)** | Tasa de llegadas: cuantos clientes llegan por unidad de tiempo. |
| **mu (μ)** | Tasa de servicio: cuantos clientes puede atender una ventanilla por unidad de tiempo. |
| **Proceso de Poisson** | Modelo matematico para llegadas aleatorias independientes. Los tiempos entre llegadas siguen una distribucion exponencial. |
| **Min-Heap (Heap Minimo)** | Arbol binario donde el nodo raiz siempre tiene el valor minimo. Permite extraer el minimo en O(log n). |
| **FIFO** | First In, First Out. Principio de cola donde el primero en llegar es el primero en ser atendido. |
| **Arquitectura Hexagonal** | Patron donde el nucleo de la aplicacion (dominio) no depende de tecnologias externas. |
| **Vertical Slicing** | Organizacion del codigo por funcionalidad de negocio completa en vez de por capa tecnica. |
| **Polling** | Tecnica donde el frontend consulta repeatedly al backend para conocer el estado actualizado. |
| **Blueprint (Flask)** | Forma de organizar las rutas de Flask en grupos modulares por funcionalidad. |
| **Value Object** | Objeto de dominio definido por su valor, no por su identidad. Es inmutable. |
| **Puerto (Port)** | Interfaz abstracta que define como interactua el dominio con el exterior. |
| **Adaptador (Adapter)** | Implementacion concreta de un puerto. Puede ser para memoria, BD, HTTP, etc. |
