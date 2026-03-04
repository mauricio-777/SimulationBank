# Puerto (output): contrato para generar clientes con distribución aleatoria

from abc import ABC, abstractmethod
from typing import Tuple

# parte-Mauricio
class CustomerGeneratorPort(ABC):
    """
    Puerto (output): contrato para generar clientes con distribución aleatoria
    """

    @abstractmethod
    def get_next_arrival_interval(self) -> float:
        """Returns the time interval until the next customer arrives."""
        pass

    @abstractmethod
    def get_service_time(self) -> float:
        """Returns the service time duration for a customer."""
        pass

    @abstractmethod
    def get_next_customer_attributes(self) -> Tuple[int, str]:
        """Returns a tuple of (priority, transaction_type) for the next customer."""
        pass
