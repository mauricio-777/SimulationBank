# parte-Leandro: Adaptador HTTP (input) - Flask Blueprint para los endpoints de simulación
# Este blueprint define todos los endpoints disponibles para:
# - Iniciar simulaciones (/api/simulation/start) - POST
# - Obtener estado de simulaciones (/api/simulation/state/<id>) - GET
# - Obtener resultados finales (/api/simulation/results/<id>) - GET
#
# Todos estos endpoints comunican con el SimulationController que orquesta la lógica de negocio

from flask import Blueprint, request, jsonify
from src.simulation.infrastructure.simulation_controller import SimulationController

# parte-Leandro: Crear el blueprint para agrupar todos los endpoints de simulación bajo /api/simulation
simulation_bp = Blueprint('simulation', __name__, url_prefix='/api/simulation')

# parte-Leandro: Instanciar el controlador que orquestará las operaciones
controller = SimulationController()


@simulation_bp.route('/start', methods=['POST'])
def start_simulation():
    """
    parte-Leandro: Endpoint para iniciar una nueva simulación con parámetros personalizados.
    
    Método: POST
    URL: /api/simulation/start
    Espera JSON con estructura:
    {
        "num_tellers": 3,
        "arrival_rate": 1.5,
        "service_mean": 5.0,
        "max_time": 28800,
        "max_queue_capacity": 100,
        "priority_weights": [0.1, 0.3, 0.6],
        "service_dist": "exponential"
    }
    
    Retorna: JSON con simulation_id y estado inicial
    """
    try:
        # parte-Leandro: Obtener el JSON del cuerpo de la petición
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400
        
        # parte-Leandro: Delegar al controlador la creación de la simulación
        result = controller.start_simulation(data)
        
        # parte-Leandro: Retornar respuesta con código de estado 201 (Created)
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@simulation_bp.route('/state/<simulation_id>', methods=['GET'])
def get_simulation_state(simulation_id):
    """
    parte-Leandro: Endpoint para consultar el estado actual de una simulación en ejecución.
    
    Método: GET
    URL: /api/simulation/state/{simulation_id}
    
    Retorna: JSON con estado actual (running, completed, paused, error, etc.)
    """
    try:
        # parte-Leandro: Consultar el estado actual de la simulación
        result = controller.get_simulation_state(simulation_id)
        
        # parte-Leandro: Si hubo error, retornar código 404. Si no, retornar 200
        status_code = 404 if "error" in result else 200
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@simulation_bp.route('/results/<simulation_id>', methods=['GET'])
def get_simulation_results(simulation_id):
    """
    parte-Leandro: Endpoint para obtener los resultados completos de una simulación terminada.
    
    Método: GET
    URL: /api/simulation/results/{simulation_id}
    
    Nota: Solo funciona si la simulación ya ha completado su ejecución.
    
    Retorna: JSON con todas las métricas de la simulación (tiempos de espera, tasas de servicio, etc.)
    """
    try:
        # parte-Leandro: Consultar los resultados de la simulación
        result = controller.get_simulation_results(simulation_id)
        
        # parte-Leandro: Si hubo error, retornar código 404. Si no, retornar 200
        status_code = 404 if "error" in result else 200
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

