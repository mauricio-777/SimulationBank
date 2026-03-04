from enum import IntEnum

# parte-Mauricio
class Priority(IntEnum):
    """
    Enum: nivel de prioridad del cliente
     HIGH = 1  (adulto mayor, embarazada)
     MEDIUM = 2 (cliente preferencial)
     LOW = 3    (cliente regular)
    """
    HIGH = 1
    MEDIUM = 2
    LOW = 3
