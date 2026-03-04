# UseCase: genera el reporte final de la simulación (resumen estadístico)
from src.simulation.infrastructure.in_memory_simulation_repository import InMemorySimulationRepository

class GetSimulationReport:
    """
    parte-Jhonny:
    Caso de Uso Principal para la Épica 3. 
    Se encarga de recuperar la simulación actual y pedirle 
    al módulo de métricas que calcule las estadísticas finales.
    """
    def __init__(self):
        self.repo = InMemorySimulationRepository.get_instance()

    def execute(self, simulation_id: str) -> dict:
        simulation = self.repo.get(simulation_id)
        if not simulation:
            return {"error": "Simulación no encontrada."}
            
        # Solicitamos procesar todas las métricas acumuladas
        return simulation.metrics.calculate_statistics(
            max_simulation_time=simulation.clock, # El reloj tiene el tiempo avanzado
            num_tellers=simulation.config.num_tellers
        )
