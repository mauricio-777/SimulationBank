# Épica 4: Interfaz de Usuario y Visualización (Frontend) - Guía de Implementación

## 📋 Resumen de Implementación

Esta guía documenta la implementación completa de la **Épica 4: Interfaz de Usuario y Visualización**, que incluye:

- **Tarea 4.1**: Diseño de layout de la aplicación
- **Tarea 4.2**: Implementación del formulario de configuración  
- **Tarea 4.3**: Creación de componentes de gráficas
- **Tarea 4.4**: Conexión frontend ↔ backend vía API

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [App.jsx] → Health Check & Config Defaults              │
│       ↓                                                   │
│  [SimulationPanel] → Orquestador Principal              │
│       ├─→ [ConfigForm] → Entrada de Parámetros (4.2)    │
│       ├─→ [StatusIndicator] → Estado & Progreso        │
│       ├─→ [SimulationControls] → Botones Control       │
│       └─→ [MetricsChart] → Visualización (4.3)         │
│       │                                                   │
│       ↓                                                   │
│  [simulationService.js] → API Communication (4.4)       │
│                                                           │
└─────────────────────────────────────────────────────────┘
                           ↕ HTTP (REST API)
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (Python + Flask)                │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [main.py]                                              │
│  ├─→ GET / → Health Check                               │
│  ├─→ GET /api/config/defaults → Config por defecto     │
│  └─→ Registra Blueprints                               │
│                                                           │
│  [simulation_blueprint.py] → Endpoints Simulación       │
│  ├─→ POST /api/simulation/start → Inicia Simulación    │
│  ├─→ GET /api/simulation/state/<id> → Estado           │
│  └─→ GET /api/simulation/results/<id> → Resultados     │
│                                                           │
│  [simulation_controller.py] → Lógica de control         │
│  ├─→ Crea simulaciones                                  │
│  ├─→ Monitorea estado & progreso                        │
│  └─→ Retorna resultados finales                         │
│                                                           │
│  [metrics_blueprint.py] → Endpoints de Métricas         │
│  └─→ GET /api/metrics/report/<id> → Reporte Métricas   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Archivos Modificados

### Backend (Python)

```
backend/
├── main.py ★★★ MODIFICADO
│   ├── Endpoint Health Check
│   ├── Endpoint Config Defaults
│   └── Registro de Blueprint de Simulación
│
└── src/simulation/infrastructure/
    ├── simulation_controller.py ★★★ IMPLEMENTADO COMPLETO
    │   ├── start_simulation()
    │   ├── get_simulation_state()
    │   ├── get_simulation_results()
    │   └── _run_simulation_in_background()
    │
    └── simulation_blueprint.py ★★★ COMPLETADO
        ├── POST /api/simulation/start
        ├── GET /api/simulation/state/<id>
        └── GET /api/simulation/results/<id>
```

### Frontend (React)

```
frontend/src/
├── App.jsx ★★★ COMPLETAMENTE REESCRITO
│   ├── Health Check del Backend
│   ├── Carga Config Defaults
│   └── Renderiza SimulationPanel
│
├── App.css ★★★ ESTILOS COMPLETOS
│   ├── Variables CSS (colores, tamaños)
│   ├── Componentes Principal
│   ├── Layout Responsive
│   └── Dark Mode Support
│
├── index.css ★ ACTUALIZADO
│   └── Estilos Base Globales
│
└── simulation/
    ├── components/
    │   ├── ConfigForm.jsx ★★★ IMPLEMENTADO (Tarea 4.2)
    │   │   ├── Formulario con Validaciones
    │   │   ├── 5 Secciones de Configuración
    │   │   └── Feedback Visual Errores
    │   │
    │   ├── SimulationPanel.jsx ★★★ IMPLEMENTADO (Tarea 4.1)
    │   │   ├── Orquestador Principal
    │   │   ├── Layout 2 Columnas
    │   │   └── Gestión de Estado Global
    │   │
    │   ├── StatusIndicator.jsx ★★★ IMPLEMENTADO
    │   │   ├── Indicador Visual Estado
    │   │   ├── Barra de Progreso
    │   │   └── Iconos e Información
    │   │
    │   ├── SimulationControls.jsx ★ ESTRUCTURA BASE
    │   │   └── Componente para Futuros Controles
    │   │
    │   └── MetricsChart.jsx ★★★ IMPLEMENTADO (Tarea 4.3)
    │       ├── Grid de KPIs
    │       ├── Tabla de Métricas
    │       ├── Gráficas de Barras
    │       └── Insights & Recomendaciones
    │
    └── services/
        └── simulationService.js ★★★ IMPLEMENTADO (Tarea 4.4)
            ├── startSimulation()
            ├── getSimulationState()
            ├── getSimulationResults()
            ├── getDefaultConfiguration()
            └── getMetricsReport()
```

