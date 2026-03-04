# Adaptador (output): implementación en memoria del SimulationRepository
from typing import Dict, Optional
from src.simulation.domain.simulation import DiscreteEventSimulation

class InMemorySimulationRepository:
    """
    parte-Jhonny:
    Repositorio en memoria (Singleton simple) para almacenar 
    las simulaciones activas y poder consultar sus métricas.
    """
    _instance = None
    
    def __init__(self):
        self.simulations: Dict[str, DiscreteEventSimulation] = {}
        
    @classmethod
    def get_instance(cls) -> 'InMemorySimulationRepository':
        if cls._instance is None:
            cls._instance = InMemorySimulationRepository()
        return cls._instance
        
    def save(self, simulation: DiscreteEventSimulation) -> None:
        self.simulations[simulation.simulation_id] = simulation
        
    def get(self, simulation_id: str) -> Optional[DiscreteEventSimulation]:
        return self.simulations.get(simulation_id)
