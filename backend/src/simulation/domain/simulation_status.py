from enum import Enum

# parte-Mauricio
class SimulationStatus(str, Enum):
    """
    Enum: estados posibles de una simulación
    IDLE | RUNNING | PAUSED | FINISHED
    """
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"
