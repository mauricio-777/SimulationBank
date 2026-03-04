# Controlador: orquesta los use cases de métricas invocados por el Blueprint
from src.metrics.application.get_simulation_report import GetSimulationReport

class MetricsController:
    """
    parte-Jhonny:
    Controlador que maneja las solicitudes HTTP.
    Invoca al UseCase GetSimulationReport y devuelve la respuesta.
    """
    def __init__(self):
        self.get_report_use_case = GetSimulationReport()

    def get_report(self, simulation_id: str):
        # En un sistema real aquí se usaría Flask Request/Response
        # pero retornamos el dict que el Blueprint serializará en JSON.
        result = self.get_report_use_case.execute(simulation_id)
        return result
