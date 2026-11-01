"""
Educational Lab: Operating Systems - Process Management & Signals
This script simulates a memory-bounded AI worker process that reads a large
dataset. It demonstrates how to enforce resource limits (RLIMIT_AS) and how
to handle signals (SIGTERM) with branching logic (clean exit vs deadlock).
"""

import os
import time
import signal
import resource
import random
import sys

# Limit memory to 50MB (50 * 1024 * 1024 bytes)
MAX_MEMORY = 50 * 1024 * 1024
try:
    # Set the soft and hard limits for the address space (RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
except Exception as e:
    print(f"AI Worker: Failed to set memory limit: {e}")

# Handle SIGTERM gracefully or simulate a bug (deadlock)
def sigterm_handler(signum, frame):
    """
    Signal handler for SIGTERM.
    We introduce randomness to simulate a flaky application that sometimes
    deadlocks instead of shutting down cleanly.
    """
    # 50% chance to exit cleanly, 50% chance to hallucinate/deadlock
    if random.choice([True, False]):
        print(f"\nAI Worker [{os.getpid()}]: Received SIGTERM, shutting down cleanly.")
        sys.exit(0)
    else:
        print(f"\nAI Worker [{os.getpid()}]: Ignoring SIGTERM (hallucinating)...")
        # Enter an infinite loop to simulate a process that is stuck
        # and won't terminate even after receiving SIGTERM.
        while True:
            time.sleep(9999)

# Register the signal handler for SIGTERM
signal.signal(signal.SIGTERM, sigterm_handler)

def main():
    pid = os.getpid()
    
    try:
        # Open the dataset and read it in 1MB chunks to avoid loading
        # the entire 500MB file into memory (which would exceed our 50MB limit and cause OOM).
        with open("dataset.bin", "rb") as f:
            while True:
                chunk = f.read(1024 * 1024) # Read 1MB chunk
                if not chunk:
                    # EOF reached, loop back to the start to simulate continuous processing
                    f.seek(0)
                    continue
                print(f"AI Worker [{pid}]: Processing dataset...")
                time.sleep(1) # Simulate some processing time
    except FileNotFoundError:
        print(f"AI Worker [{pid}]: dataset.bin not found! Please run 'make setup' first.")
        sys.exit(1)

if __name__ == "__main__":
    main()
