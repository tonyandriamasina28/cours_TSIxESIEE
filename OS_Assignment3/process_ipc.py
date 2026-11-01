from multiprocessing import Process, Pipe
import os


def child_process(connection):

    child_pid = os.getpid()

    print(f"\nChild [PID {child_pid}] waiting for data...")

    # Receive data from parent
    received = connection.recv()

    print(f"Child [PID {child_pid}] received: {received}")

    # Transform data
    result = received.upper()

    print(f"Child [PID {child_pid}] processed data: {result}")

    # Send back
    connection.send(result)

    connection.close()


if __name__ == "__main__":

    parent_pid = os.getpid()

    parent_conn, child_conn = Pipe()

    process = Process(
        target=child_process,
        args=(child_conn,)
    )

    process.start()

    message = input("Enter a message: ")

    print(f"\nParent [PID {parent_pid}] sending data...")

    parent_conn.send(message)

    result = parent_conn.recv()

    print(f"\nParent [PID {parent_pid}] received: {result}")

    process.join()

    print("\nCommunication completed.")