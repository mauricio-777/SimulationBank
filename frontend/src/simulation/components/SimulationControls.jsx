/**
 * parte-Leandro: Componente de controles de simulación
 * 
 * Este componente proporciona botones para controlar la simulación:
 * - Iniciar
 * - Pausar/Reanudar
 * - Detener
 * - Exportar resultados
 * 
 * Nota: En la versión actual de la Épica 4, estos controles están integrados
 * en SimulationPanel. Este componente está disponible para futuras extensiones.
 */
function SimulationControls({ simulationId, onPause, onResume, onStop, isPaused, isRunning }) {
  return (
    <div className="simulation-controls">
      <div className="controls-group">
        {/* parte-Leandro: Botón para pausar simulación si está en ejecución */}
        {isRunning && !isPaused && (
          <button className="control-button pause-button" onClick={onPause}>
            ⏸ Pausar
          </button>
        )}

        {/* parte-Leandro: Botón para reanudar simulación si está pausada */}
        {isPaused && (
          <button className="control-button resume-button" onClick={onResume}>
            ▶ Reanudar
          </button>
        )}

        {/* parte-Leandro: Botón para detener simulación */}
        {isRunning && (
          <button className="control-button stop-button" onClick={onStop}>
            ⏹ Detener
          </button>
        )}
      </div>
    </div>
  )
}

export default SimulationControls
