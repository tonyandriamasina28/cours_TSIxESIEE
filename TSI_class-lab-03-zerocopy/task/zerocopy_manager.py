import time
import multiprocessing
from multiprocessing import shared_memory
import resource
import os

# OpenBLAS reserves address space per CPU core when NumPy is imported. On a
# machine with many cores this uses up the limit below, so keep a single thread.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np

# --- Guardrails ---
# Limit memory to ~1.2GB to prevent accidental OOM crashes
GB = 1024 * 1024 * 1024
try:
    resource.setrlimit(resource.RLIMIT_AS, (int(1.2 * GB), int(1.2 * GB)))
except ValueError:
    pass # macOS might restrict this, ignore if it fails

def producer(shm_name, sync_event, shape, dtype):
    """
    Producer: Maps shared memory, creates a NumPy array backed by it, and fills it.
    """
    print(f"[Producer] Attaching to shared memory block: {shm_name}")
    existing_shm = shared_memory.SharedMemory(name=shm_name)

    try:
        data = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)

        print("[Producer] Filling 500MB array directly in shared memory...")
        # Fill the array with ones
        data[:] = 1.0

        print("[Producer] Data is ready. Signaling Consumer.")
        sync_event.set()

        # The array holds a view on the buffer: close() fails while it exists.
        del data

    finally:
        # Close the local handle to the shared memory block
        existing_shm.close()

def consumer(shm_name, sync_event, shape, dtype):
    """
    Consumer: Waits for the signal, then maps the shared memory to read the array.
    """
    print("[Consumer] Waiting for Producer to finish writing (Traffic Light)...")
    # Guardrail against deadlocks: wait() returns False when the timeout expires
    if not sync_event.wait(timeout=15):
        raise TimeoutError("Producer did not signal within 15 seconds")

    print(f"[Consumer] Signal received! Attaching to shared memory: {shm_name}")
    existing_shm = shared_memory.SharedMemory(name=shm_name)

    try:
        data = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)

        # Verify data
        print(f"[Consumer] Successfully read array. First element: {data[0]}, Last element: {data[-1]}")
        del data
    finally:
        # Close the local handle to the shared memory block
        existing_shm.close()

if __name__ == '__main__':
    print("=== Zero-Copy IPC Benchmark (Shared Memory) ===")

    # 500MB array (approx 62.5 million 64-bit floats)
    elements = 62500000
    shape = (elements,)
    dtype = np.float64
    bytes_required = elements * np.dtype(dtype).itemsize

    print(f"[Main] Requesting {bytes_required / (1024**2):.2f} MB of Shared Memory from OS...")

    # The OS assigns a unique name, which the children use to attach to the block
    shm = shared_memory.SharedMemory(create=True, size=bytes_required)

    # CRITICAL: We use try...finally to ensure cleanup.
    # Without this, if the script crashes, the OS will permanently leak 500MB of RAM!
    try:
        sync_event = multiprocessing.Event()

        print(f"[Main] Shared Memory allocated: {shm.name}")

        args = (shm.name, sync_event, shape, dtype)
        producer_process = multiprocessing.Process(target=producer, args=args)
        consumer_process = multiprocessing.Process(target=consumer, args=args)

        print("[Main] Starting processes...")
        start_time = time.time()

        producer_process.start()
        consumer_process.start()

        producer_process.join()
        consumer_process.join()

        end_time = time.time()

        if producer_process.exitcode != 0 or consumer_process.exitcode != 0:
            raise RuntimeError("Producer or Consumer failed, see the error above")

        print(f"\n[Result] Total time taken: {end_time - start_time:.4f} seconds")
        print("[Notice] Look at that speed! No pickling, no serialization overhead.")

    finally:
        print("\n[Main] Performing CRITICAL cleanup of Shared Memory...")
        # CRITICAL GUARDRAIL: Close the local handle and unlink (delete) the block from the OS
        shm.close()
        shm.unlink()
