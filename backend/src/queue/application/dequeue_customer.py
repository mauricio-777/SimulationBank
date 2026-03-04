# Use Case: dequeuing the highest-priority customer from the queue
# Extracts and returns the customer with highest current priority (heapify-down)

from typing import Optional
from src.shared.application.use_case import UseCase
from src.customer.domain.customer import Customer
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository


# parte-DequeueUseCase: Orchestrates extraction of highest-priority customer
class DequeueCustomerUseCase(UseCase):
    """
    Use Case: Dequeues the highest-priority customer from the queue.
    
    Responsibilities:
    - Retrieve the next customer to be served
    - Respect priority ordering (priority 1 before 2, 2 before 3)
    - Respect FIFO ordering within same priority level
    - Update queue state
    
    Process:
    1. Retrieve the queue from repository
    2. Extract highest-priority customer
    3. Return the customer or indication that queue is empty
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
        parte-Execute: Dequeues and returns the highest-priority customer.
        
        Returns:
            Dictionary with:
            - 'success': bool indicating if a customer was dequeued
            - 'customer': Customer object if available, None if queue empty
            - 'message': descriptive message
            - 'queue_size': current queue size after operation
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
        
        # Attempt to dequeue highest-priority customer
        customer = queue.dequeue()
        
        if customer is not None:
            return {
                'success': True,
                'customer': customer,
                'message': f"Customer {customer.id} (priority {customer.priority}) dequeued successfully",
                'queue_size': queue.size()
            }
        else:
            return {
                'success': False,
                'customer': None,
                'message': "Queue is empty: no customers to dequeue",
                'queue_size': 0
            }
