# Use Case: peeking at the highest-priority customer without removing
# Allows lookahead to see next customer to be served without modifying queue state

from typing import Optional
from src.shared.application.use_case import UseCase
from src.customer.domain.customer import Customer
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository


# parte-PeekUseCase: Orchestrates examination of next highest-priority customer
class PeekQueueUseCase(UseCase):
    """
    Use Case: Examines the highest-priority customer without removing them.
    
    Responsibilities:
    - Look at the front of the queue (highest priority customer)
    - Do NOT modify queue state
    - Return customer info or indication that queue is empty
    - Useful for teller or simulation lookahead operations
    
    Process:
    1. Retrieve the queue from repository
    2. Peek at highest-priority customer
    3. Return customer (if available) or None
    """
    
    def __init__(self, queue_id: str = "main_queue"):
        """
        parte-Init: Initializes the use case with a specific queue.
        
        Args:
            queue_id: ID of the target queue (defaults to "main_queue")
        """
        self.queue_id = queue_id
        self.repository = InMemoryQueueRepository.get_instance()
    
    def execute(self) -> dict:
        """
        parte-Execute: Examines and returns the highest-priority customer without removal.
        
        Returns:
            Dictionary with:
            - 'success': bool indicating if a customer is visible
            - 'customer': Customer object if available, None if queue empty
            - 'message': descriptive message
            - 'queue_size': current queue size (should not change)
        """
        # Get the queue from repository
        queue = self.repository.get_queue(self.queue_id)
        
        if queue is None:
            return {
                'success': False,
                'customer': None,
                'message': f"Queue '{self.queue_id}' not found",
                'queue_size': 0
            }
        
        # Peek at highest-priority customer (non-destructive)
        customer = queue.peek()
        
        if customer is not None:
            return {
                'success': True,
                'customer': customer,
                'message': f"Next customer: {customer.id} (priority {customer.priority})",
                'queue_size': queue.size()
            }
        else:
            return {
                'success': False,
                'customer': None,
                'message': "Queue is empty: nothing to peek",
                'queue_size': 0
            }
