# Base class for all domain entities
# Provides common functionality and interface for all entities in the domain layer

from uuid import uuid4
from typing import Optional


# parte-Entity: Provides unique identification and equality comparison for domain entities
class Entity:
    """
    Abstract base class for all domain entities.
    Ensures every entity has a unique identifier and provides equality comparison based on ID.
    """
    def __init__(self, entity_id: Optional[str] = None):
        self.id: str = entity_id or str(uuid4())
    
    def __eq__(self, other: object) -> bool:
        """
        Compares two entities based on their ID.
        Two entities are equal if they have the same ID.
        """
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash implementation based on entity ID for use in sets and dicts."""
        return hash(self.id)
