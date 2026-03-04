# Base interface for all Use Cases (Application layer)
# Defines the contract that every use case must implement

from abc import ABC, abstractmethod
from typing import Any


# parte-UseCase: Standard interface for application business logic
class UseCase(ABC):
    """
    Abstract base class for all use cases in the application layer.
    Each use case represents a single business operation or workflow
    that the system can perform.
    """
    
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the use case with the provided arguments.
        Must be implemented by all concrete use cases.
        
        Returns: The result of executing this use case
        """
        pass
