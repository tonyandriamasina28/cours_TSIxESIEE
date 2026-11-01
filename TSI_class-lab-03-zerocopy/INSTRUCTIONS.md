# Lab 03 Instructions: High-Performance Zero-Copy AI Pipeline

Welcome to Lab 03! In this lab, you will learn how to use zero-copy shared memory to efficiently pass large tensors between processes. Follow these instructions carefully to set up your environment, write the code, and benchmark your solution.

## 1. Setting up the GitHub Codespaces Environment

For this lab, we will use the default GitHub Codespaces environment.

1. Navigate to the root of the repository on GitHub.
2. Click the green **Code** button.
3. Switch to the **Codespaces** tab.
4. Click **Create codespace on main** (or your working branch).
5. Wait for the VS Code web editor to fully load.

## 2. Navigating to the Code

1. In the Explorer pane on the left side of the VS Code editor, expand the `class-lab-03-zerocopy` folder.
2. Expand the `task/` folder.
3. You will primarily be editing two files: `queue_benchmark.py` and `zerocopy_manager.py`.

> [!WARNING]
> Do NOT look in the `solution/` directory. The goal of this lab is to write the solution yourself!

## 3. Editing the Code

In both scripts, look for the comments marked with `TODO`. These comments provide hints on what code you need to write.

- In `queue_benchmark.py`, you will implement a traditional multiprocessing queue.
- In `zerocopy_manager.py`, you will implement zero-copy IPC using `multiprocessing.shared_memory`.
- Write your implementation directly below the `TODO` markers.

> [!TIP]
> **VS Code Linter Tip:** 
> Because this lab uses NumPy within an isolated virtual environment, your IDE might initially show an "import 'numpy' could not be resolved" warning. 
> To fix this:
> 1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac).
> 2. Type and select `Python: Select Interpreter`.
> 3. Click `Enter interpreter path...` and choose `./class-lab-03-zerocopy/venv/bin/python`.
> This ensures the IDE correctly resolves the `numpy` import!

## 4. Execution Workflow

To execute and test your code, we will use the provided `Makefile`.

1. Open the built-in VS Code Terminal by pressing `` Ctrl+` `` (Control and backtick) or selecting **Terminal > New Terminal** from the top menu.
2. Ensure you are in the correct directory:
   ```bash
   cd class-lab-03-zerocopy
   ```

### Step A: Setup the Virtual Environment
This lab requires `numpy`. We use a virtual environment for dependency isolation.
Run the following command to create the virtual environment and install dependencies:
```bash
make venv
```

### Step B: Run the Queue Benchmark (Baseline)
To observe the performance of traditional IPC (Pickling), run:
```bash
make run-queue
```
Note the latency and CPU usage. It will likely take a few seconds due to serialization overhead.

### Step C: Run the Zero-Copy Implementation
After you have completed the `TODO`s in `zerocopy_manager.py`, run your high-performance implementation:
```bash
make run-zerocopy
```
Compare the latency to the queue benchmark. The zero-copy version should transfer the tensor almost instantly!

### Step D: Clean Up
Once you are done testing, clean up the virtual environment and cache files by running:
```bash
make clean
```
