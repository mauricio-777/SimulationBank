# Entity: priority queue (min-heap) with FIFO tie-breaking
# Allows O(log n) insertion and extraction of highest-priority customer
# Respects FIFO order within each priority level using arrival_sequence

from typing import Optional, List
from src.shared.domain.entity import Entity
from src.customer.domain.customer import Customer
from src.queue.domain.queue_node import QueueNode
from src.queue.domain.queue_policy import QueuePolicy, TieBreakerStrategy


# parte-PriorityQueue: Main queue entity managing binary heap operations
class PriorityQueue(Entity):
    """
    Entity: Priority queue implementation using binary heap (min-heap).
    
    Characteristics:
    - Insertion (enqueue): O(log n) using heapify-up
    - Extraction (dequeue): O(log n) using heapify-down
    - Tie-breaking: FIFO within same priority level using arrival_sequence
    - Capacity management: Optional max_queue_size with rejection policy
    
    The queue respects:
    1. Primary ordering: Customer priority (1=highest, 3=lowest)
    2. Secondary ordering: Customer arrival_time (FIFO within same priority)
    """
    
    def __init__(self, queue_id: str, policy: QueuePolicy):
        super().__init__(entity_id=queue_id)
        self.policy = policy
        self.heap: List[QueueNode] = []  # Binary heap storage
        self.sequence_counter: int = 0  # Counter for arrival_sequence ordering
    
    def enqueue(self, customer: Customer) -> bool:
        """
        parte-Enqueue: Adds a customer to the queue respecting priority and capacity.
        Uses heapify-up algorithm to maintain heap property.
        
        Args:
            customer: The customer to add to the queue
        
        Returns:
            True if customer was successfully enqueued
            False if customer was rejected (capacity exceeded with rejections enabled)
        """
        # Check capacity limits and rejection policy
        if self.policy.should_reject(len(self.heap)):
            return False  # Customer rejected due to capacity constraint
        
        # Create node with current sequence counter to ensure FIFO within priority
        node = QueueNode(
            customer=customer,
            arrival_sequence=self.sequence_counter
        )
        self.sequence_counter += 1
        
        # Add to end of heap and bubble up
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)
        
        return True  # Customer successfully enqueued
    
    def dequeue(self) -> Optional[Customer]:
        """
        parte-Dequeue: Extracts the customer with highest priority (lowest priority number).
        Uses heapify-down algorithm to maintain heap property.
        Returns None if queue is empty.
        
        Returns:
            The Customer object with highest current priority, or None if queue is empty
        """
        if not self.heap:
            return None
        
        # Extract root (highest priority element)
        best_node = self.heap[0]
        
        # Move last element to root and bubble down
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            self._heapify_down(0)
        else:
            self.heap.pop()
        
        return best_node.customer
    
    def peek(self) -> Optional[Customer]:
        """
        parte-Peek: Returns the customer with highest priority WITHOUT removing them.
        Useful for lookahead operations.
        
        Returns:
            The Customer with highest current priority, or None if queue is empty
        """
        if not self.heap:
            return None
        return self.heap[0].customer
    
    def is_empty(self) -> bool:
        """parte-Empty: Checks if queue has no customers."""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """parte-Size: Returns the number of customers currently in queue."""
        return len(self.heap)
    
    def _heapify_up(self, index: int) -> None:
        """
        parte-HeapifyUp: Restores min-heap property after insertion.
        Bubbles element at 'index' upward until heap property is satisfied.
        Ensures parent has higher priority (lower value) than children.
        
        Time complexity: O(log n)
        """
        while index > 0:
            parent_index = (index - 1) // 2
            parent_node = self.heap[parent_index]
            current_node = self.heap[index]
            
            # If current has higher priority than parent, swap and continue
            if current_node < parent_node:
                self.heap[index], self.heap[parent_index] = parent_node, current_node
                index = parent_index
            else:
                break
    
    def _heapify_down(self, index: int) -> None:
        """
        parte-HeapifyDown: Restores min-heap property after removal.
        Bubbles element at 'index' downward until heap property is satisfied.
        Ensures parent has higher priority (lower value) than children.
        
        Time complexity: O(log n)
        """
        while True:
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            
            # Check if left child has higher priority
            if (left_child < len(self.heap) and
                self.heap[left_child] < self.heap[smallest]):
                smallest = left_child
            
            # Check if right child has higher priority
            if (right_child < len(self.heap) and
                self.heap[right_child] < self.heap[smallest]):
                smallest = right_child
            
            # If smallest is not current node, swap and continue
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break
