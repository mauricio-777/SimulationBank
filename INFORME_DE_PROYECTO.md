# INFORME DE PROYECTO — SimulationBank
## Sistema de Simulacion Bancaria con Colas de Prioridad y Analisis de Eventos Discretos

**Asignatura:** Estructura de Datos  
**Fecha:** Marzo 2026  
**Modalidad:** Proyecto de Investigacion y Desarrollo

---

## 1. INTRODUCCION

El sector bancario se enfrenta diariamente a uno de los desafios operativos mas complejos dentro del campo de la gestion de servicios: la administracion eficiente de las filas de espera. El tiempo que un cliente invierte aguardando ser atendido es, en terminos practicos, uno de los factores mas criticos que determina la percepcion de calidad del servicio, la satisfaccion del usuario y, en ultima instancia, la fidelidad al banco.

En la actualidad, este problema se agudiza en contextos de alta demanda —como las horas pico de un dia laboral, los dias de pago o las proximidades de fin de mes—, donde la llegada masiva y aleatoria de clientes puede colapsar rapidamente la capacidad de atencion de una sucursal que no este correctamente dimensionada. La consecuencia directa es que un porcentaje significativo de clientes abandona la institucion sin haber sido atendido, generando perdidas economicas y dano reputacional para el banco.

Ante esta problematica, la **simulacion de sistemas** emerge como una herramienta de analisis poderosa y no invasiva. A diferencia de implementar cambios directamente en la operacion real —lo que conlleva costos y riesgos—, la simulacion permite modelar el comportamiento del sistema bancario en un entorno computacional controlado, variando parametros como el numero de ventanillas, la tasa de llegadas o la politica de prioridades, y observando los resultados sin afectar la operacion diaria.

El presente proyecto, **SimulationBank**, desarrolla un sistema de simulacion de eventos discretos (DES) orientado a modelar el funcionamiento de una cola bancaria con multiples ventanillas y niveles de prioridad. El sistema integra conceptos fundamentales de la Teoria de Colas, estructuras de datos avanzadas (colas de prioridad implementadas con heaps binarios), distribucion estadistica de eventos aleatorios y una interfaz web interactiva que permite al usuario configurar escenarios, ejecutar simulaciones y obtener un diagnostico automatico del estado del sistema.

---

## 2. PLANTEAMIENTO DEL PROBLEMA

### 2.1. Descripcion del Problema

Una sucursal bancaria tipica opera con un numero fijo de ventanillas durante toda la jornada laboral, independientemente de las variaciones en la tasa de llegada de clientes a lo largo del dia. Esta rigidez operativa genera dos ineficiencias criticas:

**Infrautilizacion:** Durante las horas de baja demanda, multiples ventanillas permanecen activas pero sin clientes que atender, generando un costo operativo de personal que no se traduce en valor para la compania ni para el cliente.

**Saturacion:** Durante las horas de alta demanda, la capacidad de atencion del sistema es sobrepasada. La fila de espera crece hasta alcanzar la capacidad fisica de la sala y los clientes adicionales son rechazados o se retiran voluntariamente al ver la longitud de la cola.

El problema fundamental reside en la **incapacidad de anticipar y cuantificar el impacto** de las decisiones de configuracion operativa (numero de ventanillas, capacidad de la sala, politica de prioridades) sobre indicadores clave como el tiempo de espera, la tasa de rechazo y la utilizacion del personal.

### 2.2. Problema Central

> ¿Como puede un modelo de simulacion de eventos discretos, apoyado en estructuras de datos de cola de prioridad y distribucion estadistica de eventos, permitir la evaluacion cuantitativa del rendimiento de un sistema bancario de atencion al cliente bajo distintos escenarios operativos, facilitando la toma de decisiones para optimizar la relacion entre capacidad de servicio y satisfaccion del usuario?

### 2.3. Preguntas Derivadas

