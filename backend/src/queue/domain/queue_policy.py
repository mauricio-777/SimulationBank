# Value Object: queue policy configuration
# Defines queue behavior: preemption rules, tie-breaking, and capacity constraints

from enum import Enum
from dataclasses import dataclass
from src.shared.domain.value_object import ValueObject


class TieBreakerStrategy(Enum):
    """
    parte-TieBreaker: Strategies for deciding order when customers have same priority.
    FIFO: First In, First Out - respects arrival order
    """
    FIFO = "fifo"  # First In, First Out based on arrival timestamp


class PreemptionPolicy(Enum):
    """
    parte-Preemption: Defines if a higher-priority customer can interrupt lower-priority service.
    NON_PREEMPTIVE: Once service starts, customer completes even with higher-priority arrivals
    """
    NON_PREEMPTIVE = "non_preemptive"


@dataclass(frozen=True)
class QueuePolicy(ValueObject):
    """
    Value Object: encapsulates the policy rules for queue behavior.
    
    Configuration:
    - tie_breaker: Strategy for ordering customers with equal priority
    - preemption: Whether service can be interrupted by higher-priority customers
    - max_queue_size: Maximum customers allowed in queue (-1 for unlimited)
    - allow_rejections: If True, reject customers exceeding max_queue_size
    """
    tie_breaker: TieBreakerStrategy = TieBreakerStrategy.FIFO
    preemption: PreemptionPolicy = PreemptionPolicy.NON_PREEMPTIVE
    max_queue_size: int = -1  # -1 indicates unlimited capacity
    allow_rejections: bool = True  # When max_queue_size is exceeded
    
    def __eq__(self, other: object) -> bool:
        """Two policies are equal if they have identical configuration."""
        if not isinstance(other, QueuePolicy):
            return False
        return (self.tie_breaker == other.tie_breaker and
                self.preemption == other.preemption and
                self.max_queue_size == other.max_queue_size and
                self.allow_rejections == other.allow_rejections)
    
    def __hash__(self) -> int:
        """Hash based on policy configuration."""
        return hash((self.tie_breaker, self.preemption, self.max_queue_size, self.allow_rejections))
    
    def is_at_capacity(self, current_size: int) -> bool:
        """
        parte-CapacityCheck: Determines if queue has reached maximum capacity.
        Returns True if max_queue_size is set and current_size >= max_queue_size.
        """
        return self.max_queue_size != -1 and current_size >= self.max_queue_size
    
    def should_reject(self, current_size: int) -> bool:
        """
        parte-RejectionLogic: Determines if a new customer should be rejected.
        Returns True if queue is at capacity AND rejections are enabled.
        """
        return self.is_at_capacity(current_size) and self.allow_rejections
