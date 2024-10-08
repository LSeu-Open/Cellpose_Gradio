#!/bin/bash

# Name of the virtual environment
ENV_NAME=cellpose-gradio-env

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed or not in the system PATH."
    echo "Please install Python and try again."
    exit 1
fi

# Create the virtual environment
echo "Creating virtual environment: $ENV_NAME"
python3 -m venv $ENV_NAME
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate the environment
source $ENV_NAME/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip install numpy matplotlib pillow gradio seaborn cellpose tifffile werkzeug

# Launch the Gradio app
echo "Launching Cellpose Gradio app..."
python Cellpose_gradio.py

# Deactivate the environment
deactivate

echo "Setup complete and app launched."
