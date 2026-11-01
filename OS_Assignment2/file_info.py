import os
import stat

# Ask user for directory path
directory = input("Enter directory path: ")

# Verify directory exists
if not os.path.isdir(directory):
    print("Directory not found.")
else:
    print("\nFiles in directory:\n")

    for item in os.listdir(directory):

        full_path = os.path.join(directory, item)

        if os.path.isfile(full_path):

            file_stats = os.stat(full_path)

            size = file_stats.st_size

            permissions = ""

            permissions += "R " if os.access(full_path, os.R_OK) else "- "
            permissions += "W " if os.access(full_path, os.W_OK) else "- "
            permissions += "X" if os.access(full_path, os.X_OK) else "-"

            print(f"File: {item}")
            print(f"Size: {size} bytes")
            print(f"Permissions: {permissions}")
            print("----------------------")