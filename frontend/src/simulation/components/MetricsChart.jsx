/**
 * parte-Leandro: Componente para mostrar gráficas de métricas (Tarea 4.3)
 *
 * Muestra los resultados de la simulación con:
 * 1. Tiempos en formato legible (minutos y segundos)
 * 2. Porcentajes con contexto real (cuántas personas representan)
 * 3. Indicadores de estado (bueno / regular / malo)
 */
function MetricsChart({ metrics }) {

  // parte-Leandro: Convierte segundos a texto legible como "2 min 30 seg"
  const formatSeconds = (seconds) => {
    if (seconds < 60) {
      return `${seconds.toFixed(1)} seg`
    }
    const mins = Math.floor(seconds / 60)
    const secs = Math.round(seconds % 60)
    return secs > 0 ? `${mins} min ${secs} seg` : `${mins} min`
  }

  // parte-Leandro: Etiquetas amigables en español para cada clave del backend
  const friendlyLabels = {
    'tiempo_espera_promedio':                  'Tiempo Promedio de Espera en Cola',
    'tiempo_servicio_promedio':                'Tiempo Promedio de Atención',
    'clientes_atendidos':                      'Clientes Atendidos',
    'clientes_rechazados':                     'Clientes Rechazados',
    'utilizacion_ventanillas_porcentaje':      'Ocupación de Ventanillas',
    'max_cola':                                'Pico Máximo de la Cola',
    'promedio_cola':                           'Promedio de Personas en Cola',
    'tasa_procesamiento_clientes_por_segundo': 'Velocidad de Atención',
    'porcentaje_abandono':                     'Porcentaje de Abandono',
    'total_servidos':                          'Total de Clientes Atendidos',
    'total_rechazados':                        'Total de Clientes Rechazados',
  }

  const getLabel = (key) =>
    friendlyLabels[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())

  // parte-Leandro: Genera el valor formateado + texto interpretativo según el tipo de métrica
  const getFormattedValue = (key, value) => {
    const totalClientes = (metrics?.total_servidos || 0) + (metrics?.total_rechazados || 0)

    if (key === 'tiempo_espera_promedio') {
      return {
        display: formatSeconds(value),
        sub: `Cada cliente esperó en promedio ${formatSeconds(value)} antes de ser atendido.`
      }
    }
    if (key === 'tiempo_servicio_promedio') {
      return {
        display: formatSeconds(value),
        sub: `Cada atención en ventanilla duró en promedio ${formatSeconds(value)}.`
      }
    }
    if (key === 'utilizacion_ventanillas_porcentaje') {
      const detail = value >= 95
        ? 'Las ventanillas estuvieron casi siempre ocupadas — el sistema está saturado.'
        : value >= 60
        ? 'Buen equilibrio: las ventanillas trabajaron la mayor parte del tiempo.'
        : 'Las ventanillas estuvieron poco ocupadas — hay más capacidad de la necesaria.'
      return { display: `${value.toFixed(1)}%`, sub: detail }
    }
    if (key === 'porcentaje_abandono') {
      const rechazados = metrics?.total_rechazados || 0
      const atendidos = metrics?.total_servidos || 0
      return {
        display: `${value.toFixed(1)}%`,
        sub: `De ${totalClientes} personas que llegaron, ${rechazados} no pudieron ser atendidas (cola llena) y ${atendidos} sí fueron atendidas.`
      }
    }
    if (key === 'clientes_atendidos' || key === 'total_servidos') {
      const pct = totalClientes > 0 ? ((value / totalClientes) * 100).toFixed(1) : 0
      return {
        display: `${value} personas`,
        sub: `${pct}% de todos los clientes que llegaron al banco.`
      }
    }
    if (key === 'clientes_rechazados' || key === 'total_rechazados') {
      const pct = totalClientes > 0 ? ((value / totalClientes) * 100).toFixed(1) : 0
      return {
        display: `${value} personas`,
        sub: `${pct}% de los clientes no pudo ser atendido porque la cola estaba al máximo.`
      }
    }
    if (key === 'max_cola') {
      return {
        display: `${value} personas`,
        sub: `En el peor momento del día, ${value} personas estaban esperando al mismo tiempo en la fila.`
      }
    }
    if (key === 'promedio_cola') {
      return {
        display: `${value.toFixed(1)} personas`,
        sub: `En promedio, había ${value.toFixed(1)} personas esperando en la fila durante la simulación.`
      }
    }
    if (key === 'tasa_procesamiento_clientes_por_segundo') {
      const porMinuto = (value * 60).toFixed(2)
      return {
        display: `${value.toFixed(4)} cl/s`,
        sub: `El banco procesó aproximadamente ${porMinuto} clientes por minuto en promedio.`
      }
    }
    if (key.includes('porcentaje')) {
      return { display: `${value.toFixed(2)}%`, sub: '' }
    }
    if (key.includes('tiempo')) {
      return { display: formatSeconds(value), sub: '' }
    }
    return { display: Number.isInteger(value) ? `${value}` : value.toFixed(2), sub: '' }
  }

  // parte-Leandro: Semáforo de estado (bueno, regular, malo) según tipo y umbral de la métrica
  const getMetricStatus = (key, value) => {
    if (typeof value !== 'number') return 'metric-neutral'
    if (key === 'tiempo_espera_promedio') {
      if (value < 60) return 'metric-good'
      if (value < 300) return 'metric-moderate'
      return 'metric-poor'
    }
    if (key === 'utilizacion_ventanillas_porcentaje') {
      if (value > 60 && value < 95) return 'metric-good'
      if (value >= 95) return 'metric-poor'
      return 'metric-moderate'
    }
    if (key === 'porcentaje_abandono') {
      if (value < 5) return 'metric-good'
      if (value < 20) return 'metric-moderate'
      return 'metric-poor'
    }
    return 'metric-neutral'
  }

  const kpiKeys = [
    'tiempo_espera_promedio',
    'total_servidos',
    'total_rechazados',
    'utilizacion_ventanillas_porcentaje',
    'porcentaje_abandono',
  ]

  const tableKeys = [
    'max_cola',
    'promedio_cola',
    'tasa_procesamiento_clientes_por_segundo',
    'tiempo_espera_promedio',
    'utilizacion_ventanillas_porcentaje',
    'porcentaje_abandono',
    'total_servidos',
    'total_rechazados',
  ]

  const statusMap = {
    'metric-good': 'BUENO',
    'metric-moderate': 'REGULAR',
    'metric-poor': 'MALO',
    'metric-neutral': 'NEUTRO'
  }

  const totalClientes = (metrics?.total_servidos || 0) + (metrics?.total_rechazados || 0)

  return (
    <div className="metrics-chart">

      {/* parte-Leandro: Tarjetas KPI principales */}
      <section className="metrics-section kpi-section">
        <h4>Indicadores Clave</h4>
        <div className="metrics-grid kpi-grid">
          {kpiKeys.map(key => {
            const value = metrics?.[key]
            if (value === undefined || value === null) return null
            const status = getMetricStatus(key, value)
            const { display, sub } = getFormattedValue(key, value)
            return (
              <div key={key} className={`kpi-card ${status}`}>
                <span className="kpi-label">{getLabel(key)}</span>
                <span className="kpi-value">{display}</span>
                {sub && (
                  <span className="kpi-info" style={{ display: 'block', fontSize: '0.76rem', marginTop: '8px', opacity: 0.85, lineHeight: '1.4' }}>
                    {sub}
                  </span>
                )}
              </div>
            )
          })}
        </div>
      </section>

      {/* parte-Leandro: Tabla detallada con interpretación de cada métrica */}
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
            {tableKeys.map(key => {
              const value = metrics?.[key]
              if (value === undefined || value === null) return null
              const status = getMetricStatus(key, value)
              const { display, sub } = getFormattedValue(key, value)
              return (
                <tr key={key} className={`metric-row ${status}`}>
                  <td className="metric-name">
                    <strong>{getLabel(key)}</strong>
                    {sub && (
                      <span style={{ display: 'block', fontSize: '0.78rem', opacity: 0.75, marginTop: '4px', lineHeight: '1.4' }}>
                        {sub}
                      </span>
                    )}
                  </td>
                  <td className="metric-value" style={{ fontWeight: 'bold', fontSize: '1.05rem' }}>{display}</td>
                  <td className="metric-status">
                    <span className={`status-badge ${status}`}>{statusMap[status] || 'NEUTRO'}</span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>

      {/* parte-Leandro: Conclusiones generadas automáticamente según los datos */}
      <section className="metrics-section insights-section">
        <h4>Conclusiones y Recomendaciones</h4>
        <div className="insights-content">
          <ul>
            {metrics?.tiempo_espera_promedio > 300 && (
              <li className="insight-warning">
                ⚠️ <strong>Tiempos de espera muy altos:</strong> Los clientes esperaron en promedio {formatSeconds(metrics.tiempo_espera_promedio)}. Se recomienda añadir más ventanillas.
              </li>
            )}
            {metrics?.tiempo_espera_promedio > 60 && metrics?.tiempo_espera_promedio <= 300 && (
              <li className="insight-warning">
                ⚠️ <strong>Tiempos de espera moderados:</strong> El promedio de {formatSeconds(metrics.tiempo_espera_promedio)} podría mejorar con una ventanilla adicional.
              </li>
            )}
            {metrics?.porcentaje_abandono > 20 && (
              <li className="insight-warning">
                ⚠️ <strong>Alta tasa de abandono ({metrics.porcentaje_abandono.toFixed(1)}%):</strong> {metrics.total_rechazados} clientes se fueron sin ser atendidos. Aumenta la capacidad de la cola o añade ventanillas.
              </li>
            )}
            {metrics?.utilizacion_ventanillas_porcentaje >= 95 && (
              <li className="insight-warning">
                ⚠️ <strong>Sistema saturado ({metrics.utilizacion_ventanillas_porcentaje.toFixed(1)}% de ocupación):</strong> Las ventanillas están activas casi todo el tiempo y no pueden manejar picos de demanda.
              </li>
            )}
            {metrics?.tiempo_espera_promedio <= 60 && metrics?.porcentaje_abandono <= 5 && (
              <li className="insight-success">
                ✅ <strong>Excelente rendimiento:</strong> Espera promedio de {formatSeconds(metrics.tiempo_espera_promedio)} y solo {metrics.total_rechazados} clientes rechazados. El sistema funciona de forma óptima.
              </li>
            )}
            <li className="insight-info">
              ℹ️ <strong>Resumen general:</strong> De un total de {totalClientes} clientes simulados, <strong>{metrics?.total_servidos || 0} fueron atendidos</strong> y <strong>{metrics?.total_rechazados || 0} no pudieron ser atendidos</strong> por cola llena.
            </li>
          </ul>
        </div>
      </section>
    </div>
  )
}

export default MetricsChart