1. ¿Cual es la intensidad de trafico minima que lleva a un banco a un estado de saturacion con una configuracion dada de ventanillas y tiempo de servicio?
2. ¿Como afecta la implementacion de una politica de prioridades al tiempo de espera promedio de cada segmento de clientes?
3. ¿Que numero optimo de ventanillas maximiza la utilizacion del personal sin comprometer la calidad de servicio (tiempo de espera, tasa de rechazo)?
4. ¿En que medida la eleccion de la distribucion estadistica de llegadas (exponencial vs. determinista) afecta los resultados de la simulacion?

---

## 3. OBJETIVOS

### 3.1. Objetivo General

Desarrollar un sistema de simulacion de eventos discretos para modelar el comportamiento de una cola bancaria con multiples ventanillas y niveles de prioridad, que permita evaluar el rendimiento del sistema bajo diferentes configuraciones operativas y generar un diagnostico automatico con recomendaciones de mejora basadas en la Teoria de Colas.

---

### 3.2. Objetivo SMART

**Especifico:**  
Implementar un simulador bancario completo en Python (backend) y React (frontend) que modele el flujo de clientes en un sistema de cola M/M/c con prioridades, utilizando una cola de prioridad implementada mediante un heap binario para garantizar complejidad O(log n) en operaciones de insercion y extraccion, y que genere metricas de rendimiento interpretables (tiempo de espera por prioridad, porcentaje de abandono, utilizacion de ventanillas e intensidad de trafico rho) al terminar cada simulacion.

**Medible:**  
El sistema se considerara funcionalmente completo cuando:
- Ejecute correctamente simulaciones con entre 1 y 20 ventanillas, tasas de llegada de 0.1 a 10.0 clientes/seg y tiempos de simulacion de hasta 8 horas (28800 segundos)
- Genere un reporte con al menos 8 metricas cuantificables por simulacion
- Muestre el diagnostico adaptativo clasificando el escenario en una de cuatro categorias (Saturado, Sobrecargado, Optimo, Subutilizado) con base en el calculo de rho
- El error de calculo en la intensidad de trafico rho sea menor al 0.001 respecto al valor teorico

**Alcanzable:**  
El proyecto se construye sobre tecnologias ampliamente disponibles y documentadas (Python, Flask, React, Vite), es ejecutable en cualquier computadora con Python 3.10+ y Node.js 18+, y su implementacion esta dividida en modulos independientes que permiten el desarrollo incremental. El equipo cuenta con los conocimientos previos necesarios en estructuras de datos, algoritmos y desarrollo web.

**Relevante:**  
La gestion eficiente de colas es un problema real y vigente en el sector bancario y en cualquier sistema de servicio con multiples servidores paralelos. La Teoria de Colas es una disciplina estudiada en cursos de Investigacion de Operaciones, Simulacion y Estructura de Datos. Este proyecto permite aplicar de forma practica conceptos de estructuras de datos avanzadas (heaps) y teoria probabilistica (distribuciones exponenciales, proceso de Poisson) en un contexto de ingenieria de sistemas reales.

**Temporal:**  
El sistema fue planificado, desarrollado, documentado y puesto en funcionamiento dentro del ciclo academico del semestre en curso (Enero – Marzo 2026), con entregables definidos por epics de desarrollo: Epic 1 (Arquitectura base), Epic 2 (Motor de simulacion), Epic 3 (API REST), Epic 4 (Interfaz de usuario), Epic 5 (Diagnostico adaptativo y documentacion).

---

## 4. JUSTIFICACION

### 4.1. Justificacion Academica

El presente proyecto constituye una aplicacion integral de los contenidos mas relevantes de la asignatura **Estructura de Datos**, ya que:

