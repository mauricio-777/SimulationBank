/**
 * parte-Leandro: Componente indicador de estado de simulación
 * 
 * Muestra visualmente:
 * 1. Estado actual (initializing, running, paused, completed, error)
 * 2. Barra de progreso con porcentaje
 * 3. Icono o indicador visual del estado
 * 
 * Este componente ayuda al usuario a entender rápidamente qué está pasando con la simulación.
 */
function StatusIndicator({ status = 'idle', progress = 0 }) {
  /**
   * parte-Leandro: Función para obtener información visual del estado
   * Retorna color, icono y texto descriptivo para cada estado
   */
  const getStatusInfo = () => {
    switch (status) {
      case 'initializing':
        return {
          icon: '⚙️',
          text: 'Initializing...',
          color: 'status-yellow',
          description: 'Preparing simulation environment'
        }
      case 'running':
        return {
          icon: '▶️',
          text: 'Running',
          color: 'status-green',
          description: 'Simulation in progress'
        }
      case 'paused':
        return {
          icon: '⏸️',
          text: 'Paused',
          color: 'status-blue',
          description: 'Simulation paused'
        }
      case 'completed':
        return {
          icon: '✅',
          text: 'Completed',
          color: 'status-success',
          description: 'Simulation finished successfully'
        }
      case 'error':
        return {
          icon: '❌',
          text: 'Error',
          color: 'status-error',
          description: 'An error occurred during simulation'
        }
      default:
        return {
          icon: '⭕',
          text: 'Ready',
          color: 'status-idle',
          description: 'Ready to start a new simulation'
        }
    }
  }

  const statusInfo = getStatusInfo()

  return (
    <div className={`status-indicator ${statusInfo.color}`}>
      {/* parte-Leandro: Icono del estado */}
      <div className="status-icon">
        {statusInfo.icon}
      </div>

      {/* parte-Leandro: Información textual del estado */}
      <div className="status-info">
        <h4 className="status-text">{statusInfo.text}</h4>
        <p className="status-description">{statusInfo.description}</p>
      </div>

      {/* parte-Leandro: Barra de progreso - mostrar solo cuando hay progreso significativo */}
      {progress > 0 && progress < 100 && (
        <div className="progress-container">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span className="progress-text">{Math.round(progress)}%</span>
        </div>
      )}

      {/* parte-Leandro: Barra de progreso completa cuando termina */}
      {progress === 100 && (
        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: '100%' }}></div>
          </div>
          <span className="progress-text">100%</span>
        </div>
      )}
    </div>
  )
}

export default StatusIndicator
