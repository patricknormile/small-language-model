#!/bin/bash

# Create a Python 3.11 virtual environment named slm-env
python3.11 -m venv slm-env

# Activate the virtual environment
source slm-env/bin/activate

# Install the requirements from requirements.txt
pip install -r requirements.txt

# Activate the environment
echo "Virtual environment slm-env created and requirements installed."
echo "To activate the environment, run: source slm-env/bin/activate"
