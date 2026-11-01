# Lab 02 Instructions: AI Worker Process Manager

Welcome to Lab 02! In this lab, you will learn how to handle OS process creation and termination. Follow these instructions carefully to set up your environment, write the code, and test your solution.

## 1. Setting up the GitHub Codespaces Environment

For this lab, we will use the default GitHub Codespaces Python environment. You do **not** need a custom `.devcontainer.json`. Python 3 and `make` are pre-installed and ready to use.

1. Navigate to the root of the repository on GitHub.
2. Click the green **Code** button.
3. Switch to the **Codespaces** tab.
4. Click **Create codespace on main** (or your working branch).
5. Wait for the VS Code web editor to fully load.

## 2. Navigating to the Code

1. In the Explorer pane on the left side of the VS Code editor, expand the `class-lab-02-sigterm` folder.
2. Expand the `task/` folder.
3. Open `agent_manager.py`.

> [!WARNING]
> Do NOT look in the `solution/` directory. The goal of this lab is to write the solution yourself!

## 3. Editing the Code

In `agent_manager.py`, look for the comments marked with `TODO`. These comments provide hints on what code you need to write.

- You will need to use the `subprocess` and `signal` modules.
- Write your implementation directly below the `TODO` markers.

## 4. Execution Workflow

To execute and test your code, we will use the provided `Makefile`.

1. Open the built-in VS Code Terminal by pressing `` Ctrl+` `` (Control and backtick) or selecting **Terminal > New Terminal** from the top menu.
2. Ensure you are in the correct directory:
   ```bash
   cd class-lab-02-sigterm
   ```

### Step A: Setup (Data Generation)
Before running the code, you need to generate the dummy dataset for the AI worker.
Run the following command:
```bash
make setup
```
*Note: This command only generates `dataset.bin`. It does not create a virtual environment, as we are demonstrating that standard OS features work natively.*

### Step B: Run the Manager
To execute your code, run:
```bash
make run
```
Let the process run for a few seconds.

### Step C: Test the Signals
To test if your signal handling works:
1. While `make run` is actively executing, click inside the terminal window.
2. Press `Ctrl+C`.
3. Watch the console output:
   - Did your manager catch the signal?
   - Did it send `SIGTERM`?
   - Did the child process clean up and exit gracefully, or did it require a forceful `SIGKILL`?

### Step D: Clean Up
Once you are done testing, clean up the generated data and cache files by running:
```bash
make clean
```
