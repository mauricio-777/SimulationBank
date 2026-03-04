from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any

# parte-Mauricio
class EventType(str, Enum):
    ARRIVAL = "ARRIVAL"
    SERVICE_START = "SERVICE_START"
    SERVICE_END = "SERVICE_END"

@dataclass(order=True)
class SimulationEvent:
    """
    Evento de dominio: emitido cuando la simulación cambia de estado
    Ordenable por 'time' para usar en la cola de prioridad de la simulación.
    """
    time: float
    event_type: EventType = field(compare=False)
    customer: Optional[Any] = field(default=None, compare=False)
    teller_id: Optional[str] = field(default=None, compare=False)