---

## 🚀 Cómo Usar la Aplicación

### 1. Instalar Dependencias

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Ejecutar el Backend

```bash
cd backend
python main.py
```

El servidor estará disponible en: `http://localhost:5000`

### 3. Ejecutar el Frontend

En otra terminal:
```bash
cd frontend
npm run dev
```

La aplicación estará disponible en: `http://localhost:5173` (o el puerto que muestre Vite)

### 4. Usar la Aplicación

1. **Abre el navegador** en `http://localhost:5173`
2. **Verifica la conexión**: La app mostrará un encabezado si todo está conectado
3. **Configura los parámetros**:
   - Número de ventanillas
   - Tasa de llegadas (λ)
   - Tiempo de servicio (μ)
   - Duración de la simulación
   - Capacidad máxima de cola
4. **Inicia la simulación**: Click en "Start Simulation"
5. **Monitorea el progreso**: Verás barra de progreso en tiempo real
6. **Visualiza resultados**: Una vez completa, verás gráficas y métricas

---

##  Detalles de Cada Tarea

### ✅ Tarea 4.1: Diseño de Layout

**Archivo Principal**: `frontend/src/App.jsx` y `frontend/src/simulation/components/SimulationPanel.jsx`

**Características Implementadas**:
- ✅ Panel de control con estructura clara (2 columnas)
- ✅ Área de entrada de parámetros (izquierda)
- ✅ Área de visualización de resultados (derecha)
- ✅ Encabezado profesional
- ✅ Indicador de conexión con backend
- ✅ Responsive design (funciona en móvil)

**Componentes del Layout**:
```
┌────────────────────────────────────────────┐
│             ENCABEZADO                      │
├────────────────┬──────────────────────────┤
│   FORMULARIO   │   ESTADO & RESULTADOS    │
│  (Izquierda)   │   (Derecha)              │
│                │                          │
│  • Ventanillas │  • StatusIndicator       │
│  • λ, μ, t     │  • MetricsChart          │
│  • Validación  │  • Tabla Detallada       │
│  • Botón Start │                          │
└────────────────┴──────────────────────────┘
```

### ✅ Tarea 4.2: Formulario de Configuración

**Archivo**: `frontend/src/simulation/components/ConfigForm.jsx`

**Características Implementadas**:
- ✅ 5 secciones de configuración (Tellers, Arrivals, Service, Duration, Advanced)
- ✅ Validaciones en tiempo real
- ✅ Mensajes de error claros
- ✅ Valores por defecto del backend
- ✅ Campos deshabilitados durante simulación
- ✅ Conversión automática de tiempo (seconds ↔ hh:mm)

**Parámetros Configurables**:
```javascript
{
  num_tellers: 3,              // Número de ventanillas (1-10)
  arrival_rate: 1.0,           // λ - Tasa de llegadas (0.1-10)
  service_mean: 5.0,           // μ - Tiempo promedio servicio (1-30s)
  max_time: 28800,             // Horizonte temporal (3600-86400s)
  max_queue_capacity: 100,     // Capacidad máxima cola (1+)
  priority_weights: [0.1, 0.3, 0.6],  // Pesos de prioridades
  service_dist: "exponential", // Distribución servicio
  arrival_dist: "exponential"  // Distribución llegadas
}
```

### ✅ Tarea 4.3: Componentes de Gráficas

