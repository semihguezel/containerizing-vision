import queue
import threading


class FrameQueueHandler:
    def __init__(self, max_size=10):
        """
        Initialize FrameQueueHandler.

        This class is designed to handle a thread-safe queue for storing frames.

        Args:
        - max_size (int): Maximum size of the frame queue.
        """
        self.max_size = max_size
        # Initialize a thread-safe queue
        self.queue = queue.Queue(maxsize=max_size)
        # Initialize a lock for thread safety
        self.lock = threading.Lock()

    def put(self, frame):
        """
        Put a frame into the queue.

        This method puts a frame into the queue, and if the queue is full, it removes the oldest frame to make space.

        Args:
        - frame: The frame to be put into the queue.
        """
        with self.lock:
            if self.queue.qsize() < self.max_size:
                self.queue.put(frame)
            else:
                # Remove the oldest frame
                self.queue.get()
                self.queue.put(frame)

    def get(self):
        """
        Get a frame from the queue.

        This method retrieves a frame from the queue. If the queue is empty, it returns None.

        Returns:
        - frame: The retrieved frame or None if the queue is empty.
        """
        with self.lock:
            if not self.queue.empty():
                return self.queue.get()
            else:
                return None
