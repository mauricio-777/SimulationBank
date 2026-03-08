/**
 * parte-Leandro: Componente para mostrar gráficas de métricas (Tarea 4.3)
 * 
 * Este componente visualiza los resultados de la simulación en formato gráfico.
 * Actualmente muestra:
 * 1. Tabla de métricas principales
 * 2. Gráficas de barras para comparación
 * 3. Indicadores clave de rendimiento
 * 
 * En futuras versiones se puede integrar una librería como Chart.js o D3
 * para gráficas más avanzadas (líneas temporales, áreas, etc.)
 */
function MetricsChart({ metrics }) {
  /**
   * parte-Leandro: Función para formatear la llave de métrica a texto legible
   * Convierte 'average_wait_time' a 'Average Wait Time'
   */
  const formatMetricLabel = (key) => {
    return key
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  /**
   * parte-Leandro: Función para formatear valores numéricos
   * Si es un porcentaje, muestra con símbolo %
   * Si es un tiempo, muestra con decimales limitados
   */
  const formatMetricValue = (key, value) => {
    if (typeof value !== 'number') return value

    // Formatear según el tipo de métrica
    if (key.includes('tasa') || key.includes('porcentaje') || key.includes('probabilidad')) {
      return `${(value * 100).toFixed(2)}%`
    }

    if (key.includes('tiempo')) {
      return `${value.toFixed(2)}s`
    }

    return value.toFixed(2)
  }

  /**
   * parte-Leandro: Determinar si la métrica indica buen o mal rendimiento
   * Retorna una clase CSS para colorear la métrica
   */
  const getMetricStatus = (key, value) => {
    if (typeof value !== 'number') return 'metric-neutral'

    // parte-Leandro: Tiempos de espera bajos son buenos
    if (key.includes('espera')) {
      if (value < 5) return 'metric-good'
      if (value < 15) return 'metric-moderate'
      return 'metric-poor'
    }

    // parte-Leandro: Tasas de servicio altas son buenas
    if (key.includes('servicio') || key.includes('rendimiento')) {
      if (value > 0.9) return 'metric-good'
      if (value > 0.7) return 'metric-moderate'
      return 'metric-poor'
    }

    // parte-Leandro: Utilización moderada es ideal
    if (key.includes('utilizacion')) {
      if (value > 0.6 && value < 0.95) return 'metric-good'
      if (value > 0.4 && value < 1.0) return 'metric-moderate'
      return 'metric-poor'
    }

    return 'metric-neutral'
  }

  return (
    <div className="metrics-chart">
      {/* parte-Leandro: Sección de indicadores clave (KPIs) en vista de tarjetas */}
      <section className="metrics-section kpi-section">
        <h4>Indicadores Clave de Rendimiento</h4>
        <div className="metrics-grid kpi-grid">
          {/* parte-Leandro: Mostrar métricas principales en formato grande y destacado */}
          {metrics && Object.entries(metrics).map(([key, value]) => {
            // Saltar valores no numéricos y ciertas claves
            if (typeof value !== 'number' || key === 'success') return null

            // Mostrar solo métricas clave
            const keyMetrics = [
              'tiempo_espera_promedio',
              'tiempo_servicio_promedio',
              'clientes_atendidos',
              'clientes_rechazados',
              'utilizacion_ventanillas_porcentaje'
            ]

            if (!keyMetrics.some(km => key.includes(km))) return null

            const status = getMetricStatus(key, value)

            return (
              <div key={key} className={`kpi-card ${status}`}>
                <span className="kpi-label">{formatMetricLabel(key)}</span>
                <span className="kpi-value">{formatMetricValue(key, value)}</span>
                <span className="kpi-indicator"></span>
              </div>
            )
          })}
        </div>
      </section>

      {/* parte-Leandro: Sección de tabla de todas las métricas */}
      <section className="metrics-section table-section">
        <h4>Métricas Detalladas</h4>
        <table className="metrics-table">
          <thead>
            <tr>
              <th>Métrica</th>
              <th>Valor</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {/* parte-Leandro: Iterar sobre todas las métricas y mostrarlas en la tabla */}
            {metrics && Object.entries(metrics).map(([key, value]) => {
              // Saltar valores no numéricos, arreglos extensos (como historial) y ciertas claves especiales
              if (typeof value !== 'number' || key === 'success' || Array.isArray(value)) return null
              
              const status = getMetricStatus(key, value)
              const statusMap = {
                'metric-good': 'BUENO',
                'metric-moderate': 'REGULAR',
                'metric-poor': 'MALO',
                'metric-neutral': 'NEUTRO'
              };
              const statusLabel = statusMap[status] || 'NEUTRO';

              return (
                <tr key={key} className={`metric-row ${status}`}>
                  <td className="metric-name">{formatMetricLabel(key)}</td>
                  <td className="metric-value">{formatMetricValue(key, value)}</td>
                  <td className="metric-status">
                    <span className={`status-badge ${status}`}>{statusLabel}</span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>

      {/* parte-Leandro: Sección de gráfica de barras simple */}
      <section className="metrics-section chart-section">
        <h4>Gráfica de Rendimiento</h4>
        <div className="simple-chart">
          {/* parte-Leandro: Crear una visualización simple de barras horizontales */}
          {metrics && Object.entries(metrics)
            .filter(([key, value]) => typeof value === 'number' && !key.includes('count') && key !== 'success' && !Array.isArray(value))
            .slice(0, 5) // Mostrar solo las primeras 5 métricas para evitar saturación
            .map(([key, value]) => {
              // Normalizar valores a escala 0-100 para visualización
              let normalizedValue = value
              if (key.includes('tiempo')) {
                normalizedValue = Math.min((value / 30) * 100, 100) // Asumir máximo 30 segundos
              } else if (value <= 1) {
                normalizedValue = value * 100 // Si es porcentaje (0-1), convertir a 0-100
              }

              return (
                <div key={key} className="chart-bar-item">
                  <label>{formatMetricLabel(key)}</label>
                  <div className="bar-container">
                    <div
                      className="bar-fill"
                      style={{ width: `${Math.min(normalizedValue, 100)}%` }}
                    ></div>
                  </div>
                  <span className="bar-value">{formatMetricValue(key, value)}</span>
                </div>
              )
            })}
        </div>
      </section>

      {/* parte-Leandro: Sección de conclusiones y recomendaciones */}
      <section className="metrics-section insights-section">
        <h4>Conclusiones y Recomendaciones</h4>
        <div className="insights-content">
          {/* parte-Leandro: Generar recomendaciones basadas en las métricas */}
          <ul>
            {metrics && metrics.tiempo_espera_promedio > 10 && (
              <li className="insight-warning">
                ⚠️ <strong>Tiempos de espera altos detectados:</strong> Considera aumentar el número de ventanillas o mejorar la eficiencia del servicio.
              </li>
            )}

            {metrics && metrics.clientes_rechazados > metrics.clientes_atendidos * 0.1 && (
              <li className="insight-warning">
                ⚠️ <strong>La tasa de rechazo es alta:</strong> Aumenta la capacidad máxima de la cola o añade más ventanillas para reducir la pérdida de clientes.
              </li>
            )}

            {metrics && metrics.utilizacion_ventanillas_porcentaje > 0.95 && (
              <li className="insight-warning">
                ⚠️ <strong>El sistema está sobreutilizado:</strong> Considera añadir más ventanillas o reducir la tasa de llegada de clientes.
              </li>
            )}

            {metrics && metrics.tiempo_espera_promedio < 5 && metrics.utilizacion_ventanillas_porcentaje < 0.8 && (
              <li className="insight-success">
                ✅ <strong>El sistema está funcionando bien:</strong> Los tiempos de espera son bajos y la utilización del sistema es razonable.
              </li>
            )}

            <li className="insight-info">
              ℹ️ <strong>Resumen de la Simulación:</strong> Esta simulación se ejecutó con los parámetros que especificaste y recopiló métricas sobre el comportamiento de la cola, tiempos de servicio y eficiencia del sistema.
            </li>
          </ul>
        </div>
      </section>
    </div>
  )
}

export default MetricsChart