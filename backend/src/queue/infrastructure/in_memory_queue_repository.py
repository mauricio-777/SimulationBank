# Output Adapter (Repository): in-memory storage of queue instances
# Manages persistence and retrieval of queue objects during runtime

from typing import Dict, Optional
from src.queue.infrastructure.binary_heap_queue import BinaryHeapQueueAdapter
from src.queue.domain.queue_policy import QueuePolicy


# parte-Repository: Singleton pattern for centralized queue storage management
class InMemoryQueueRepository:
    """
    Output Adapter: manages in-memory storage of queue instances.
    Uses Singleton pattern to ensure only one repository instance exists during execution.
    
    Concept: Acts as a storage service for queue objects, allowing multiple queues
    to coexist (useful if multiple simulation runs or different queue types are needed).
    """
    
    _instance: Optional['InMemoryQueueRepository'] = None
    
    def __init__(self):
        """parte-Constructor: Initializes internal queue storage."""
        self.queues: Dict[str, BinaryHeapQueueAdapter] = {}
    
    @classmethod
    def get_instance(cls) -> 'InMemoryQueueRepository':
        """
        parte-Singleton: Returns the single instance of this repository.
        Creates instance on first call and reuses it thereafter.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def create_queue(self, queue_id: str, policy: Optional[QueuePolicy] = None) -> BinaryHeapQueueAdapter:
        """
        parte-Create: Creates and stores a new priority queue.
        
        Args:
            queue_id: Unique identifier for the new queue
            policy: QueuePolicy configuration (defaults to no capacity limit)
        
        Returns:
            The newly created BinaryHeapQueueAdapter instance
        """
        if queue_id in self.queues:
            raise ValueError(f"Queue with ID '{queue_id}' already exists")
        
        queue = BinaryHeapQueueAdapter(queue_id, policy)
        self.queues[queue_id] = queue
        return queue
    
    def get_queue(self, queue_id: str) -> Optional[BinaryHeapQueueAdapter]:
        """
        parte-Retrieve: Gets an existing queue by ID.
        
        Args:
            queue_id: The ID of the queue to retrieve
        
        Returns:
            The BinaryHeapQueueAdapter if found, None otherwise
        """
        return self.queues.get(queue_id)
    
    def delete_queue(self, queue_id: str) -> bool:
        """
        parte-Delete: Removes a queue from storage.
        
        Args:
            queue_id: The ID of the queue to delete
        
        Returns:
            True if queue was deleted, False if it didn't exist
        """
        if queue_id in self.queues:
            del self.queues[queue_id]
            return True
        return False
    
    def queue_exists(self, queue_id: str) -> bool:
        """parte-Exists: Checks if a queue with given ID exists."""
        return queue_id in self.queues
    
    def all_queues(self) -> Dict[str, BinaryHeapQueueAdapter]:
        """parte-All: Returns all stored queues."""
        return dict(self.queues)
    
    def clear_all(self) -> None:
        """parte-Clear: Removes all queues from storage (useful for reset/cleanup)."""
        self.queues.clear()
    
    @classmethod
    def reset_instance(cls) -> None:
        """parte-Reset: Resets the singleton instance (for testing purposes)."""
        cls._instance = None
