# Adapter (Infrastructure): concrete implementation of queue using binary heap
# Wraps the domain PriorityQueue for use as a repository interface

from typing import Optional
from src.queue.domain.priority_queue import PriorityQueue
from src.queue.domain.queue_policy import QueuePolicy
from src.customer.domain.customer import Customer


# parte-BinaryHeapAdapter: Infrastructure adapter providing queue interface
class BinaryHeapQueueAdapter:
    """
    Concrete implementation adapter that provides a user-friendly interface
    to the domain PriorityQueue entity using binary heap storage.
    
    This adapter follows the Adapter pattern to translate between the domain logic
    and infrastructure concerns.
    """
    
    def __init__(self, queue_id: str, policy: Optional[QueuePolicy] = None):
        """
        parte-Init: Initializes the queue adapter with an optional policy.
        
        Args:
            queue_id: Unique identifier for this queue instance
            policy: QueuePolicy object defining queue behavior (uses default if None)
        """
        if policy is None:
            policy = QueuePolicy()  # Default policy: no capacity limit, FIFO tie-breaking
        self.priority_queue = PriorityQueue(queue_id, policy)
    
    def enqueue(self, customer: Customer) -> bool:
        """
        parte-EnqueueAdapter: Enqueues a customer using the underlying priority queue.
        
        Args:
            customer: The customer to enqueue
        
        Returns:
            True if successfully enqueued
            False if rejected (due to capacity policy)
        """
        return self.priority_queue.enqueue(customer)
    
    def dequeue(self) -> Optional[Customer]:
        """
        parte-DequeueAdapter: Dequeues and returns the highest-priority customer.
        
        Returns:
            The Customer with highest priority, or None if queue is empty
        """
        return self.priority_queue.dequeue()
    
    def peek(self) -> Optional[Customer]:
        """
        parte-PeekAdapter: Returns the highest-priority customer without removing.
        
        Returns:
            The Customer with highest priority, or None if queue is empty
        """
        return self.priority_queue.peek()
    
    def is_empty(self) -> bool:
        """parte-IsEmpty: Checks if queue contains no customers."""
        return self.priority_queue.is_empty()
    
    def size(self) -> int:
        """parte-Size: Returns current number of customers in queue."""
        return self.priority_queue.size()
    
    def get_queue_id(self) -> str:
        """parte-GetId: Returns the unique identifier of this queue."""
        return self.priority_queue.id
    
    def get_policy(self) -> QueuePolicy:
        """parte-GetPolicy: Returns the policy configuration of this queue."""
        return self.priority_queue.policy
