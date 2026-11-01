"""
Educational Lab: Operating Systems - Process Management & Signals
This script acts as the "Manager" process. It spawns a worker process and
demonstrates how to gracefully handle signals (like Ctrl+C) to terminate
child processes, with a fallback to forceful termination (SIGKILL) if the
child becomes unresponsive.
"""

import os
import signal
import subprocess
import time
import sys

# Hardcoded absolute timeout to prevent the script from running forever
# This acts as a guardrail in case the lab is left running in a Codespace.
ABSOLUTE_TIMEOUT = 60

# Global process variable so it can be accessed inside signal handlers
worker_process = None

def handle_sigint(signum, frame):
    """
    Signal handler for SIGINT (Ctrl+C).
    """
    print("\nManager: Caught SIGINT (Ctrl+C). Initiating graceful shutdown...")

    # Step 2: Politely ask the child to stop.
    print(f"Manager: Sending SIGTERM to worker {worker_process.pid}")
    os.kill(worker_process.pid, signal.SIGTERM)

    # Step 3: Give it 2 seconds, then force it. SIGKILL cannot be caught or
    # ignored, so it also ends a worker stuck in its SIGTERM handler.
    try:
        worker_process.wait(timeout=2)
        print("Manager: Worker exited after SIGTERM.")
    except subprocess.TimeoutExpired:
        print("Manager: Worker did not exit in time. Sending SIGKILL.")
        os.kill(worker_process.pid, signal.SIGKILL)
        # Collect the exit status so the child does not remain a zombie.
        worker_process.wait()
        print("Manager: Worker killed.")

    print("Manager: Shutdown complete. Exiting.")
    sys.exit(0)

def main():
    global worker_process
    print(f"Manager [PID {os.getpid()}]: Starting up...")

    # Step 1: Spawn the worker in the background.
    # A new session keeps the worker out of the terminal's foreground process
    # group; otherwise Ctrl+C would send SIGINT to it too, before the SIGTERM.
    worker_process = subprocess.Popen(
        [sys.executable, "dummy_ai_worker.py"],
        start_new_session=True,
    )
    print(f"Manager: Spawned worker with PID {worker_process.pid}")

    # Register the SIGINT handler
    signal.signal(signal.SIGINT, handle_sigint)

    print(f"Manager: Running. Press Ctrl+C to stop. Hard timeout in {ABSOLUTE_TIMEOUT} seconds.")
    start_time = time.time()

    # Main loop - waiting for the absolute timeout or a manual interrupt
    while True:
        if time.time() - start_time > ABSOLUTE_TIMEOUT:
            print("Manager: Absolute timeout reached. Forcibly terminating worker.")
            # Guardrail: Forcefully kill the child process if the timeout is reached
            if worker_process:
                worker_process.kill()
                worker_process.wait()
            break
        time.sleep(1)

    print("Manager: Exiting due to timeout.")

if __name__ == "__main__":
    main()