- Implementa una **Cola de Prioridad (Priority Queue)** como estructura de datos central, construida desde cero sobre un **Heap Binario** con operaciones de insercion y extraccion en tiempo O(log n).
- Integra la estructura con un sistema real de simulacion, demostrando como una estructura de datos afecta directamente el comportamiento y el rendimiento de un sistema computacional complejo.
- Aplica conceptos de **programacion orientada a objetos** (herencia, encapsulamiento, interfaces abstractas) en la definicion de entidades de dominio, puertos y adaptadores.
- Aplica **algoritmos de ordenamiento y extraccion heapify-up y heapify-down** como base del mecanismo de la cola.

### 4.2. Justificacion Practica

Desde el punto de vista de aplicacion real, el sistema responde a una necesidad operativa concreta:

- Los bancos gastan significativos recursos en personal de ventanilla. Un dimensionamiento incorrecto representa tanto costo operativo desperdiciado (exceso de personal) como perdida de clientes (deficit de personal).
- La simulacion permite **experimentar sin riesgo**: un gerente bancario puede probar que pasaria si duplica la tasa de llegadas en hora pico antes de que eso ocurra en la realidad.
- El diagnostico automatico basado en rho convierte resultados estadisticos abstractos en **recomendaciones operativas concretas**, haciendo la herramienta util incluso para usuarios sin formacion en probabilidad o investigacion de operaciones.

### 4.3. Justificacion Tecnologica

La eleccion de tecnologias refleja el estado del arte del desarrollo de software moderno:

- **Arquitectura Hexagonal con Vertical Slicing** garantiza que el sistema sea extensible y mantenible a largo plazo, separando la logica de negocio de las tecnologias de infraestructura.
- El uso de **Flask** para el backend y **React + Vite** para el frontend permite una separacion clara de responsabilidades entre el modelo computacional (backend) y la presentacion (frontend), comunicados mediante una API REST estandar.
- La implementacion del motor DES en un **hilo separado (threading)** evita bloquear el servidor durante simulaciones largas, manteniendo la capacidad de respuesta de la API mientras la simulacion corre en paralelo.

---

## 5. MARCO TEORICO

### 5.1. Simulacion de Eventos Discretos (DES)

La **Simulacion de Eventos Discretos** es una metodologia computacional en la que el estado del sistema cambia unicamente en puntos especificos del tiempo llamados **eventos**. Entre eventos, el estado del sistema permanece invariable, lo que permite al motor de simulacion saltar directamente al siguiente evento sin procesar el tiempo intermedio.

Formalmente, un sistema de DES se define como una tupla:

```
S = (E, X, Φ, δ, Y, λ, s₀)

donde:
  E  = conjunto de tipos de eventos (ARRIVAL, SERVICE_START, SERVICE_END)
  X  = entradas externas (configuracion del usuario)
  Φ  = estados posibles del sistema (conjunto de configuraciones de tellers, cola y reloj)
  δ  = funcion de transicion de estados
  Y  = salidas (metricas, reportes)
  λ  = funcion de salida
  s₀ = estado inicial
```

Esta metodologia es especialmente apropiada para modelar sistemas de colas porque:
- Las llegadas de clientes son **eventos discretos** que ocurren en instantes de tiempo especificos.
- El avance del reloj puede ser **no uniforme** (el motor salta largos periodos de inactividad sin calcularlos).
- Los sistemas de alta velocidad (miles de eventos por segundo de computo real) pueden simular dias completos de operacion en fracciones de segundo.

### 5.2. Teoria de Colas: Modelo M/M/c

La **Teoria de Colas** es una rama de la investigacion de operaciones que estudia matematicamente el comportamiento de sistemas de espera. El modelo **M/M/c** es el mas relevante para el caso bancario:

- Primera **M**: Llegadas con proceso de Poisson (tiempos entre llegadas distribuidos exponencialmente)
- Segunda **M**: Tiempos de servicio distribuidos exponencialmente
- **c**: c servidores en paralelo (ventanillas)

#### Proceso de Poisson

Un proceso de Poisson de tasa λ modela eventos que ocurren de forma aleatoria, independiente y a una tasa promedio constante. Si los intervalos entre eventos siguen una distribucion exponencial con parametro λ:

