import threading
import time

THREADS = 4
INCREMENTS = 1_000_000

counter = 0


# -------------------------
# PART 1 — WITHOUT LOCK
# -------------------------

def increment_without_lock():
    global counter

    for _ in range(INCREMENTS):

        temp = counter
        temp += 1

        # Force context switching between the read and the write:
        # another thread can update counter here, and that update is then lost
        if _ % 1000 == 0:
            time.sleep(0)

        counter = temp


# -------------------------
# PART 2 — WITH LOCK
# -------------------------

lock = threading.Lock()


def increment_with_lock():
    global counter

    for _ in range(INCREMENTS):

        with lock:
            counter += 1


def run_without_lock():

    global counter
    counter = 0

    threads = []

    print("\nPART 1 — Race Condition\n")

    for i in range(THREADS):

        t = threading.Thread(
            target=increment_without_lock,
            name=f"Thread-{i+1}"
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Expected Result: {THREADS * INCREMENTS}")
    print(f"Actual Result:   {counter}")


def run_with_lock():

    global counter
    counter = 0

    threads = []

    print("\nPART 2 — Using Lock\n")

    for i in range(THREADS):

        t = threading.Thread(
            target=increment_with_lock,
            name=f"Thread-{i+1}"
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Expected Result: {THREADS * INCREMENTS}")
    print(f"Actual Result:   {counter}")


if __name__ == "__main__":

    run_without_lock()

    run_with_lock()