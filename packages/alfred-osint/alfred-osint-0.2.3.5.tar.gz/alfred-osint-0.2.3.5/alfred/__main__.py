#! /usr/bin/env python3

"""
Alfred: Alfred is an advanced OSINT information gathering tool
"""

import os
import sys
import subprocess


def check_python_version():
    required_version = (3, 10)
    current_version = sys.version_info
    if current_version < required_version:
        version_str = f"{current_version.major}.{current_version.minor}.{current_version.micro}"
        sys.exit(f"Alfred requires Python 3.10+\nYou are using Python {version_str}, which is not supported.")


def main():
    print("Alfred is starting...")
    check_python_version()

    # Print the absolute path of the current file
    print(os.path.abspath(__file__))

    # Execute the `brib.py` script using the correct Python executable
    brib_script_path = os.path.join(os.getcwd(), "brib.py")
    if os.name == "nt":
        subprocess.run(["python.exe", brib_script_path], check=True)
    else:
        subprocess.run(["python3", brib_script_path], check=True)


if __name__ == "__main__":
    main()