# Base class for all Value Objects in the domain
# Value Objects represent immutable, conceptual values that define characteristics but have no identity

from abc import ABC, abstractmethod


# parte-ValueObject: Immutable objects compared by value, not identity
class ValueObject(ABC):
    """
    Abstract base class for all domain Value Objects.
    Value Objects are immutable objects defined by their attributes.
    Unlike entities, two value objects with the same attributes are considered equal.
    """
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Two value objects are equal if all their attributes are equal."""
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """Value objects must be hashable based on their attributes."""
        pass
