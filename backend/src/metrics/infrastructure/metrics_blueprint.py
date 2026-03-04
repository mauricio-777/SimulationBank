# Adaptador HTTP (input): Flask Blueprint con los endpoints de métricas
from flask import Blueprint, jsonify
from src.metrics.infrastructure.metrics_controller import MetricsController

metrics_bp = Blueprint('metrics', __name__)
controller = MetricsController()

@metrics_bp.route('/api/metrics/report/<simulation_id>', methods=['GET'])
def get_simulation_report(simulation_id):
    """
    parte-Jhonny:
    Endpoint HTTP GET para exportar los resultados a formato JSON (Épica 3.4).
    Recibe el ID de la simulación y retorna todas las métricas procesadas
    serializadas de una manera limpia para que el frontend las consuma.
    """
    report = controller.get_report(simulation_id)
    if "error" in report:
        return jsonify(report), 404
        
    return jsonify(report), 200
