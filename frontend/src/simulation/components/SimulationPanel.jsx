import { useState } from 'react'
import ConfigForm from './ConfigForm'
import SimulationControls from './SimulationControls'
import StatusIndicator from './StatusIndicator'
import MetricsChart from './MetricsChart'
import { startSimulation, getSimulationState, getSimulationResults } from '../services/simulationService'

/**
 * parte-Leandro: Componente principal del panel de simulación (Tarea 4.1 - Layout)
 * 
 * Este es el contenedor principal que coordina toda la interfaz de usuario.
 * Estructura del layout:
 * 1. Panel de configuración (ConfigForm) - izquierda o arriba
 * 2. Área de visualización de resultados - derecha o abajo
 * 3. Indicadores de estado - en la parte superior
 * 4. Controles de simulación - en la parte inferior
 * 5. Gráficas de resultados - cuando la simulación está completa
 * 
 * Responsabilidades:
 * 1. Gestionar el estado global de la simulación
 * 2. Coordinar entre el formulario de configuración y los resultados
 * 3. Comunicarse con el backend vía API
 * 4. Mostrar estado de progreso durante la simulación
 * 5. Mostrar resultados y gráficas cuando termina
 */
function SimulationPanel({ defaultConfig }) {
  // parte-Leandro: Estado para almacenar el ID de la simulación en curso
  const [currentSimulationId, setCurrentSimulationId] = useState(null)

  // parte-Leandro: Estado para almacenar el estado actual de la simulación
  // Valores posibles: null, 'initializing', 'running', 'completed', 'error'
  const [simulationStatus, setSimulationStatus] = useState(null)

  // parte-Leandro: Estado para almacenar el progreso de la simulación (0-100%)
  const [simulationProgress, setSimulationProgress] = useState(0)

  // parte-Leandro: Estado para almacenar los resultados de la simulación completada
  const [results, setResults] = useState(null)

  // parte-Leandro: Estado para mostrar mensajes de error
  const [error, setError] = useState(null)

  // parte-Leandro: Estado para indicar si hay un envío en progreso
  const [isSubmitting, setIsSubmitting] = useState(false)

  /**
   * parte-Leandro: Manejador para cuando el usuario envía el formulario de configuración
   * Este método:
   * 1. Envía la configuración al backend vía API
   * 2. Obtiene un ID de simulación
   * 3. Inicia un intervalo para monitorear el progreso
   * 4. Muestra el estado en la interfaz
   */
  const handleConfigSubmit = async (configData) => {
    setIsSubmitting(true)
    setError(null)
    setResults(null)

    try {
      // parte-Leandro: Llamar al servicio para iniciar la simulación en el backend
      const response = await startSimulation(configData)

      if (!response.success) {
        throw new Error(response.error || 'Fallo al iniciar simulación')
      }

      // parte-Leandro: Guardar el ID de la simulación
      const simId = response.simulation_id
      setCurrentSimulationId(simId)
      setSimulationStatus(response.status)
      setSimulationProgress(0)

      // parte-Leandro: Iniciar un intervalo para monitorear el estado de la simulación
      // Se verifica cada 500ms para actualizar el progreso
      const statusCheckInterval = setInterval(async () => {
        try {
          // parte-Leandro: Obtener el estado actual de la simulación
          const stateResponse = await getSimulationState(simId)

          if (stateResponse.success) {
            setSimulationStatus(stateResponse.status)
            setSimulationProgress(stateResponse.progress || 0)

            // parte-Leandro: Si la simulación se completó, detener el intervalo y obtener los resultados
            if (stateResponse.status === 'completed') {
              clearInterval(statusCheckInterval)

              // parte-Leandro: Esperar un poco antes de obtener los resultados
              // (para asegurar que todas las métricas estén calculadas)
              setTimeout(async () => {
                try {
                  const resultsResponse = await getSimulationResults(simId)
                  if (resultsResponse.success) {
                    setResults(resultsResponse.metrics || resultsResponse)
                  }
                } catch (err) {
                  console.error('Error fetching results:', err)
                }
              }, 500)
            }

            // parte-Leandro: Si hay error, detener el intervalo
            if (stateResponse.status === 'error') {
              clearInterval(statusCheckInterval)
              setError(stateResponse.error || 'Ocurrió un error en la simulación')
            }
          }
        } catch (err) {
          console.error('Error checking simulation state:', err)
          // Continuar intentando aunque haya error en esta iteración
        }
      }, 500)

      // parte-Leandro: Limpiar el intervalo si el usuario navega fuera del componente
      return () => clearInterval(statusCheckInterval)

    } catch (err) {
      setError(err.message || 'Fallo al iniciar simulación')
      setIsSubmitting(false)
    } finally {
      setIsSubmitting(false)
    }
  }

  /**
   * parte-Leandro: Manejador para resetear la simulación y volver al formulario
   */
  const handleReset = () => {
    setCurrentSimulationId(null)
    setSimulationStatus(null)
    setSimulationProgress(0)
    setResults(null)
    setError(null)
  }

  // parte-Leandro: Renderizar el layout principal en dos columnas
  // Columna izquierda: Formulario de configuración
  // Columna derecha: Estado, progreso y resultados
  return (
    <div className="simulation-panel">
      {/* parte-Leandro: Mostrar error si ocurrió alguno */}
      {error && (
        <div className="error-box">
          <p>{error}</p>
          <button onClick={() => setError(null)}>Cerrar</button>
        </div>
      )}

      {/* parte-Leandro: Diseño en dos columnas para mejor presentación */}
      <div className="panel-layout">
        {/* parte-Leandro: Columna izquierda - Formulario de configuración o controles */}
        <div className="panel-left">
          {!currentSimulationId ? (
            // parte-Leandro: Si no hay simulación en curso, mostrar formulario de configuración
            <ConfigForm
              defaultConfig={defaultConfig}
              onSubmit={handleConfigSubmit}
              isLoading={isSubmitting}
            />
          ) : (
            // parte-Leandro: Si hay simulación en curso, mostrar información y controles
            <div className="simulation-info">
              <h3>Simulación Activa</h3>
              <div className="info-box">
                <p><strong>ID de Simulación:</strong> {currentSimulationId}</p>
                <p><strong>Estado:</strong> {simulationStatus}</p>
              </div>

              {/* parte-Leandro: Mostrar botón para volver al formulario si la simulación terminó */}
              {simulationStatus === 'completed' && (
                <button className="reset-button" onClick={handleReset}>
                  Iniciar Nueva Simulación
                </button>
              )}
            </div>
          )}
        </div>

        {/* parte-Leandro: Columna derecha - Estado, progreso y resultados */}
        <div className="panel-right">
          {currentSimulationId && (
            <>
              {/* parte-Leandro: Indicador de estado de la simulación */}
              <StatusIndicator
                status={simulationStatus}
                progress={simulationProgress}
              />

              {/* parte-Leandro: Mostrar gráficas de resultados si la simulación está completa */}
              {simulationStatus === 'completed' && results && (
                <div className="results-section">
                  <h3>Resultados de la Simulación</h3>
                  <MetricsChart metrics={results} />
                </div>
              )}

              {/* parte-Leandro: Mostrar tabla de detalles de resultados si están disponibles */}
              {results && (
                <div className="metrics-details">
                  <h4>Métricas Detalladas</h4>
                  <div className="metrics-grid">
                    {Object.entries(results).map(([key, value]) => {
                      // Saltar la clave 'success' que no es una métrica
                      if (key === 'success') return null

                      // Formatear la visualización del valor
                      let displayValue = value
                      if (typeof value === 'number') {
                        displayValue = value.toFixed(2)
                      }

                      return (
                        <div key={key} className="metric-item">
                          <span className="metric-label">{key.replace(/_/g, ' ').toUpperCase()}</span>
                          <span className="metric-value">{displayValue}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default SimulationPanel