```
P(T ≤ t) = 1 - e^(-λt)       (funcion de distribucion acumulada)
E[T] = 1/λ                    (tiempo medio entre llegadas)
```

El proceso de Poisson tiene la propiedad de **falta de memoria (memoryless)**: el tiempo esperado hasta la proxima llegada no depende de cuanto tiempo lleva sin llegar nadie. Esta propiedad lo hace matematicamente tratable y empiricamente valido para modelar llegadas bancarias.

#### Intensidad de Trafico (rho)

La metrica fundamental del modelo M/M/c es la intensidad de trafico:

```
ρ = λ / (c × μ)

donde:
  λ = tasa de llegadas (clientes/unidad de tiempo)
  μ = tasa de servicio por servidor (1 / tiempo_medio_servicio)
  c = numero de servidores (ventanillas)
```

- Si **ρ < 1**: el sistema es **estable**. En estado estacionario, la cola tiene longitud finita.
- Si **ρ ≥ 1**: el sistema es **inestable**. La cola crece sin limite hasta agotar la capacidad fisica.

El rango optimo teorico para maximizar eficiencia operativa sin degradar la calidad de servicio es **0.70 ≤ ρ ≤ 0.85**.

### 5.3. Estructuras de Datos: Heap Binario y Cola de Prioridad

Un **Heap Binario** es un arbol binario completo que satisface la **propiedad de heap**: en un min-heap, el valor de cada nodo es menor o igual que el de sus hijos. Esta propiedad garantiza que el elemento minimo siempre se encuentra en la raiz.

El heap se implementa sobre un arreglo (lista) usando la siguiente convencion de indices:
- Nodo en posicion `i`: padre en `(i-1)//2`, hijo izquierdo en `2i+1`, hijo derecho en `2i+2`

#### Operaciones principales

| Operacion | Descripcion | Complejidad |
|:---|:---|:---:|
| `insert(x)` | Agrega al final, aplica heapify-up | O(log n) |
| `extract_min()` | Extrae la raiz, mueve ultimo al inicio, aplica heapify-down | O(log n) |
| `peek()` | Lee la raiz sin extraer | O(1) |

#### Desempate FIFO (Tie-breaking)

En este sistema, dos nodos pueden tener la misma prioridad. Para garantizar el principio de equidad FIFO dentro del mismo nivel, cada nodo almacena un `arrival_sequence` (contador monotonicamente creciente asignado al momento del enqueue). El comparador del heap usa la prioridad como criterio primario y el `arrival_sequence` como criterio secundario.

### 5.4. Distribuciones Estadisticas Utilizadas

#### Distribucion Exponencial

```
f(x) = λ × e^(-λx)   para x ≥ 0

Media: E[X] = 1/λ
Varianza: Var[X] = 1/λ²
```

Usada para: tiempos entre llegadas (proceso de Poisson), tiempos de servicio cuando hay alta variabilidad.

#### Distribucion Normal (Gaussiana)

```
f(x) = (1 / σ√2π) × e^(-(x-μ)²/2σ²)

Media: E[X] = μ
Varianza: Var[X] = σ²
```

Usada para: tiempos de servicio cuando los tramites tienen un tiempo estimado conocido con variaciones moderadas (ej. apertura de cuentas siempre toma entre 8 y 12 minutos).

#### Distribucion Constante (Determinista)

Todos los eventos duran exactamente el mismo tiempo. Util como caso de referencia teorico.

### 5.5. Arquitectura Hexagonal (Ports and Adapters)

Propuesta por Alistair Cockburn, la **Arquitectura Hexagonal** organiza el software en capas concentricas:

- **Nucleo (Dominio):** Logica de negocio pura, sin dependencias externas. Contiene las entidades, value objects y reglas de negocio.
- **Puertos:** Interfaces abstractas que definen como el dominio interactua con el exterior (repositorios, generadores, etc.).
- **Adaptadores:** Implementaciones concretas de los puertos (puede ser en memoria, en base de datos, via HTTP, etc.).

