# Entidad: representa un cliente que llega al banco
# Atributos: id, arrival_time, service_time, priority, transaction_type, status

from dataclasses import dataclass
from typing import Optional
from .priority import Priority
from .transaction_type import TransactionType

# parte-Mauricio
@dataclass
class Customer:
    """
    Entidad: representa un cliente que llega al banco.
    Define todos los atributos esenciales para rastrear el ciclo de vida del usuario dentro de la sucursal.
    """
    id: str # Identificador único del cliente generado aleatoriamente
    arrival_time: float # Momento en el tiempo de la simulación en el que el cliente llega al banco
    service_time: float # Tiempo total requerido en la ventanilla para procesar su transacción
    priority: int # Nivel de prioridad asignado (1: Alta, 2: Media, 3: Baja) para determinar su lugar en la cola
    transaction_type: str # El tipo de operación que el cliente viene a realizar (ej. DEPOSIT, WITHDRAWAL)
    status: str = "WAITING" # Estado inicial por defecto, indica que el cliente está esperando en la fila
    service_start_time: Optional[float] = None # Momento exacto en el que el cliente es llamado a una ventanilla
