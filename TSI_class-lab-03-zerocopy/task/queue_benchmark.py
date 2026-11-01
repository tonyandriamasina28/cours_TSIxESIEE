import time
import multiprocessing
import resource
import sys
import threading
import os

# OpenBLAS reserves address space per CPU core when NumPy is imported. On a
# machine with many cores this uses up the limit below, so keep a single thread.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np

# --- Guardrails ---
# Limit memory to prevent accidental OOM crashes during the lab.
# Raised from the original 1.2GB: the array plus its pickled copy did not fit,
# so the Queue's feeder thread failed and the Consumer never received anything.
GB = 1024 * 1024 * 1024
try:
    resource.setrlimit(resource.RLIMIT_AS, (int(2.5 * GB), int(2.5 * GB)))
except ValueError:
    pass # macOS might restrict this, ignore if it fails

# --- Helper ---
def progress_spinner(stop_event):
    """A simple background thread to show the system is busy (blocking)."""
    spinner = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r[System] Pickling and transferring 500MB array... {spinner[i % 4]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r[System] Transfer complete!                           \n")

def producer(q):
    """
    Producer: Generates a massive 500MB NumPy array and sends it via Queue.
    """
    print("[Producer] Generating 500MB NumPy array...")
    # Generate 500MB array (approx 62.5 million 64-bit floats)
    data = np.ones(62500000, dtype=np.float64)
    print(f"[Producer] Array generated. Size in memory: {data.nbytes / (1024**2):.2f} MB")

    # Notice how the program "hangs" here. This is the Pickle Penalty!
    q.put(data)

def consumer(q):
    """
    Consumer: Receives the array from the Queue.
    """
    print("[Consumer] Waiting for data from Producer...")

    # Guardrail against deadlocks: raises queue.Empty if nothing ever arrives
    data = q.get(timeout=60)
    print(f"\n[Consumer] Received array. First element: {data[0]}, Last element: {data[-1]}")

if __name__ == '__main__':
    print("=== IPC Queue Benchmark (The Pickle Penalty) ===")

    q = multiprocessing.Queue()

    producer_process = multiprocessing.Process(target=producer, args=(q,))
    consumer_process = multiprocessing.Process(target=consumer, args=(q,))

    print("[Main] Starting processes...")
    start_time = time.time()

    # Start the visual spinner to show the blocking behavior
    spinner_stop = threading.Event()
    spinner_thread = threading.Thread(target=progress_spinner, args=(spinner_stop,))
    spinner_thread.start()

    producer_process.start()
    consumer_process.start()

    # Join the consumer first: the producer cannot exit until the queue's
    # feeder thread has pushed all its data through the pipe.
    consumer_process.join()
    producer_process.join()

    # Stop the spinner
    spinner_stop.set()
    spinner_thread.join()

    end_time = time.time()

    if producer_process.exitcode != 0 or consumer_process.exitcode != 0:
        sys.exit("[Error] Producer or Consumer failed, see the error above")

    print(f"\n[Result] Total time taken: {end_time - start_time:.2f} seconds")
    print("[Notice] Did you see the delay? That's the CPU struggling to serialize (pickle)")
    print("         and deserialize 500MB of data through a standard pipe.")