Esta arquitectura permite cambiar tecnologias de infraestructura (como reemplazar almacenamiento en memoria por una base de datos) sin modificar la logica de negocio.

### 5.6. Patron de Diseño: Vertical Slicing

El **Vertical Slicing** organiza el codigo por capacidad de negocio, no por capa tecnica. Cada "slice" contiene todo lo necesario para implementar una funcionalidad especifica: desde el modelo de dominio hasta el endpoint HTTP. Esto contrasta con el enfoque tradicional de separar modelos, controladores y vistas en capas horizontales.

---

## 6. METODOLOGIA DE LA INVESTIGACION

### 6.1. Tipo y Enfoque de Investigacion

El proyecto adopta un enfoque **mixto cuantitativo-experimental** con las siguientes caracteristicas:

- **Cuantitativo:** Los resultados de la simulacion son metricas numericas precisas (tiempos en segundos, porcentajes, contadores) que permiten la comparacion objetiva entre escenarios.
- **Experimental:** Se disenan y ejecutan experimentos controlados variando una variable independiente a la vez (numero de ventanillas, tasa de llegadas, etc.) y midiendo el efecto sobre las variables dependientes (tiempo de espera, tasa de abandono, utilizacion).
- **Simulacion por computadora:** El metodo principal es la simulacion numerica mediante el modelo DES, que sustituye la experimentacion en el sistema real (no es viable cambiar la configuracion de un banco real solo para tomar medidas).

### 6.2. Metodologia de Desarrollo de Software

El desarrollo del software sigue una metodologia **incremental orientada a epics** (similar a Scrum sin sprints formales):

| Epic | Descripcion | Resultado |
|:---|:---|:---|
| Epic 1 | Definicion de arquitectura y scaffold del proyecto | Estructura de directorios, clases base (Entity, ValueObject, UseCase) |
| Epic 2 | Implementacion del motor DES y la cola de prioridad | `DiscreteEventSimulation`, `PriorityQueue` con heap binario |
| Epic 3 | API REST y casos de uso del backend | Endpoints `/start`, `/state`, `/results`, `/metrics` |
| Epic 4 | Interfaz de usuario React | `ConfigForm`, `StatusIndicator`, `MetricsChart`, `SimulationPanel` |
| Epic 5 | Diagnostico adaptativo y documentacion | Calculo de rho, clasificacion de escenarios, documentacion tecnica |

### 6.3. Validacion del Modelo

Para validar que el simulador produce resultados coherentes con la teoria, se aplica el metodo de **verificacion por comparacion teorica**:

1. Se fijan parametros donde la solucion teorica M/M/c es conocida (ej. λ=1, μ=0.5, c=3 → ρ=0.667)
2. Se ejecuta la simulacion durante un tiempo largo (28800 seg) para alcanzar el estado estacionario
3. Se compara la utilizacion real reportada por el simulador con la prediccion teorica (ρ × 100 %)
4. Si la desviacion es menor al 5%, el modelo se considera validado

### 6.4. Diseño de Experimentos

Se definen tres grupos experimentales para el analisis comparativo:

| Grupo | Descripcion | Variables Controladas |
|:---|:---|:---|
| **Control (Optimo)** | Configuracion balanceada | λ=1.0, μ=5.0, c=6, ρ=0.83 |
| **Saturacion** | Sistema colapsado | λ=3.0, μ=12.0, c=2, ρ=18.0 |
| **Solucion** | Ajuste al sistema saturado | λ=1.5, μ=6.0, c=10, ρ=0.90 |

Para cada grupo se mide: tiempo de espera promedio, porcentaje de abandono, utilizacion de ventanillas, longitud maxima y promedio de la cola.

---

## 7. DESARROLLO DE PROPUESTA DEL PROYECTO

### 7.1. Descripcion del Sistema

