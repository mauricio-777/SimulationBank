# Value Object: represents a node in the priority queue (binary heap)
# Stores a customer with priority level and timestamp for tie-breaking (FIFO within same priority)

from dataclasses import dataclass
from typing import Optional
from src.shared.domain.value_object import ValueObject
from src.customer.domain.customer import Customer


# parte-QueueNode: Immutable container for queue priority calculation
@dataclass(frozen=True)
class QueueNode(ValueObject):
    """
    Value Object: represents a single node in the priority queue.
    
    Contains:
    - customer: The customer object stored in the queue
    - arrival_sequence: Timestamp/counter for FIFO tie-breaking within same priority level
    
    Used for proper ordering: first by priority (ascending: 1 highest), 
    then by arrival_sequence (ascending: earliest first)
    """
    customer: Customer
    arrival_sequence: float  # Timestamp or sequence counter ensuring FIFO within same priority
    
    def __eq__(self, other: object) -> bool:
        """
        Two nodes are equal if they contain the same customer.
        Priority and sequence are not used for equality since they're ordering criteria.
        """
        if not isinstance(other, QueueNode):
            return False
        return self.customer.id == other.customer.id
    
    def __hash__(self) -> int:
        """Hash based on customer ID for use in sets and dicts."""
        return hash(self.customer.id)
    
    def __lt__(self, other: 'QueueNode') -> bool:
        """
        Comparison for heap ordering.
        parte-Ordering: Compares first by priority, then by arrival_sequence for FIFO within same priority.
        Returns True if self has HIGHER priority (lower numerical value) than other.
        """
        if self.customer.priority != other.customer.priority:
            return self.customer.priority < other.customer.priority  # Lower number = higher priority
        return self.arrival_sequence < other.arrival_sequence  # FIFO: earlier arrival first
    
    def __le__(self, other: 'QueueNode') -> bool:
        """Less than or equal comparison for heap compatibility."""
        return self < other or self == other
    
    def __gt__(self, other: 'QueueNode') -> bool:
        """Greater than comparison for heap compatibility."""
        return other < self
    
    def __ge__(self, other: 'QueueNode') -> bool:
        """Greater than or equal comparison for heap compatibility."""
        return self > other or self == other
