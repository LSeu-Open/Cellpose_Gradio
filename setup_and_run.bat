@echo off
setlocal enabledelayedexpansion

:: Name of the Conda environment
set ENV_NAME=cellpose-gradio

:: Check if Conda is installed
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo Conda is not installed or not in the system PATH.
    echo Please install Conda and try again.
    exit /b 1
)

:: Create and activate the Conda environment
echo Creating Conda environment: %ENV_NAME%
conda create -n %ENV_NAME% python=3.8.18 -y
if %errorlevel% neq 0 (
    echo Failed to create Conda environment.
    exit /b 1
)

:: Activate the environment
call conda activate %ENV_NAME%
if %errorlevel% neq 0 (
    echo Failed to activate Conda environment.
    exit /b 1
)

:: Install required packages
echo Installing required packages...
conda install -y numpy matplotlib pillow gradio seaborn
pip install cellpose tifffile

:: Launch the Gradio app
echo Launching Cellpose Gradio app...
python Cellpose_gradio.py

:: Deactivate the environment
call conda deactivate

echo Setup complete and app launched.
pause