# Lab 08: AI Worker Process Manager (SIGTERM vs SIGKILL)

## 🎯 Objective
Build a Python Process Manager for a simulated "AI Worker". 
In this lab, you will apply core Operating System concepts including `fork/exec` (via Python's `subprocess`), PID tracking, and Asynchronous Signal handling.

## 📖 The Scenario
Imagine you have a background AI agent that continuously processes data. However, occasionally this AI worker "hallucinates", enters an infinite loop, and completely freezes. 

Your job is to write a system-level **Process Manager** script that:
1. Launches this AI worker in the background.
2. Monitors it concurrently.
3. Knows how to gracefully shut it down when the user requests it.
4. Forcefully annihilates the worker if it refuses to shut down (deadlock).

## 📂 Directory Structure
* `task/` - Contains the starter code. **You will write your code here.** (Look for the `TODO` comments).
* `solution/` - Contains the reference solution. Try not to look at this until you've solved it yourself!
* `dummy_ai_worker.py` - A simulated AI process that we have provided for you. It mimics both normal work and sudden deadlocks.

---

## 🛠️ Step-by-Step Instructions

### Step 1: Spawning the Process
**Goal:** Create a background child process without blocking the parent.
* Open `task/agent_manager.py`.
* Use the OS module (`subprocess.Popen`) to launch `dummy_ai_worker.py` as a background child process.
* Retrieve the unique Process ID (`pid`) from the OS kernel using the process object.
* Ensure your parent process continues running concurrently (do not use `.run()` or `.call()` which block the parent).

### Step 2: Signal Handling (The Polite Request)
**Goal:** Rewrite the OS default behavior for `Ctrl+C`.
* Usually, pressing `Ctrl+C` instantly kills your program. We want to trap this!
* Register a signal handler using the `signal` module to intercept `Ctrl+C` (`signal.SIGINT`) from the user.
* Inside your handler, delegate the signal: use `os.kill(pid, signal.SIGTERM)` to send a polite termination request to the child process.
* This allows the AI worker to finish its current loop, save its data, and exit cleanly.

### Step 3: The SIGKILL Fallback (The Hammer)
**Goal:** Prevent zombies and handle deadlocks.
* What happens if the AI worker is completely frozen in an infinite loop? It will ignore your polite `SIGTERM`.
* In your signal handler, after sending `SIGTERM`, use the process object's `.wait(timeout=2)` method.
* Give the process exactly **2 seconds** to shut down.
* If it throws a `TimeoutExpired` exception (meaning it refused to exit), escalate the situation: send a `signal.SIGKILL` to forcefully annihilate the process at the kernel level.

---

## 🚀 How to Run and Test
1. Navigate to the `task/` directory.
2. Run your manager: `python3 agent_manager.py`
3. Let it run for a few seconds so the AI worker starts "processing".
4. Press `Ctrl+C`. 
5. Observe the console output:
   * Did the parent catch the signal?
   * Did it send a `SIGTERM`?
   * Did the child exit gracefully, or did it require a `SIGKILL`?

*Note: This 2-second fallback logic is exactly how modern container engines like Docker implement the `docker stop` command under the hood!*