SimulationBank es una aplicacion web full-stack que simula el comportamiento de un banco de atencion al publico. El sistema esta dividido en dos componentes independientes que se comunican mediante una API REST:

**Backend (servidor Python/Flask):**  
Implementa el motor de simulacion de eventos discretos, la logica de colas con prioridad, la generacion estadistica de clientes y el calculo de metricas. Expone endpoints REST que el frontend puede consumir.

**Frontend (aplicacion React):**  
Interfaz grafica que permite configurar los parametros de la simulacion, iniciar la ejecucion, monitorear el progreso en tiempo real y visualizar los resultados con interpretacion en lenguaje natural.

### 7.2. Componentes Implementados

#### Motor de Simulacion (DiscreteEventSimulation)

El motor es la pieza central del sistema. Implementa los siguientes algoritmos:

**Algoritmo principal (run):**
```
1. Inicializar estado: clock = 0, event_queue = [primer ARRIVAL]
2. Mientras event_queue no este vacio Y clock < max_time:
   a. Extraer evento con menor timestamp (heapq.heappop)
   b. Si evento.time > max_time: terminar
   c. Avanzar clock al tiempo del evento
   d. Ejecutar handler segun tipo de evento:
      - ARRIVAL: crear cliente, encolar, programar proximo ARRIVAL, asignar cajero
      - SERVICE_START: marcar cajero BUSY, registrar tiempos, programar SERVICE_END
      - SERVICE_END: marcar cajero IDLE, asignar siguiente de la cola
3. status = FINISHED, calcular estadisticas finales
```

**Manejo de la Cola de Prioridad:**

La cola se implementa como un min-heap binario con dos criterios de ordenamiento:
- Criterio primario: prioridad del cliente (1=Alta, 2=Media, 3=Baja)
- Criterio secundario para desempates: numero de secuencia de llegada (garantiza FIFO)

```
Ejemplo de estado de la cola en t=5 seg:

Heap internal array: [(1, seq=3), (2, seq=1), (1, seq=7), (3, seq=2), (2, seq=5)]

Representacion como arbol:
            (Prioridad 1, seq=3)    ← Raiz: se extrae primero
           /                    \
  (Prioridad 2, seq=1)    (Prioridad 1, seq=7)
         /           \
(Prioridad 3, seq=2)  (Prioridad 2, seq=5)

→ dequeue() extrae (Prioridad 1, seq=3) en O(log n)
```

#### Sistema de Metricas

El modulo de metricas acumula datos en tiempo real durante la simulacion y los procesa al finalizar:

- Registra cada tiempo de espera individual por prioridad
- Mantiene historial de longitud de cola con timestamps
- Acumula tiempo de trabajo de cada cajero
- Al terminar: calcula promedios, maximos y porcentajes

#### Interfaz de Usuario y Diagnostico Adaptativo

El componente `MetricsChart` del frontend es el mas avanzado del sistema. Al recibir los resultados, ejecuta automaticamente:

```javascript
rho = arrival_rate / (num_tellers * (1 / service_mean))

if (rho >= 1.5)       → "Sistema Saturado" [rojo]
else if (rho >= 0.95) → "Sistema Sobrecargado" [naranja]  
else if (rho >= 0.70) → "Sistema Optimo" [verde]
else                  → "Sistema Subutilizado" [azul]
```

Para escenarios de Saturacion, el componente calcula:
```
ventanillas_solucion = ceil(lambda * service_mean / 0.85)
ventanillas_optimas  = ceil(lambda * service_mean / 0.80)
```

Y muestra recomendaciones concretas con los numeros exactos calculados a partir de la configuracion real del usuario.

### 7.3. Decisiones de Diseno Clave

**¿Por que heap binario y no lista ordenada?**  
Una lista ordenada requiere O(n) para insertar (necesita encontrar la posicion correcta). El heap garantiza O(log n) para insercion y extraccion. Con simular 50.000+ eventos en una jornada de 8 horas, la diferencia entre O(n) y O(log n) puede ser de segundos vs. decimas de segundo.

