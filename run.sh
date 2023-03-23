#!/bin/bash

# Set the directory of the script as the current working directory
cd "$(dirname "$0")"

# Activate the Python virtual environment stored in the .venv subdirectory
source .venv/bin/activate

# Run the Python file called main.py
python main.py

# Deactivate the virtual environment
deactivate
