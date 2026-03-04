from enum import Enum

# parte-Mauricio
class TellerStatus(str, Enum):
    """
    Enum: estado operativo de una ventanilla
    IDLE    -> libre, esperando cliente
    BUSY    -> atendiendo a un cliente
    BROKEN  -> fuera de servicio (fallo simulado)
    """
    IDLE = "IDLE"
    BUSY = "BUSY"
    BROKEN = "BROKEN"