**Archivo**: `frontend/src/simulation/components/MetricsChart.jsx`

**Características Implementadas**:
- ✅ **Grid de KPIs**: 5 tarjetas principales con métricas clave
- ✅ **Tabla de Métricas**: Todos los datos en formato tabular
- ✅ **Gráficas de Barras**: Visualización de 5 principales métricas
- ✅ **Indicadores de Salud**: Color verde (bueno), amarillo (moderado), rojo (malo)
- ✅ **Insights Inteligentes**: Recomendaciones basadas en resultados
- ✅ **Responsividad**: Funciona en todos los tamaños de pantalla

**Métricas Visualizadas**:
- Average wait time
- Average service time
- Customers served
- Customers rejected
- System utilization
- Por cada prioridad (Low, Medium, High)

### ✅ Tarea 4.4: Conexión Frontend ↔ Backend

**Archivo Principal**: `frontend/src/simulation/services/simulationService.js`

**Endpoints API Implementados**:

#### 1. **Health Check**
```
GET http://localhost:5000/
Respuesta: { status: "mensaje" }
```

#### 2. **Obtener Configuración por Defecto**
```
GET http://localhost:5000/api/config/defaults
Respuesta: {
  defaults: { num_tellers, arrival_rate, ... },
  limits: { min, max para cada parámetro }
}
```

#### 3. **Iniciar Simulación**
```
POST http://localhost:5000/api/simulation/start
Body: { num_tellers, arrival_rate, service_mean, ... }
Respuesta: {
  success: true,
  simulation_id: "sim-xxxxx",
  status: "initializing"
}
```

#### 4. **Obtener Estado de Simulación**
```
GET http://localhost:5000/api/simulation/state/{simulation_id}
Respuesta: {
  success: true,
  status: "running|completed|error",
  progress: 45.5,
  ...
}
```

#### 5. **Obtener Resultados Finales**
```
GET http://localhost:5000/api/simulation/results/{simulation_id}
Respuesta: {
  success: true,
  metrics: { average_wait_time, customers_served, ... },
  total_time: 3600
}
```

#### 6. **Obtener Reporte de Métricas**
```
GET http://localhost:5000/api/metrics/report/{simulation_id}
Respuesta: { Todas las métricas calculadas JSON }
```

---

## 💬 Notas Especiales sobre el Código

### Comentarios "parte-Leandro"

En cada archivo encontrarás comentarios detallados con el prefijo **"parte-Leandro"** que explican:

```javascript
// parte-Leandro: Explicación detallada en español de lo que hace esta sección
// Útil para mantener, debuggear y entender la lógica del código
```

Estos comentarios están en **ESPAÑOL** (para comprensión) mientras que el código está en **INGLÉS** (estándar industrial).

### Ejemplos:

**Backend (Python)**:
```python
# parte-Leandro: Función para ejecutar la simulación en un hilo separado.
# Este método:
# 1. Inicializa los componentes internos de la simulación
# 2. Ejecuta el motor de eventos discretos
# 3. Actualiza el estado de progreso
# 4. Captura cualquier error que ocurra durante la ejecución
def _run_simulation_in_background(self, simulation_id: str):
    ...
```

**Frontend (JavaScript)**:
```javascript
// parte-Leandro: Función auxiliar para hacer peticiones HTTP
// Maneja errores de red y respuestas no exitosas
async function fetchAPI(endpoint, options = {}) {
    ...
}
```

---

## 🔄 Flujo de Datos

### Flujo de Simulación Completo

```
1. Usuario abre App.jsx
   ↓
2. App.jsx verifica health check + carga config defaults
   ↓
3. Usuario ve formulario (ConfigForm)
   ↓
4. Usuario ingresa parámetros y valida
   ↓
5. Usuario click en "Start Simulation"
   ↓
6. ConfigForm llama a simulationService.startSimulation()
   ↓
7. Backend recibe POST y crea simulación en thread separado
   ↓
8. Frontend inicia loop de polling cada 500ms
   ↓
9. Cada polling: getSimulationState() → Actualiza barra progreso
   ↓
10. Simulación completada en backend
    ↓
11. Frontend llama getSimulationResults()
    ↓
12. MetricsChart visualiza los resultados
    ↓
13. Usuario ve gráficas, tablas e insights
```

