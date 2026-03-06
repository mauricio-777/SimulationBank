import { useEffect, useState } from 'react'
import './App.css'
import SimulationPanel from './simulation/components/SimulationPanel'

/**
 * parte-Leandro: Componente raíz de la aplicación
 * 
 * Este componente es el contenedor principal de toda la aplicación.
 * Se encarga de:
 * 1. Verificar que el backend está disponible
 * 2. Inicializar valores por defecto desde el servidor
 * 3. Renderizar el panel de simulación principal
 * 4. Manejar errores de conexión con el backend
 */
function App() {
  // parte-Leandro: Estado para almacenar si el backend está disponible
  const [backendAvailable, setBackendAvailable] = useState(false)

  // parte-Leandro: Estado para almacenar los parámetros por defecto obtenidos del backend
  const [defaultConfig, setDefaultConfig] = useState(null)

  // parte-Leandro: Estado para mostrar mensajes de error si el backend no está disponible
  const [error, setError] = useState(null)

  /**
   * parte-Leandro: Hook useEffect para verificar disponibilidad del backend al cargar la aplicación
   * Se ejecuta una sola vez cuando el componente se monta (empty dependency array)
   */
  useEffect(() => {
    const checkBackendAndLoadDefaults = async () => {
      try {
        // parte-Leandro: Primero, hacer un GET al endpoint de health check
        const healthResponse = await fetch('http://localhost:5000/')

        if (!healthResponse.ok) {
          throw new Error('El servidor backend no responde correctamente')
        }

        // parte-Leandro: Si el health check pasó, obtener la configuración por defecto
        const configResponse = await fetch('http://localhost:5000/api/config/defaults')

        if (!configResponse.ok) {
          throw new Error('No se pudo cargar la configuración por defecto')
        }

        // parte-Leandro: Parsear la respuesta JSON
        const configData = await configResponse.json()

        // parte-Leandro: Actualizar el estado con la configuración obtenida
        setDefaultConfig(configData)
        setBackendAvailable(true)
        setError(null)

      } catch (err) {
        // parte-Leandro: Si hay error de conexión, mostrar mensaje al usuario
        setError(`Error al conectar con el backend: ${err.message}. Asegúrate de que el servidor backend esté ejecutándose en http://localhost:5000`)
        setBackendAvailable(false)
      }
    }

    // parte-Leandro: Ejecutar la verificación al montar el componente
    checkBackendAndLoadDefaults()
  }, [])

  /**
   * parte-Leandro: Renderizar la aplicación
   * Si hay error de conexión, mostrar mensaje de error
   * Si el backend está disponible, mostrar el panel de simulación con la configuración por defecto
   */
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Simulation Bank - Simulación de Eventos Discretos</h1>
        <p>Sistema de Gestión de Colas con Manejo de Prioridades</p>
      </header>

      {/* parte-Leandro: Mostrar error si hay problemas de conexión */}
      {error && (
        <div className="error-banner">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
        </div>
      )}

      {/* parte-Leandro: Mostrar contenido solo si el backend está disponible */}
      {backendAvailable && defaultConfig && (
        <main className="app-main">
          <SimulationPanel defaultConfig={defaultConfig} />
        </main>
      )}

      {/* parte-Leandro: Mostrar indicador de carga mientras se verifican los parámetros */}
      {!backendAvailable && !error && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Conectando al servidor backend...</p>
        </div>
      )}
    </div>
  )
}

export default App