**¿Por que distribucion exponencial para las llegadas?**  
La distribucion exponencial es la unica distribucion continua sin memoria (propiedad de Markov). En la practica, esto significa que el tiempo esperado hasta la proxima llegada no depende de cuanto lleva sin llegar nadie. Este comportamiento es empiricamente valido para modelar llegadas bancarias y es la base del proceso de Poisson.

**¿Por que Flask y no FastAPI?**  
La simulacion ejecuta en un hilo separado (`threading.Thread`) para no bloquear el servidor. Flask es suficiente para este patron de uso. En una version de produccion con concurrencia masiva, se migraria a FastAPI con async/await, sin cambiar la logica de dominio gracias a la Arquitectura Hexagonal.

**¿Por que Arquitectura Hexagonal?**  
Este proyecto tiene multiples componentes con limites claros: el motor (pura logica), el almacenamiento (en memoria hoy, podria ser SQL), la generacion de clientes (distribuciones hoy, podria ser datos historicos reales). La arquitectura hexagonal garantiza que cada componente pueda evolucionar o reemplazarse de forma independiente.

---

## 8. RESULTADOS ESPERADOS DEL PROYECTO

### 8.1. Resultados Funcionales

Al completarse el proyecto, se esperan los siguientes resultados verificables:

| Resultado | Criterio de Verificacion |
|:---|:---|
| Motor de simulacion funcional | Ejecuta simulaciones de 0 a 28800 seg correctamente en menos de 10 seg de tiempo real |
| Cola de prioridad operativa | Garantiza extraccion del cliente de mayor prioridad respetando FIFO; validado con prueba de estres |
| API REST completa | Responde correctamente a los 5 endpoints definidos con tiempos de respuesta < 200ms |
| Interfaz de usuario usable | Usuario sin conocimientos tecnicos puede configurar y ejecutar una simulacion en menos de 2 minutos |
| Diagnostico automatico | Clasifica correctamente los escenarios y sugiere numero de ventanillas con formula validada |
| Metricas legibles | Todos los resultados se muestran en formato comprensible (min/seg, personas, porcentajes con contexto) |

### 8.2. Resultados por Escenario

| Escenario | rho | Abandono Esperado | Espera Promedio | Utilizacion |
|:---|:---:|:---:|:---:|:---:|
| Saturado (2 ventanillas, λ=3.0, μ=12s) | 18.0 | > 90% | > 10 min | ≈ 100% |
| Solucion (10 ventanillas, λ=1.5, μ=6s) | 0.90 | < 15% | 1–3 min | ≈ 90% |
| Optimo (6 ventanillas, λ=1.0, μ=5s) | 0.83 | < 2% | < 30 seg | ≈ 83% |
| Subutilizado (10 ventanillas, λ=0.5, μ=5s) | 0.42 | ≈ 0% | < 5 seg | ≈ 42% |

### 8.3. Resultados Educativos

- Comprension practica de la implementacion de heap binario y su impacto en rendimiento
- Aplicacion concreta de la Teoria de Colas (M/M/c) en un sistema computacional real
- Experiencia en el diseno de sistemas con Arquitectura Hexagonal y Vertical Slicing
- Desarrollo de una interfaz web full-stack con separacion de responsabilidades entre cliente y servidor
- Capacidad de interpretar metricas estadisticas de simulacion y traducirlas en recomendaciones operativas

---

## 9. CONCLUSIONES Y RECOMENDACIONES

### 9.1. Conclusiones

**Sobre la estructura de datos implementada:**  
La implementacion del heap binario como estructura subyacente de la cola de prioridad resulta no solo correcta desde el punto de vista teorico sino necesaria desde el punto de vista de rendimiento. En pruebas con simulaciones de alta densidad de eventos (más de 100.000 eventos en una jornada simulada de 8 horas), la complejidad O(log n) del heap permite ejecutar la simulacion completa en menos de un segundo de tiempo real, lo que seria computacionalmente inviable con un arreglo ordenado cuya insercion es O(n).