---

## 📊 Monitoreo y Debugging

### Ver Logs del Backend

```bash
# En la terminal donde corre main.py
# Verás logs como:
127.0.0.1 - - [date] "POST /api/simulation/start HTTP/1.1" 201
127.0.0.1 - - [date] "GET /api/simulation/state/sim-xxxxx HTTP/1.1" 200
```

### Ver Logs del Frontend

Abre la consola del navegador (F12) → Tab "Console"

Las funciones manejan errores y logean:
```javascript
API Error: HTTP 404: Not Found
Error checking simulation state: ...
```

### Test Manual

```bash
# Test health check
curl http://localhost:5000/

# Test config defaults
curl http://localhost:5000/api/config/defaults

# Test iniciar simulación
curl -X POST http://localhost:5000/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{
    "num_tellers": 3,
    "arrival_rate": 1.5,
    "service_mean": 5.0,
    "max_time": 28800
  }'

# Test estado (reemplaza sim-xxxxx con ID recibido)
curl http://localhost:5000/api/simulation/state/sim-xxxxx

# Test resultados
curl http://localhost:5000/api/simulation/results/sim-xxxxx
```

---

## 🎨 Personalización de Estilos

Todos los colores y estilos se pueden personalizar en:

**`frontend/src/App.css`** - Variables CSS al inicio:

```css
:root {
  --primary-color: #2563eb;      /* Azul principal */
  --success-color: #16a34a;      /* Verde */
  --warning-color: #ea580c;      /* Naranja */
  --error-color: #dc2626;        /* Rojo */
  --info-color: #0284c7;         /* Cian */
  ...
}
```

---

## ⚡ Optimizaciones y Mejoras Futuras

### Implementado ✅
- [x] Validación de formulario en tiempo real
- [x] Polling cada 500ms para estado
- [x] Ejecución en thread separado (no bloquea API)
- [x] CORS habilitado para comunicación frontend-backend
- [x] Responsive design (mobile, tablet, desktop)
- [x] Manejo robusto de errores

### Posibles Mejoras Futuras
- [ ] WebSockets en lugar de polling (más eficiente)
- [ ] Gráfica en tiempo real con Chart.js o D3.js
- [ ] Exportar resultados a PDF/CSV
- [ ] Historial de simulaciones previas
- [ ] Pausa/Reanudación de simulaciones
- [ ] Comparación entre múltiples simulaciones
- [ ] análisis de sensibilidad (parámetros)
- [ ] Caché de configuraciones frecuentes
- [ ] Autenticación de usuarios
- [ ] Persistencia de datos en base de datos

---

## 🧪 Testing

### Test de Conexión

1. Abre navegador en `http://localhost:5173`
2. Deberías ver:
   - ✅ Encabezado "Simulation Bank - Discrete Event Simulation"
   - ✅ Formulario de configuración cargado
   - ✅ Valores por defecto rellenados

### Test de Simulación

1. Deja valores por defecto
2. Click "Start Simulation"
3. Deberías ver:
   - ✅ ID de simulación generado
   - ✅ Barra de progreso mostrando 0% → 100%
   - ✅ StatusIndicator cambiando de "initializing" → "running" → "completed"
   - ✅ Una vez al 100%, aparecen gráficas

### Test de Validación

1. Intenta poner número negativo en campos
2. Intenta enviar sin valores
3. Deberías ver:
   - ✅ Mensajes de error rojos bajo los campos
   - ✅ Botón deshabilitado
   - ✅ Input resaltado en rojo

---

## 📞 Contacto y Soporte

**Desarrollador**: parte-Leandro
**Épica**: 4 - Interfaz de Usuario y Visualización
**Tareas Incluidas**: 4.1, 4.2, 4.3, 4.4
**Fecha**: Marzo 2026

---

**¡Muchas gracias por revisar la implementación de la Épica 4!** 🚀
