# 🎉 Épica 4 - Guía Rápida de Inicio

## ⚡ Comienza en 3 Pasos

### Paso 1: Inicia el Backend
```bash
cd backend
python main.py
```
✅ Verás: `Running on http://127.0.0.1:5000`

### Paso 2: Inicia el Frontend (Nueva Terminal)
```bash
cd frontend
npm run dev
```
✅ Verás: `http://localhost:5173`

### Paso 3: Abre en Navegador
Accede a: **http://localhost:5173**

---

## 🎯 ¿Qué puedes hacer ahora?

### 1️⃣ **Configurar Simulación**
- Define número de ventanillas (1-10)
- Establece tasa de llegadas λ (clientes por tiempo)
- Indica tiempo servicio μ (segundos)
- Elige duración total (1 a 24 horas)
- Especifica capacidad máxima de cola

### 2️⃣ **Ejecutar Simulación**
- Click "Start Simulation"
- El sistema valida automáticamente
- Backend ejecuta en thread separado
- No bloquea la interfaz

### 3️⃣ **Monitorear Progreso**
- Ves barra de progreso en tiempo real
- Estado actualizado automáticamente
- Se monitorea cada 500ms

### 4️⃣ **Ver Resultados**
Una vez completada, ves automáticamente:
- **5 KPIs** principales en tarjetas coloreadas
- **Tabla** con todas las métricas
- **Gráficas** de barras para comparación
- **Insights** con recomendaciones

---

## 📊 Ejemplo de Uso

```
Usuario ingresa:
├─ Tellers: 3
├─ λ (Arrival Rate): 1.5
├─ μ (Service Time): 5.0 segundos
├─ Duration: 8 horas
└─ Max Queue: 100

↓ [Click "Start Simulation"]

Backend:
├─ Crea simulación con ID único
├─ Ejecuta en thread separado
└─ Procesa eventos discretos

Frontend:
├─ Monitorea cada 500ms
├─ Muestra: "Running 45%"
└─ Al 100%: Obtiene resultados

Resultados Visuales:
├─ KPI Cards:
│  ├─ Average Wait Time: 2.3s ✅
│  ├─ Customers Served: 432
│  ├─ Utilization: 78%
│  └─ Rejection Rate: 2%
├─ Tabla completa de métricas
└─ Gráficas interactivas
```

---

## 🔧 Parámetros Disponibles

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| **Tellers** | 1-10 | Número de vendedores en la bancada |
| **λ (Lambda)** | 0.1-10 | Clientes que llegan por unidad tiempo |
| **μ (Mu)** | 1-30s | Tiempo promedio de servicio |
| **Duration** | 1h-24h | Cuánto tiempo simular |
| **Queue Capacity** | 1+ | Máximo en fila de espera |

---

## 🎨 Visualización de Resultados

### Tarjetas KPI (Cards)
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ WAIT TIME       │  │ CUSTOMERS SERVED│  │ UTILIZATION     │
│     2.3s        │  │       432       │  │      78%        │
│   ✅ GOOD       │  │  ✅ GOOD        │  │  ✅ GOOD        │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Tabla de Métricas
```
┌────────────────────────────────────┬─────────────┐
│ Metric                             │ Value │ Status
├────────────────────────────────────┼─────────────┤
│ Average Wait Time                  │ 2.30s │ ✅
│ Average Service Time               │ 5.12s │ ✅
│ Customers Served                   │ 432   │ ✅
│ System Utilization                 │ 78%   │ ✅
│ ...                                │ ...   │ ...
└────────────────────────────────────┴─────────────┘
```

### Gráficas de Barras
```
Wait Time      ████████░░░░░░░░░░░░░░ 2.3s
Service Time   ████████████░░░░░░░░░░░░ 5.1s
Utilization    ███████████░░░░░░░░░░░░░ 78%
Rejection Rate ██░░░░░░░░░░░░░░░░░░░░░░ 2%
```

---

## 🟢 ¿Cómo Saber si está Todo Bien?

✅ **Verde/Bueno**:
- Tiempos de espera < 5 segundos
- Tasa de servicio > 0.9
- Pocos rechazos (< 5%)
- Utilización 60-80%

🟡 **Amarillo/Moderado**:
- Tiempos de espera 5-15 segundos
- Utilización 80-95%
- Algunos rechazos

🔴 **Rojo/Malo**:
- Tiempos de espera > 15 segundos
- Alta tasa de rechazo (> 10%)
- Utilización > 95%

---

## 💡 Recomendaciones del Sistema

El sistema automáticamente sugiere:

- "Tiempos de espera altos: considera agregar ventanillas"
- "Tasa de rechazo alta: aumenta capacidad de cola"
- "Sistema saturado: reduce λ o aumenta ventanillas"
- "Sistema funcionando bien: parámetros óptimos"

---

## 🐛 Si Algo No Funciona

### ❌ "Backend not responding"
```bash
# Asegúrate que el backend está corriendo
cd backend
python main.py
# Debe mostrar: Running on http://127.0.0.1:5000
```

### ❌ "Cannot find module"
```bash
# Instala dependencias
cd frontend
npm install
```

### ❌ "Validation error"
- Verifica los valores estén en rangos permitidos
- Los números negativos no son válidos
- Los campos vacíos se rechazarán

