/**
 * parte-Leandro: Componente para mostrar gráficas de métricas (Tarea 4.3)
 *
 * Muestra los resultados de la simulación con:
 * 1. Tiempos en formato legible (minutos y segundos)
 * 2. Porcentajes con contexto real (cuántas personas representan)
 * 3. Diagnóstico adaptativo basado en la configuración real del usuario
 */
function MetricsChart({ metrics, config }) {

  // parte-Leandro: Convierte segundos a texto legible como "2 min 30 seg"
  const formatSeconds = (seconds) => {
    if (seconds < 60) return `${seconds.toFixed(1)} seg`
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

  // parte-Leandro: Genera el valor formateado + texto interpretativo
  const getFormattedValue = (key, value) => {
    const totalClientes = (metrics?.total_servidos || 0) + (metrics?.total_rechazados || 0)

    if (key === 'tiempo_espera_promedio') {
      return { display: formatSeconds(value), sub: `Cada cliente esperó en promedio ${formatSeconds(value)} antes de ser atendido.` }
    }
    if (key === 'tiempo_servicio_promedio') {
      return { display: formatSeconds(value), sub: `Cada atención en ventanilla duró en promedio ${formatSeconds(value)}.` }
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
      return { display: `${value} personas`, sub: `${pct}% de todos los clientes que llegaron al banco.` }
    }
    if (key === 'clientes_rechazados' || key === 'total_rechazados') {
      const pct = totalClientes > 0 ? ((value / totalClientes) * 100).toFixed(1) : 0
      return { display: `${value} personas`, sub: `${pct}% de los clientes no pudo ser atendido porque la cola estaba al máximo.` }
    }
    if (key === 'max_cola') {
      return { display: `${value} personas`, sub: `En el peor momento del día, ${value} personas estaban esperando al mismo tiempo.` }
    }
    if (key === 'promedio_cola') {
      return { display: `${value.toFixed(1)} personas`, sub: `En promedio, había ${value.toFixed(1)} personas esperando en la fila.` }
    }
    if (key === 'tasa_procesamiento_clientes_por_segundo') {
      const porMinuto = (value * 60).toFixed(2)
      return { display: `${value.toFixed(4)} cl/s`, sub: `El banco procesó aproximadamente ${porMinuto} clientes por minuto en promedio.` }
    }
    if (key.includes('porcentaje')) return { display: `${value.toFixed(2)}%`, sub: '' }
    if (key.includes('tiempo')) return { display: formatSeconds(value), sub: '' }
    return { display: Number.isInteger(value) ? `${value}` : value.toFixed(2), sub: '' }
  }

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

  const kpiKeys = ['tiempo_espera_promedio', 'total_servidos', 'total_rechazados', 'utilizacion_ventanillas_porcentaje', 'porcentaje_abandono']
  const tableKeys = ['max_cola', 'promedio_cola', 'tasa_procesamiento_clientes_por_segundo', 'tiempo_espera_promedio', 'utilizacion_ventanillas_porcentaje', 'porcentaje_abandono', 'total_servidos', 'total_rechazados']
  const statusMap = { 'metric-good': 'BUENO', 'metric-moderate': 'REGULAR', 'metric-poor': 'MALO', 'metric-neutral': 'NEUTRO' }
  const totalClientes = (metrics?.total_servidos || 0) + (metrics?.total_rechazados || 0)

  // ─────────────────────────────────────────────────────────────────────────
  // parte-Leandro: Diagnóstico adaptativo — calcula ρ con la config real
  // ─────────────────────────────────────────────────────────────────────────
  const buildDiagnosis = () => {
    if (!config) return null
    const lambda = parseFloat(config.arrival_rate) || 1.0
    const serviceMean = parseFloat(config.service_mean) || 5.0
    const mu = 1.0 / serviceMean
    const c = parseInt(config.num_tellers) || 3
    const rho = lambda / (c * mu)
    const tellersSolution = Math.ceil(lambda / (mu * 0.85))
    const tellersOptimal  = Math.ceil(lambda / (mu * 0.80))

    let scenario
    if (rho >= 1.5)       scenario = 'saturated'
    else if (rho >= 0.95) scenario = 'overloaded'
    else if (rho >= 0.70) scenario = 'optimal'
    else                  scenario = 'underutilized'

    return { rho, lambda, mu, serviceMean, c, tellersSolution, tellersOptimal, scenario }
  }

  const diagnosis = buildDiagnosis()

  const diagLabels = {
    saturated:     'Sistema Saturado',
    overloaded:    'Sistema Sobrecargado',
    optimal:       'Sistema Optimo',
    underutilized: 'Sistema Subutilizado',
  }

  return (
    <div className="metrics-chart">

      {/* ── DIAGNÓSTICO ADAPTATIVO ── */}
      {diagnosis && (
        <section className={`diagnosis-block diagnosis-${diagnosis.scenario}`}>
          <h4 className="diagnosis-title">
            Diagnostico: {diagLabels[diagnosis.scenario]}
          </h4>

          {/* Fórmula ρ con valores reales */}
          <div className="diagnosis-formula">
            <strong>Intensidad de Trafico (rho) = λ / (c × μ)</strong><br />
            = {diagnosis.lambda.toFixed(2)} llegadas/seg ÷ ({diagnosis.c} ventanillas × {diagnosis.mu.toFixed(3)} atenciones/seg)
            {' = '}
            <span className="diagnosis-rho-value">{diagnosis.rho.toFixed(3)}</span>
            <span className="diagnosis-formula-note">
              {diagnosis.rho >= 1
                ? `rho mayor o igual a 1: El banco recibe ${diagnosis.rho.toFixed(1)}x mas trabajo del que puede manejar. La cola crece hasta llenarse y rechazar clientes.`
                : `rho menor a 1: El sistema es estable. Las ventanillas pueden absorber toda la demanda.`}
            </span>
          </div>

          {/* Saturado */}
          {diagnosis.scenario === 'saturated' && (
            <div>
              <p className="diagnosis-text">
                <strong>Que esta pasando:</strong> Con solo {diagnosis.c} ventanilla(s) atendiendo a {diagnosis.lambda} cliente(s)/seg
                (cada uno tarda aproximadamente {diagnosis.serviceMean} seg), el sistema no da abasto.
                La cola se llena rapidamente y la mayoria de personas son rechazadas antes de ser atendidas.
              </p>
              <div className="diagnosis-card card-solution">
                <strong>Solucion minima para estabilizar el sistema:</strong>
                <ul>
                  <li>Aumentar a <strong>{diagnosis.tellersSolution} ventanillas</strong> (actualmente: {diagnosis.c})</li>
                  <li>Esto llevaria rho a aproximadamente 0.85, el banco puede manejar la demanda sin colapsar</li>
                  <li>Alternativa: reducir el tiempo de atencion por debajo de <strong>{(diagnosis.lambda / (diagnosis.c * 0.85)).toFixed(1)} seg</strong></li>
                </ul>
              </div>
              <div className="diagnosis-card card-optimal">
                <strong>Configuracion optima recomendada:</strong>
                <ul>
                  <li><strong>{diagnosis.tellersOptimal} ventanillas</strong>, lo que llevaría rho a aproximadamente 0.80</li>
                  <li>Los cajeros trabajan el 80% del tiempo, eficientes sin estar colapsados</li>
                  <li>Espera promedio estimada: baja (menos de 1 minuto) — Abandono estimado: menos del 2%</li>
                </ul>
              </div>
            </div>
          )}

          {/* Sobrecargado */}
          {diagnosis.scenario === 'overloaded' && (
            <div>
              <p className="diagnosis-text">
                <strong>Que esta pasando:</strong> El sistema funciona pero esta al limite (rho = {diagnosis.rho.toFixed(2)}).
                Cualquier pequeno pico de demanda puede saturarlo. Los tiempos de espera son elevados.
              </p>
              <div className="diagnosis-card card-optimal">
                <strong>Para llegar al optimo:</strong>
                <ul>
                  <li>Agrega <strong>{Math.max(1, diagnosis.tellersOptimal - diagnosis.c)} ventanilla(s) mas</strong> (total recomendado: {diagnosis.tellersOptimal})</li>
                  <li>Llevaria rho de {diagnosis.rho.toFixed(2)} a aproximadamente 0.80</li>
                  <li>Los tiempos de espera bajarian considerablemente</li>
                </ul>
              </div>
            </div>
          )}

          {/* Optimo */}
          {diagnosis.scenario === 'optimal' && (
            <div>
              <p className="diagnosis-text">
                <strong>Configuracion equilibrada.</strong> Con rho = {diagnosis.rho.toFixed(2)},
                las ventanillas trabajan el {(diagnosis.rho * 100).toFixed(0)}% del tiempo.
                Son eficientes sin saturarse ante picos de demanda.
              </p>
              <p className="diagnosis-text" style={{ opacity: 0.75, fontSize: '0.9rem' }}>
                Si los tiempos de espera siguen siendo altos a pesar de este rho, considera reducir el tiempo medio de atencion mediante digitalizacion de tramites.
              </p>
            </div>
          )}

          {/* Subutilizado */}
          {diagnosis.scenario === 'underutilized' && (
            <div>
              <p className="diagnosis-text">
                <strong>Capacidad ociosa.</strong> Con rho = {diagnosis.rho.toFixed(2)}, las ventanillas
                solo trabajan el {(diagnosis.rho * 100).toFixed(0)}% del tiempo.
                Tienes mas personal del necesario para la demanda actual.
              </p>
              <div className="diagnosis-card card-savings">
                <strong>Para optimizar costos sin sacrificar calidad:</strong>
                <ul>
                  <li>Podrias operar con solo <strong>{diagnosis.tellersOptimal} ventanillas</strong> (actualmente usas {diagnosis.c})</li>
                  <li>Eso mantendria rho en aproximadamente 0.80, excelente servicio con menos personal</li>
                  <li>Ahorro potencial: <strong>{diagnosis.c - diagnosis.tellersOptimal} ventanilla(s)</strong> innecesaria(s)</li>
                </ul>
              </div>
            </div>
          )}
        </section>
      )}

      {/* ── KPIs ── */}
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
                {sub && <span className="kpi-info" style={{ display: 'block', fontSize: '0.76rem', marginTop: '8px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>{sub}</span>}
              </div>
            )
          })}
        </div>
      </section>

      {/* ── Tabla detallada ── */}
      <section className="metrics-section table-section">
        <h4>Metricas Detalladas</h4>
        <table className="metrics-table">
          <thead>
            <tr>
              <th>Metrica</th>
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
                    {sub && <span style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: '1.4' }}>{sub}</span>}
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

      {/* ── Resumen general ── */}
      <section className="metrics-section insights-section">
        <h4>Resumen General</h4>
        <div className="insights-content">
          <ul>
            {metrics?.tiempo_espera_promedio > 300 && (
              <li className="insight-warning">
                <strong>Tiempos de espera muy altos:</strong> Los clientes esperaron en promedio {formatSeconds(metrics.tiempo_espera_promedio)}. Revisa el diagnostico de arriba.
              </li>
            )}
            {metrics?.porcentaje_abandono > 20 && (
              <li className="insight-warning">
                <strong>Alta tasa de abandono ({metrics.porcentaje_abandono.toFixed(1)}%):</strong> {metrics.total_rechazados} clientes se fueron sin ser atendidos.
              </li>
            )}
            {metrics?.tiempo_espera_promedio <= 60 && metrics?.porcentaje_abandono <= 5 && (
              <li className="insight-success">
                <strong>Excelente rendimiento:</strong> Espera de {formatSeconds(metrics.tiempo_espera_promedio)} y solo {metrics.total_rechazados} rechazados.
              </li>
            )}
            <li className="insight-info">
              <strong>Total:</strong> De {totalClientes} clientes simulados, <strong>{metrics?.total_servidos || 0} fueron atendidos</strong> y <strong>{metrics?.total_rechazados || 0} no pudieron ser atendidos</strong>.
            </li>
          </ul>
        </div>
      </section>

    </div>
  )
}

export default MetricsChart