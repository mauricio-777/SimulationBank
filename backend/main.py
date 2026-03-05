# parte-Leandro: Punto de entrada de la aplicación Flask
# Este es el archivo principal que configura e inicia el servidor.
# Se encarga de:
# 1. Crear la instancia de la aplicación Flask
# 2. Registrar todos los blueprints (módulos de rutas) de la aplicación
# 3. Inicializar endpoints generales (como health check)
# 4. Ejecutar el servidor en host 0.0.0.0 y puerto 5000

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.metrics.infrastructure.metrics_blueprint import metrics_bp
from src.simulation.infrastructure.simulation_blueprint import simulation_bp
from src.simulation.infrastructure.in_memory_simulation_repository import InMemorySimulationRepository
from src.simulation.domain.simulation import DiscreteEventSimulation
from src.simulation.domain.simulation_config import SimulationConfig

# parte-Leandro: Crear instancia de la aplicación Flask
app = Flask(__name__)

# parte-Leandro: Habilitar CORS (Cross-Origin Resource Sharing) para permitir peticiones desde el frontend
# Esto es necesario porque el frontend (http://localhost:5173) hace peticiones al backend (http://localhost:5000)
CORS(app)

# parte-Leandro: Registrar los blueprints (módulos con grupos de rutas relacionadas)
# metrics_bp: contiene los endpoints para obtener reportes y métricas de simulaciones
# simulation_bp: contiene los endpoints para crear y gestionar simulaciones
app.register_blueprint(metrics_bp)
app.register_blueprint(simulation_bp)


@app.route('/', methods=['GET'])
def health_check():
    """
    parte-Leandro: Endpoint de verificación de salud del servidor.
    El frontend puede consultar este endpoint para verificar que el backend está activo y respondiendo.
    """
    return jsonify({"status": "Simulation Bank API - Épica 4 (Frontend) funcionando correctamente"})


@app.route('/api/config/defaults', methods=['GET'])
def get_default_configuration():
    """
    parte-Leandro: Endpoint para obtener la configuración por defecto de la simulación.
    
    El frontend usa este endpoint durante su carga inicial para mostrar valores por defecto
    en el formulario de configuración. Esto asegura que haya coherencia entre frontend y backend.
    
    Retorna un JSON con los parámetros por defecto que se pueden usar en una simulación.
    """
    default_config = {
        "num_tellers": 3,              # parte-Leandro: Número por defecto de ventanillas del banco
        "arrival_rate": 1.0,           # parte-Leandro: Tasa de llegadas (λ) - clientes por unidad de tiempo
        "service_mean": 5.0,           # parte-Leandro: Tiempo medio de servicio (μ) en segundos
        "max_time": 28800,             # parte-Leandro: 8 horas en segundos como horizonte temporal
        "max_queue_capacity": 100,     # parte-Leandro: Capacidad máxima de la cola de espera
        "arrival_dist": "exponential", # parte-Leandro: Distribución de llegadas (exponencial por defecto)
        "service_dist": "exponential", # parte-Leandro: Distribución de servicio (exponencial por defecto)
        "service_stddev": 1.0,         # parte-Leandro: Desviación estándar del servicio
        "priority_weights": [0.1, 0.3, 0.6]  # parte-Leandro: Pesos de distribución de prioridades [Baja, Media, Alta]
    }
    
    return jsonify({
        "success": True,
        "defaults": default_config,
        "limits": {
            "num_tellers_min": 1,
            "num_tellers_max": 10,
            "arrival_rate_min": 0.1,
            "arrival_rate_max": 10.0,
            "service_mean_min": 1.0,
            "service_mean_max": 30.0,
            "max_time_min": 3600,
            "max_time_max": 86400
        }
    })


@app.route('/api/simulation/test_run', methods=['POST'])
def test_run():
    """
    parte-Leandro: Endpoint de desarrollo para crear y ejecutar una simulación de prueba rápidamente.
    Esto es útil para testing durante el desarrollo cuando el frontend aún no estáCompleto.
    """
    repo = InMemorySimulationRepository.get_instance()
    
    try:
        # parte-Leandro: Crear configuración de prueba
        config = SimulationConfig(max_simulation_time=3600, num_tellers=3)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # parte-Leandro: Crear y ejecutar la simulación de prueba
    sim_id = "test-sim-123"
    sim = DiscreteEventSimulation(sim_id, config)
    repo.save(sim)
    
    sim.initialize()
    sim.run()
    
    return jsonify({
        "message": "Test simulation created and executed successfully.",
        "simulation_id": sim_id,
        "instructions": f"Now do a GET to /api/metrics/report/{sim_id} to see the metrics in JSON format.",
        "final_clock": sim.clock
    })


if __name__ == '__main__':
    # parte-Leandro: Ejecutar el servidor Flask
    # - host='0.0.0.0': Aceptar conexiones desde cualquier dirección IP
    # - port=5000: Escuchar en el puerto 5000
    # - debug=True: Habilitar recarga automática cuando hay cambios en el código
    app.run(host='0.0.0.0', port=5000, debug=True)
