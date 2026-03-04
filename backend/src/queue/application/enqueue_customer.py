# Use Case: enqueuing a customer into the priority queue
# Inserts customer with their priority level, respecting FIFO within same priority

from src.shared.application.use_case import UseCase
from src.customer.domain.customer import Customer
from src.queue.infrastructure.in_memory_queue_repository import InMemoryQueueRepository


# parte-EnqueueUseCase: Orchestrates customer insertion into priority queue
class EnqueueCustomerUseCase(UseCase):
    """
    Use Case: Enqueues a customer into the priority queue.
    
    Responsibilities:
    - Take a customer from domain layer
    - Check queue capacity policy
    - Insert into queue respecting priority + FIFO ordering
    - Return success/rejection status
    
    Process:
    1. Retrieve the queue from repository
    2. Attempt to enqueue the customer
    3. Return result (success or rejection reason)
    """
    
    def __init__(self, queue_id: str = "main_queue"):
        """
        parte-Init: Initializes the use case with a specific queue.
        
        Args:
            queue_id: ID of the target queue (defaults to "main_queue")
        """
        self.queue_id = queue_id
        self.repository = InMemoryQueueRepository.get_instance()
    
    def execute(self, customer: Customer) -> dict:
        """
        parte-Execute: Enqueues a customer into the priority queue.
        
        Args:
            customer: The Customer object to enqueue
        
        Returns:
            Dictionary with:
            - 'success': bool indicating if customer was queued
            - 'message': descriptive message
            - 'queue_size': current queue size after operation
            - 'customer_id': ID of the customer
        """
        # Get the queue from repository
        queue = self.repository.get_queue(self.queue_id)
        
        if queue is None:
            return {
                'success': False,
                'message': f"Queue '{self.queue_id}' not found",
                'queue_size': 0,
                'customer_id': customer.id
            }
        
        # Attempt to enqueue customer
        was_enqueued = queue.enqueue(customer)
        
        if was_enqueued:
            return {
                'success': True,
                'message': f"Customer {customer.id} (priority {customer.priority}) enqueued successfully",
                'queue_size': queue.size(),
                'customer_id': customer.id
            }
        else:
            return {
                'success': False,
                'message': f"Customer {customer.id} rejected: queue at capacity",
                'queue_size': queue.size(),
                'customer_id': customer.id
            }