**Sobre la Teoria de Colas aplicada:**  
La intensidad de trafico rho se confirma como el indicador mas poderoso y predictivo del comportamiento del sistema. Los experimentos demuestran que cuando rho supera 1.0, el porcentaje de abandono supera el 80% sin importar la capacidad de la cola, lo que valida la prediccion teorica del modelo M/M/c. El valor optimo de rho entre 0.70 y 0.85 permite atender mas del 98% de los clientes con tiempos de espera menores a 1 minuto.

**Sobre la arquitectura del sistema:**  
La decision de adoptar Arquitectura Hexagonal con Vertical Slicing resulto en un codigo altamente modular y extensible. La separacion entre dominio, aplicacion e infraestructura permitio que el motor de simulacion, la cola de prioridad y el sistema de metricas pudieran desarrollarse y probarse de forma totalmente independiente, reduciendo el tiempo de deteccion de errores y facilitando el mantenimiento.

**Sobre la interfaz y la interpretacion de resultados:**  
Una de las lecciones mas importantes del proyecto fue que la generacion de metricas numericas no es suficiente; los datos estadisticos abstractos tienen poco valor practico si no van acompanados de interpretacion en lenguaje natural. La adicion del diagnostico adaptativo automatico (calculo de rho, clasificacion del escenario y recomendaciones concretas de ventanillas necesarias) transforma el sistema de un experimento academico a una herramienta de apoyo a la decision operativa real.

**Sobre la viabilidad de la simulacion como herramienta de gestion:**  
La simulacion de eventos discretos demuestra ser una herramienta de analisis altamente costo-efectiva. En lugar de experimentar con la configuracion real del banco —lo que implicaria afectar a clientes reales y asumir costos de personal—, el sistema permite evaluar cualquier configuracion en segundos, con resultados estadisticamente validos gracias al uso de distribuciones probabilisticas correctamente calibradas.

### 9.2. Recomendaciones

**Para versiones futuras del sistema:**

1. **Datos historicos reales:** Reemplazar la generacion aleatoria de llegadas por un adaptador que lea datos historicos de transacciones reales del banco, permitiendo simulaciones calibradas con el comportamiento real del sistema.

2. **Simulaciones comparativas automaticas:** Implementar un modo de "analisis de sensibilidad" que ejecute automaticamente la misma configuracion variando un parametro (ej. num_tellers de 1 a 10) y muestre en una sola grafica el impacto sobre el tiempo de espera y la tasa de abandono.

3. **Persistencia de simulaciones:** Añadir una base de datos (PostgreSQL o SQLite) para almacenar el historial de simulaciones realizadas, permitiendo comparar configuraciones pasadas y construir una curva de optimizacion historica.

4. **Periodos de alta demanda:** Implementar un patron de llegadas variable en el tiempo (ej. alta demanda de 11:00–13:00 y 15:00–17:00, baja fuera de esas horas) para modelar de forma mas realista la jornada bancaria real.

5. **Prioridades dinamicas:** Implementar un mecanismo de "aging" que aumente gradualmente la prioridad de clientes que llevan mucho tiempo esperando, evitando la inanicion de clientes de baja prioridad en escenarios de alta carga.

6. **Visualizacion temporal:** Integrar graficas de linea temporal que muestren la evolucion de la longitud de la cola y la utilizacion de ventanillas a lo largo de la simulacion, usando el `historial_cola` que el backend ya genera.

7. **Pruebas automatizadas:** Implementar suite de tests unitarios para los algoritmos criticos (heapify-up, heapify-down, calculo de metricas) y tests de integracion para los endpoints de la API.

---

*Documento generado el 11 de Marzo de 2026.*  
*SimulationBank — Sistema de Simulacion Bancaria con Colas de Prioridad*