### ❌ "Simulation stuck at X%"
- Es normal que tome tiempo
- No cierres la ventana del navegador
- Frontend monitorea automáticamente
- Espera a que complete

---

## 📁 Archivos Clave del Proyecto

```
SimulationBank/
├── backend/
│   ├── main.py ............................ Punto entrada API
│   └── src/
│       └── simulation/
│           └── infrastructure/
│               ├── simulation_controller.py ... Controlador
│               └── simulation_blueprint.py ... Endpoints
│
└── frontend/
    ├── src/
    │   ├── App.jsx ........................ Componente raíz
    │   ├── App.css ....................... Estilos completos
    │   └── simulation/
    │       ├── components/
    │       │   ├── ConfigForm.jsx ....... Formulario
    │       │   ├── SimulationPanel.jsx . Orquestador
    │       │   ├── MetricsChart.jsx ... Visualización
    │       │   └── StatusIndicator.jsx . Indicador
    │       └── services/
    │           └── simulationService.js  Comunicación API
    |
    └── EPIC_4_IMPLEMENTATION.md ........ Documentación completa
    └── EPIC_4_CHANGES.md .............. Cambios realizados
    └── EPIC_4_SUMMARY.md .............. Este archivo
```

---

## 🔌 API Endpoints Disponibles

```javascript
// Todos estos endpoints funcionan:

// 1. Health Check
GET http://localhost:5000/
// { "status": "Simulation Bank API..." }

// 2. Configuración por defecto
GET http://localhost:5000/api/config/defaults
// { "defaults": {...}, "limits": {...} }

// 3. Iniciar simulación
POST http://localhost:5000/api/simulation/start
// Body: { "num_tellers": 3, "arrival_rate": 1.5, ... }
// { "simulation_id": "sim-xxxxx", "status": "initializing" }

// 4. Obtener estado
GET http://localhost:5000/api/simulation/state/sim-xxxxx
// { "status": "running", "progress": 45.5 }

// 5. Obtener resultados
GET http://localhost:5000/api/simulation/results/sim-xxxxx
// { "metrics": {...}, "total_time": 3600 }

// 6. Reporte de métricas
GET http://localhost:5000/api/metrics/report/sim-xxxxx
// { "average_wait_time": 2.3, ... }
```

---

## 🎓 Conceptos Principales

### Parámetros M/M/c

La simulación usa modelo de colas M/M/c:
- **M** = Llegadas exponenciales (λ)
- **M** = Servicio exponencial (μ)
- **c** = Número de servidores (ventanillas)

### Variables Monitoreadas

- **λ (Lambda)**: Tasa de llegadas
- **μ (Mu)**: Tasa de servicio
- **N**: Clientes en sistema
- **Nq**: Clientes esperando en cola
- **Nw**: Clientes siendo servidos

### Métricas Calculadas

- **Lq**: Longitud media de cola
- **L**: Longitud media del sistema
- **Wq**: Tiempo medio en cola
- **W**: Tiempo medio en sistema
- **ρ**: Factor de utilización

---

## ⏱️ Tiempos Típicos

Para horizonte de 8 horas:
- ⚡ Simulación pequeña (3 tellers): ~5-10 segundos
- ⏱️ Simulación mediana (5 tellers): ~15-30 segundos
- 🕐 Simulación grande (10 tellers): ~40-60 segundos

---

## 🎯 Flujo Típico de Uso

1. **Abre aplicación**
   - Verificar conexión con backend ✓
   - Cargar valores por defecto ✓

2. **Configura parámetros**
   - Ajusta según necesidad
   - Validación automática en tiempo real

3. **Inicia simulación**
   - Click "Start Simulation"
   - Ver barra de progreso

4. **Espera complemente**
   - Monitoreo automático cada 500ms
   - No cierre navegador

5. **Analiza resultados**
   - Revisa KPIs
   - Lee tabla de métricas
   - Observa gráficas
   - Lee recomendaciones

6. **Itera**
   - Click "Start New Simulation"
   - Prueba con parámetros diferentes
   - Compara resultados

---

## 📞 Información Técnica

- **Framework Backend**: Flask (Python)
- **Framework Frontend**: React (JavaScript)
- **Comunicación**: REST API (HTTP)
- **Estilos**: CSS3 (Responsive)
- **Threading**: Python threading (simulación asíncrona)
- **Polling**: JavaScript fetch cada 500ms

---

## ✅ Garantías

- ✅ Validación fuerte en formulario
- ✅ Manejo robusto de errores
- ✅ No bloquea interfaz durante simulación
- ✅ Comunicación segura HTTP
- ✅ Resultados precisos y reproducibles
- ✅ UI profesional y moderna
- ✅ Funciona en móviles y tablets
- ✅ Documentación completa

---

## 🚀 ¡Estás Listo!

Tu aplicación Simulation Bank está **100% funcional** y lista para:

✅ Ejecutar simulaciones de colas bancarias
✅ Analizar parámetros M/M/c
✅ Visualizar resultados en tiempo real
✅ Tomar decisiones informadas

---

**¿Preguntas?** Ver `EPIC_4_IMPLEMENTATION.md` para documentación completa.

**¿Bugs?** Revisa la consola del navegador (F12) para detalles de error.

---

_Épica 4: Interfaz de Usuario y Visualización_
_Responsable: parte-Leandro | Marzo 2026_
