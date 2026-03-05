import { useState, useEffect } from 'react'

/**
 * parte-Leandro: Componente de formulario para configuración de simulación (Tarea 4.2)
 * 
 * Este componente permite al usuario ingresar los parámetros de la simulación:
 * - Número de ventanillas (tellers)
 * - Tasa de llegadas (λ - arrival rate)
 * - Tiempo medio de servicio (μ - service mean)
 * - Duración total de la simulación (max time)
 * - Capacidad máxima de la cola
 * - Pesos de distribución de prioridades
 * 
 * Responsabilidades:
 * 1. Renderizar campos de entrada con valores por defecto
 * 2. Validar que los valores ingresados sean válidos (rangos, números positivos)
 * 3. Llamar al callback onSubmit cuando el usuario envía el formulario
 * 4. Mostrar feedback visual de validación
 */
function ConfigForm({ defaultConfig, onSubmit, isLoading }) {
  // parte-Leandro: Estado local para almacenar los valores del formulario
  const [formData, setFormData] = useState({
    num_tellers: defaultConfig?.defaults?.num_tellers || 3,
    arrival_rate: defaultConfig?.defaults?.arrival_rate || 1.0,
    service_mean: defaultConfig?.defaults?.service_mean || 5.0,
    max_time: defaultConfig?.defaults?.max_time || 28800,
    max_queue_capacity: defaultConfig?.defaults?.max_queue_capacity || 100,
    priority_weights: defaultConfig?.defaults?.priority_weights || [0.1, 0.3, 0.6],
    service_dist: defaultConfig?.defaults?.service_dist || 'exponential',
    arrival_dist: defaultConfig?.defaults?.arrival_dist || 'exponential'
  })

  // parte-Leandro: Estado para almacenar errores de validación
  const [errors, setErrors] = useState({})

  // parte-Leandro: Actualizar el formulario si cambian los valores por defecto
  useEffect(() => {
    if (defaultConfig?.defaults) {
      setFormData({
        num_tellers: defaultConfig.defaults.num_tellers,
        arrival_rate: defaultConfig.defaults.arrival_rate,
        service_mean: defaultConfig.defaults.service_mean,
        max_time: defaultConfig.defaults.max_time,
        max_queue_capacity: defaultConfig.defaults.max_queue_capacity,
        priority_weights: defaultConfig.defaults.priority_weights,
        service_dist: defaultConfig.defaults.service_dist,
        arrival_dist: defaultConfig.defaults.arrival_dist
      })
    }
  }, [defaultConfig])

  /**
   * parte-Leandro: Función para validar todos los campos del formulario
   * Verifica que:
   * - Los valores numéricos estén dentro de los rangos permitidos
   * - No haya campos vacíos
   * - Los valores sean números válidos
   */
  const validateForm = () => {
    const newErrors = {}
    const limits = defaultConfig?.limits || {}

    // parte-Leandro: Validar número de ventanillas
    if (formData.num_tellers < (limits.num_tellers_min || 1) || 
        formData.num_tellers > (limits.num_tellers_max || 10)) {
      newErrors.num_tellers = `Must be between ${limits.num_tellers_min || 1} and ${limits.num_tellers_max || 10}`
    }

    // parte-Leandro: Validar tasa de llegadas
    if (formData.arrival_rate < (limits.arrival_rate_min || 0.1) || 
        formData.arrival_rate > (limits.arrival_rate_max || 10.0)) {
      newErrors.arrival_rate = `Must be between ${limits.arrival_rate_min || 0.1} and ${limits.arrival_rate_max || 10.0}`
    }

    // parte-Leandro: Validar tiempo medio de servicio
    if (formData.service_mean < (limits.service_mean_min || 1.0) || 
        formData.service_mean > (limits.service_mean_max || 30.0)) {
      newErrors.service_mean = `Must be between ${limits.service_mean_min || 1.0} and ${limits.service_mean_max || 30.0}`
    }

    // parte-Leandro: Validar duración total de la simulación
    if (formData.max_time < (limits.max_time_min || 3600) || 
        formData.max_time > (limits.max_time_max || 86400)) {
      newErrors.max_time = `Must be between ${limits.max_time_min || 3600} and ${limits.max_time_max || 86400} seconds`
    }

    // parte-Leandro: Validar capacidad máxima de la cola
    if (formData.max_queue_capacity < 1) {
      newErrors.max_queue_capacity = 'Must be at least 1'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  /**
   * parte-Leandro: Manejador para cambios en los inputs de texto
   * Actualiza el estado del formulario cuando el usuario escribe
   */
  const handleInputChange = (e) => {
    const { name, value, type } = e.target
    
    // parte-Leandro: Convertir a número si es un campo numérico
    const processedValue = type === 'number' ? parseFloat(value) : value

    setFormData(prev => ({
      ...prev,
      [name]: processedValue
    }))

    // parte-Leandro: Limpiar el error del campo cuando el usuario empieza a escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined
      }))
    }
  }

  /**
   * parte-Leandro: Manejador para el envío del formulario
   * Valida todos los campos y llama a onSubmit si todo es correcto
   */
  const handleSubmit = (e) => {
    e.preventDefault()

    // parte-Leandro: Validar antes de enviar
    if (!validateForm()) {
      return
    }

    // parte-Leandro: Llamar al callback pasado como prop con los datos del formulario
    onSubmit(formData)
  }

  // parte-Leandro: Función auxiliar para convertir segundos a formato legible (horas, minutos)
  const formatTimeDisplay = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}h ${minutes}m`
  }

  return (
    <form className="config-form" onSubmit={handleSubmit}>
      <div className="form-title">
        <h2>Simulation Configuration</h2>
        <p>Enter the parameters for your bank simulation</p>
      </div>

      {/* parte-Leandro: Sección 1: Configuración de Ventanillas */}
      <fieldset className="form-section">
        <legend>Teller Configuration</legend>
        
        <div className="form-group">
          <label htmlFor="num_tellers">Number of Tellers (Servers)</label>
          <input
            id="num_tellers"
            name="num_tellers"
            type="number"
            min="1"
            max="10"
            value={formData.num_tellers}
            onChange={handleInputChange}
            disabled={isLoading}
            className={errors.num_tellers ? 'input-error' : ''}
          />
          {errors.num_tellers && <span className="error-message">{errors.num_tellers}</span>}
          <small>How many tellers are available to serve customers</small>
        </div>
      </fieldset>

      {/* parte-Leandro: Sección 2: Configuración de Llegadas */}
      <fieldset className="form-section">
        <legend>Arrival Configuration (λ - Lambda)</legend>
        
        <div className="form-group">
          <label htmlFor="arrival_rate">Arrival Rate (customers per time unit)</label>
          <input
            id="arrival_rate"
            name="arrival_rate"
            type="number"
            min="0.1"
            max="10"
            step="0.1"
            value={formData.arrival_rate}
            onChange={handleInputChange}
            disabled={isLoading}
            className={errors.arrival_rate ? 'input-error' : ''}
          />
          {errors.arrival_rate && <span className="error-message">{errors.arrival_rate}</span>}
          <small>Higher values mean more customers arrive per unit of time</small>
        </div>

        <div className="form-group">
          <label htmlFor="arrival_dist">Arrival Distribution</label>
          <select
            id="arrival_dist"
            name="arrival_dist"
            value={formData.arrival_dist}
            onChange={handleInputChange}
            disabled={isLoading}
          >
            <option value="exponential">Exponential</option>
            <option value="poisson">Poisson</option>
          </select>
        </div>
      </fieldset>

      {/* parte-Leandro: Sección 3: Configuración de Servicio */}
      <fieldset className="form-section">
        <legend>Service Configuration (μ - Mu)</legend>
        
        <div className="form-group">
          <label htmlFor="service_mean">Mean Service Time (seconds)</label>
          <input
            id="service_mean"
            name="service_mean"
            type="number"
            min="1"
            max="30"
            step="0.5"
            value={formData.service_mean}
            onChange={handleInputChange}
            disabled={isLoading}
            className={errors.service_mean ? 'input-error' : ''}
          />
          {errors.service_mean && <span className="error-message">{errors.service_mean}</span>}
          <small>Average time each teller spends serving a customer</small>
        </div>

        <div className="form-group">
          <label htmlFor="service_dist">Service Distribution</label>
          <select
            id="service_dist"
            name="service_dist"
            value={formData.service_dist}
            onChange={handleInputChange}
            disabled={isLoading}
          >
            <option value="exponential">Exponential</option>
            <option value="uniform">Uniform</option>
          </select>
        </div>
      </fieldset>

      {/* parte-Leandro: Sección 4: Configuración del Tiempo de Simulación */}
      <fieldset className="form-section">
        <legend>Simulation Duration</legend>
        
        <div className="form-group">
          <label htmlFor="max_time">Simulation Duration (seconds)</label>
          <div className="input-with-display">
            <input
              id="max_time"
              name="max_time"
              type="number"
              min="3600"
              max="86400"
              step="3600"
              value={formData.max_time}
              onChange={handleInputChange}
              disabled={isLoading}
              className={errors.max_time ? 'input-error' : ''}
            />
            <span className="time-display">{formatTimeDisplay(formData.max_time)}</span>
          </div>
          {errors.max_time && <span className="error-message">{errors.max_time}</span>}
          <small>Total simulation time in seconds (suggested: 8 hours = 28800 seconds)</small>
        </div>
      </fieldset>

      {/* parte-Leandro: Sección 5: Configuración Avanzada */}
      <fieldset className="form-section">
        <legend>Advanced Settings</legend>
        
        <div className="form-group">
          <label htmlFor="max_queue_capacity">Maximum Queue Capacity</label>
          <input
            id="max_queue_capacity"
            name="max_queue_capacity"
            type="number"
            min="1"
            value={formData.max_queue_capacity}
            onChange={handleInputChange}
            disabled={isLoading}
            className={errors.max_queue_capacity ? 'input-error' : ''}
          />
          {errors.max_queue_capacity && <span className="error-message">{errors.max_queue_capacity}</span>}
          <small>Maximum number of customers that can wait in the queue</small>
        </div>
      </fieldset>

      {/* parte-Leandro: Botón de envío del formulario */}
      <button
        type="submit"
        className="submit-button"
        disabled={isLoading}
      >
        {isLoading ? 'Starting Simulation...' : 'Start Simulation'}
      </button>
    </form>
  )
}

export default ConfigForm
