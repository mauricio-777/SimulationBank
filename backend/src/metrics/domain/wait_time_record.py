# Value Object: registro de tiempo de espera de un cliente
# Contiene: customer_id, priority, wait_time, service_time, total_time
from dataclasses import dataclass

@dataclass
class WaitTimeRecord:
    """
    parte-Jhonny:
    Este es un 'Value Object' inmutable que representa 
    el registro de tiempos asociados a un solo cliente que fue atendido.
    Almacenamos la prioridad para poder calcular promedios por prioridad.
    """
    customer_id: str
    priority: int
    wait_time: float
    service_time: float
    total_time: float
