#!/bin/bash

# Name of the Conda environment
ENV_NAME=cellpose-gradio

# Check if Conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda is not installed or not in the system PATH."
    echo "Please install Conda and try again."
    exit 1
fi

# Create the Conda environment
echo "Creating Conda environment: $ENV_NAME"
conda create -n $ENV_NAME python=3.8.18 -y
if [ $? -ne 0 ]; then
    echo "Failed to create Conda environment."
    exit 1
fi

# Activate the environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME
if [ $? -ne 0 ]; then
    echo "Failed to activate Conda environment."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
conda install -y numpy matplotlib pillow gradio seaborn
pip install cellpose tifffile

# Launch the Gradio app
echo "Launching Cellpose Gradio app..."
python Cellpose_gradio.py

# Deactivate the environment
conda deactivate

echo "Setup complete and app launched."