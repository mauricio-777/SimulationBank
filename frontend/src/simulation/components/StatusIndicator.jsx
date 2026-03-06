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
          text: 'Inicializando...',
          color: 'status-yellow',
          description: 'Preparando entorno de simulación'
        }
      case 'running':
        return {
          icon: '▶️',
          text: 'En curso',
          color: 'status-green',
          description: 'Simulación en progreso'
        }
      case 'paused':
        return {
          icon: '⏸️',
          text: 'Pausada',
          color: 'status-blue',
          description: 'Simulación pausada'
        }
      case 'completed':
        return {
          icon: '✅',
          text: 'Completada',
          color: 'status-success',
          description: 'Simulación finalizada con éxito'
        }
      case 'error':
        return {
          icon: '❌',
          text: 'Error',
          color: 'status-error',
          description: 'Ocurrió un error durante la simulación'
        }
      default:
        return {
          icon: '⭕',
          text: 'Listo',
          color: 'status-idle',
          description: 'Listo para iniciar una nueva simulación'
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
