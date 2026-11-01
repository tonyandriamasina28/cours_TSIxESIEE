# Coursework: TSI x ESIEE

Operating systems and Python exercises from my TSI and ESIEE courses.

## Contents

| Folder | Topic |
|---|---|
| `OS_Assignment1` | System information |
| `OS_Assignment2` | File metadata and permissions |
| `OS_Assignment3` | Processes and IPC with `Pipe` |
| `OS_Assignment4` | Race conditions and locks |
| `TSI_class-lab-02-sigterm` | SIGTERM, SIGKILL and process cleanup (course starter code, TODOs completed) |
| `TSI_class-lab-03-zerocopy` | Queue vs shared-memory IPC (course starter code, TODOs completed) |
| `ESIEE_python_workshop` | Python basics and classes (course material, `tasks.py` completed) |

## Lab 03 results

Three runs on WSL2 Debian with Python 3.12 and NumPy 2.5, transferring a 477 MiB array:

| Method | Total time |
|---|---|
| `multiprocessing.Queue` | 5.7 to 8.9 s |
| Shared memory | 0.26 to 1.9 s |

## Changes to the starter code

- **Lab 02:** the worker starts in its own session, so Ctrl+C reaches only the manager and the SIGTERM path actually runs.
- **Lab 03:** `OPENBLAS_NUM_THREADS=1` stops NumPy from using up the memory limit on machines with many cores.
- **Lab 03, Queue:** the memory limit goes from 1.2 GB to 2.5 GB, because the array and its pickled copy did not fit.
- **ESIEE:** `superheroes.py` crashed because the IronMan example was missing the `alignment` argument.

Labs 02 and 03 need Linux because they use the `resource` module.

## Credits and licenses

- TSI labs: course repository [`maksim-tsi/os-course-illustrative`](https://github.com/maksim-tsi/os-course-illustrative), MIT license (see each lab's `LICENSE`).
- ESIEE workshop: [`pirrencode/esiee_workshop`](https://github.com/pirrencode/esiee_workshop), GPL-3.0 license (see `ESIEE_python_workshop/LICENSE`).
