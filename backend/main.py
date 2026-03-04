# Entry point — Flask application
from flask import Flask, jsonify
from src.metrics.infrastructure.metrics_blueprint import metrics_bp
from src.simulation.infrastructure.in_memory_simulation_repository import InMemorySimulationRepository
from src.simulation.domain.simulation import DiscreteEventSimulation
from src.simulation.domain.simulation_config import SimulationConfig

app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(metrics_bp)

# parte-Jhonny: Ruta de prueba para verificar que el servidor está vivo
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Simulation Bank API de métricas funcionando (Épica 3)!"})

# parte-Jhonny: Endpoint de desarrollo para crear y correr una simulación de prueba rápido
# Ya que las otras interfaces aún no están listas, esto asegura que podamos testear
# la lógica de nuestra Épica 3 generando datos mock de la simulación.
@app.route('/api/simulation/test_run', methods=['POST'])
def test_run():
    repo = InMemorySimulationRepository.get_instance()
    
    # Importar configuraciones requeridas por el simulador original
    try:
        from src.simulation.domain.simulation_config import SimulationConfig
        config = SimulationConfig(max_simulation_time=3600, num_tellers=3)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    sim_id = "test-sim-123"
    sim = DiscreteEventSimulation(sim_id, config)
    repo.save(sim)
    
    sim.initialize()
    sim.run()
    
    return jsonify({
        "message": "Simulación de prueba generada y ejecutada al 100%.",
        "simulation_id": sim_id,
        "instrucciones": f"Ahora haz un GET a /api/metrics/report/{sim_id} para ver los JSON de las métricas.",
        "reloj_final": sim.clock
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
