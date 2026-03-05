/**
 * parte-Leandro: Servicio de comunicación con el backend (Tarea 4.4)
 * 
 * Este módulo encapsula toda la comunicación HTTP con el servidor backend.
 * Proporciona funciones para:
 * 1. Iniciar simulaciones (POST /api/simulation/start)
 * 2. Obtener estado de simulación (GET /api/simulation/state/<id>)
 * 3. Obtener resultados finales (GET /api/simulation/results/<id>)
 * 4. Obtener configuración por defecto (GET /api/config/defaults)
 * 
 * Todas las funciones retornan promesas y manejan errores de forma consistente.
 */

// parte-Leandro: URL base del servidor backend
// En desarrollo: http://localhost:5000
// En producción: se debería obtener de variables de entorno
const API_BASE_URL = 'http://localhost:5000'

/**
 * parte-Leandro: Función auxiliar para hacer peticiones HTTP
 * Maneja errores de red y respuestas no exitosas
 * 
 * @param {string} endpoint - La ruta del endpoint (ej: '/api/simulation/start')
 * @param {object} options - Opciones de fetch (método, body, headers, etc.)
 * @returns {Promise} - La respuesta parseada como JSON
 */
async function fetchAPI(endpoint, options = {}) {
  try {
    // parte-Leandro: Construir URL completa del API
    const url = `${API_BASE_URL}${endpoint}`

    // parte-Leandro: Agregar headers por defecto si no se especifican
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    }

    // parte-Leandro: Hacer la petición fetch
    const response = await fetch(url, { ...defaultOptions, ...options })

    // parte-Leandro: Parsear la respuesta como JSON
    const data = await response.json()

    // parte-Leandro: Si la respuesta HTTP no fue exitosa, lanzar error
    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`)
    }

    return data

  } catch (error) {
    // parte-Leandro: Propagar el error con contexto adicional
    console.error(`API Error: ${error.message}`)
    throw error
  }
}

/**
 * parte-Leandro: Inicia una nueva simulación en el backend
 * 
 * Envía la configuración de simulación al servidor y recibe un ID único
 * para el seguimiento de esa simulación en particular.
 * 
 * @param {object} config - Objeto con los parámetros de configuración
 * @returns {Promise<object>} - Respuesta con simulation_id y estado inicial
 */
export async function startSimulation(config) {
  return fetchAPI('/api/simulation/start', {
    method: 'POST',
    body: JSON.stringify(config)
  })
}

/**
 * parte-Leandro: Obtiene el estado actual de una simulación en ejecución
 * 
 * Este endpoint es usado para monitorear el progreso de la simulación.
 * Se puede consultar repetidamente para obtener actualizaciones del estado.
 * 
 * @param {string} simulationId - ID de la simulación a consultar
 * @returns {Promise<object>} - Objeto con estado actual y progreso (0-100%)
 */
export async function getSimulationState(simulationId) {
  return fetchAPI(`/api/simulation/state/${simulationId}`, {
    method: 'GET'
  })
}

/**
 * parte-Leandro: Obtiene los resultados completos de una simulación completada
 * 
 * Solo funciona si la simulación ha terminado (status = 'completed').
 * Retorna todas las métricas calculadas por la simulación.
 * 
 * @param {string} simulationId - ID de la simulación
 * @returns {Promise<object>} - Objeto con todas las métricas y resultados
 */
export async function getSimulationResults(simulationId) {
  return fetchAPI(`/api/simulation/results/${simulationId}`, {
    method: 'GET'
  })
}

/**
 * parte-Leandro: Obtiene la configuración por defecto del sistema
 * 
 * El frontend consulta este endpoint al cargar para obtener valores
 * por defecto y límites permitidos para los campos del formulario.
 * 
 * @returns {Promise<object>} - Objeto con defaults y limits
 */
export async function getDefaultConfiguration() {
  return fetchAPI('/api/config/defaults', {
    method: 'GET'
  })
}

/**
 * parte-Leandro: Obtiene el reporte de métricas de una simulación
 * 
 * Este es un endpoint alternativo para obtener métricas si es necesario
 * (versión alternativa a getSimulationResults).
 * 
 * @param {string} simulationId - ID de la simulación
 * @returns {Promise<object>} - Objeto con todas las métricas detalladas
 */
export async function getMetricsReport(simulationId) {
  return fetchAPI(`/api/metrics/report/${simulationId}`, {
    method: 'GET'
  })
}