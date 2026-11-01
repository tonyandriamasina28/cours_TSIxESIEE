# Lab 09: High-Performance Zero-Copy AI Pipeline

## 🎯 Objective
Master high-performance Inter-Process Communication (IPC) by building a data pipeline for massive AI Tensors. 
You will compare the traditional "Pickle-based" message passing with modern **Zero-Copy Shared Memory** techniques using Python's `multiprocessing.shared_memory` and `NumPy`.

## 📖 The Scenario
In modern AI infrastructure, moving a 500MB or 1GB tensor between a data loader process and a model inference process can become a massive bottleneck. 
* **The Problem:** Traditional IPC (Pipes, Queues) serializes data into bytes (Pickling), which consumes 100% CPU and creates significant latency.
* **The Solution:** Use Shared Memory to allow both processes to "see" the same RAM buffer, eliminating the need to copy or translate data.

## 📂 Directory Structure
* `task/` - Contains the starter code with `TODO` markers.
* `solution/` - Reference implementation for post-lab review.
* `Makefile` - Automation for environment setup and cleanup.

---

## 🛠️ Step-by-Step Instructions

### Step 1: The "Pickle Penalty" (Baseline)
**Goal:** Observe why standard Queues are slow for large data.
* Open `task/queue_benchmark.py`.
* Implement a simple `multiprocessing.Queue` to send a 500MB NumPy array from a Producer to a Consumer.
* Run the script and observe the **Latency** and **CPU Usage**. 
* *Note:* You will notice the system "freezes" for a few seconds while Python serializes (Pickles) the massive array.

### Step 2: Implementing Zero-Copy Shared Memory
**Goal:** Share the raw memory buffer between processes.
* Open `task/zerocopy_manager.py`.
* **TODO 1:** Create a named shared memory block using `multiprocessing.shared_memory.SharedMemory`.
* **TODO 2:** Create a NumPy array that uses this shared memory block as its underlying buffer (`buffer=shm.buf`).
* **TODO 3:** In the Consumer process, attach to the *same* named memory block and reconstruct the NumPy array without copying any data.

### Step 3: Synchronization (The Traffic Light)
**Goal:** Prevent Race Conditions.
* Shared memory is fast but "dumb"—it doesn't know when the Producer is finished writing.
* **TODO 4:** Implement a `multiprocessing.Event`. 
* The Consumer must `wait()` until the Producer signals that the data is ready.
* This ensures the Consumer doesn't read a half-written, corrupted tensor.

---

## ⚠️ Critical Guardrails: Memory Cleanup
Unlike standard Python variables, **Shared Memory is managed by the OS kernel**. 
* If your script crashes or you forget to close it, the 500MB block will **stay in your RAM forever** (a memory leak).
* **Requirement:** You MUST implement a `try...finally` block to ensure `shm.close()` and `shm.unlink()` are called, even if an error occurs.

## 🚀 How to Run
1. Setup environment: `make setup`
2. Run benchmark (Slow): `python3 task/queue_benchmark.py`
3. Run Zero-Copy (Fast): `python3 task/zerocopy_manager.py`
4. Clean up: `make clean`

**Success Criteria:** The Zero-Copy version should transfer the 500MB tensor in **less than 0.1 seconds**, whereas the Queue version will likely take several seconds.