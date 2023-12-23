import numpy as np


import asyncio
from collections import deque
from multiprocessing.shared_memory import SharedMemory


class FramesDepot:
    """
    A class for storing and managing frames in a shared memory space with controlled access.

    Attributes:
        max_size (int): The maximum number of frames to store in the queue.
        queue (deque): A fixed-size queue to hold the frames.
        index (dict): A dictionary to index frames by their frame number.
        _last_requested_frame (int): The last frame number requested.
        enqueue_lock (asyncio.Lock): A lock to ensure one frame is added at a time.
        __mem_size (int): The size of the shared memory block.
        __shared_memory (SharedMemory): The shared memory object.
        dropped_frames (int): The number of frames dropped due to a full queue.
        backpressure_callback (function): Optional callback function to execute when the queue is full.

    Methods:
        __init__(frame_size, memory_name, max_size, backpressure_callback): Initializes the FramesDepot.
        __len__(): Returns the number of frames in the queue.
        __del__(): Ensures resources are released upon deletion of the object.
        __init_shared_memory(memory_name): Initializes shared memory.
        queue_is_full: Property that indicates if the queue is full.
        enqueue(frame_dict): Adds a frame to the queue and shared memory.
        get_frame(frame_number): Retrieves a specific frame by number.
        clear_queue(): Clears the queue and frame index.
        close(): Closes and releases all resources.
    """

    def __init__(
        self,
        frame_size: tuple[int, int, int],
        memory_name: str,
        max_size: int = 10,
        backpressure_callback=None,
    ):
        """
        Initializes the FramesDepot object with the given parameters.

        Args:
            frame_size (tuple[int, int, int]): The dimensions of the frames (width, height, channels).
            memory_name (str): The name of the shared memory block.
            max_size (int): The maximum number of frames to store in the queue.
            backpressure_callback (function): Optional callback function to execute when the queue is full.
        """
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)
        self.index = {}  # Un dizionario per indicizzare i frame per numero di frame
        self._last_requested_frame: int = -1
        self.enqueue_lock = asyncio.Lock()
        self.__mem_size = frame_size[0] * frame_size[1] * frame_size[2]
        self.__shared_memory = self.__init_shared_memory(memory_name)
        self.dropped_frames = 0
        self.backpressure_callback = backpressure_callback

    def __len__(self):
        """Returns the number of frames currently in the queue."""
        return len(self.queue)

    def __del__(self):
        """Ensures resources are released properly when the object is deleted."""
        self.close()

    def __init_shared_memory(self, memory_name):
        """
        Initializes or connects to shared memory with the given name.

        Args:
            memory_name (str): The name of the shared memory block.

        Returns:
            SharedMemory: The initialized shared memory object.
        """
        try:
            return SharedMemory(name=memory_name, create=True, size=self.__mem_size)
        except FileExistsError:
            return SharedMemory(name=memory_name)

    @property
    def queue_is_full(self):
        """Indicates whether the queue is full."""
        return len(self.queue) >= self.max_size

    async def enqueue(self, frame_dict: dict[int, np.ndarray]):
        """
        Asynchronously adds a frame to the queue and shared memory.

        Args:
            frame_dict (dict[int, np.ndarray]): A dictionary containing the frame number and frame data.

        If the queue is full, it increments the dropped_frames count and optionally calls the backpressure_callback.
        """
        async with self.enqueue_lock:  # Assicura che un solo frame sia aggiunto alla volta
            if self.queue_is_full:
                self.dropped_frames += 1
                if self.backpressure_callback:
                    await self.backpressure_callback()
                return
            frame_number = int(frame_dict["frame_number"])

            # Aggiungi il frame al dizionario di indicizzazione e alla coda
            self.index[frame_number] = frame_dict["frame"]
            self.queue.append(frame_dict)

            # Rimuovi il frame più vecchio dall'indice se necessario
            if len(self.queue) > self.max_size:
                oldest_frame = next(iter(self.index))
                del self.index[oldest_frame]

    def get_frame(self, frame_number: int):
        """
        Retrieves a specific frame by number and updates the shared memory with its data.

        Args:
            frame_number (int): The number of the frame to retrieve.
        """
        self._last_requested_frame = frame_number  # Aggiorna l'ultimo frame richiesto
        frame: np.ndarray = self.index.get(frame_number, None)
        self.__shared_memory.buf[: self.__mem_size] = bytearray(frame)
        while self.queue and self.queue[0]["frame_number"] <= frame_number:
            removed_frame = self.queue.popleft()
            del self.index[removed_frame["frame_number"]]

    async def clear_queue(self):
        """Asynchronously clears the frame queue and index."""
        async with self.enqueue_lock:
            self.queue.clear()
            self.index.clear()
            self._last_requested_frame = -1
        print("The queue and index have been emptied.")

    async def close(self):
        """
        Asynchronously closes and releases all resources, including shared memory.
        """
        async with self.enqueue_lock:
            await self.clear_queue()  # Prima svuota la coda e l'indice
            self.__shared_memory.close()  # Chiudi la memoria condivisa
            self.__shared_memory.unlink()  # Scollega la memoria condivisa, se necessario
        print("All resources have been released.")
