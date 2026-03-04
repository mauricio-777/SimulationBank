from dataclasses import dataclass
from typing import Optional
from .teller_status import TellerStatus
from src.customer.domain.customer import Customer

# Entidad: ventanilla (cajero) del banco
# Atributos: id, status (IDLE/BUSY/BROKEN), current_customer, sessions_served

# parte-Mauricio
@dataclass
class Teller:
    """
    Entidad: ventanilla (cajero) del banco
    Representa un recurso del sistema que atiende clientes uno a la vez.
    """
    id: str # Identificador alfanumérico de la ventanilla (ej. 'T-1')
    status: TellerStatus = TellerStatus.IDLE # Estado operativo actual (libre, ocupado o averiado)
    current_customer: Optional[Customer] = None # Referencia al cliente que está siendo atendido en este momento (si lo hay)
    sessions_served: int = 0 # Contador que acumula cuántos clientes han sido atendidos exitosamente por esta ventanilla

    def start_service(self, customer: Customer, current_time: float) -> None:
        """
        Inicia el proceso de atención para un cliente específico.
        Cambia el estado de la ventanilla a ocupado (BUSY).
        Registra el cliente actual y actualiza el estado del cliente a 'BEING_SERVED',
        guardando el momento exacto en el que inició su servicio.
        """
        self.status = TellerStatus.BUSY
        self.current_customer = customer
        customer.status = "BEING_SERVED"
        customer.service_start_time = current_time

    def end_service(self) -> Optional[Customer]:
        """
        Finaliza el servicio del cliente que está siendo atendido actualmente.
        Cambia el estado del cliente a completado ('COMPLETED').
        Libera la ventanilla cambiándola a estado 'IDLE'.
        Incrementa el número de sesiones servidas y devuelve el cliente que finalizó.
        """
        if not self.current_customer:
            return None
        served = self.current_customer
        served.status = "COMPLETED"
        self.current_customer = None
        self.status = TellerStatus.IDLE
        self.sessions_served += 1
        return served
