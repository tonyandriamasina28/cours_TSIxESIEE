import platform
import os
import getpass

# Assignment 1 - Basic System Information

print("=== Basic System Information ===")

# Operating system and kernel
print("Operating System:", platform.system())
print("Kernel Version:", platform.release())

# Current user
print("Current User:", getpass.getuser())

# Current working directory
print("Current Working Directory:", os.getcwd())