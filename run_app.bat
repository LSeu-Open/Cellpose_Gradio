@echo off
setlocal enabledelayedexpansion

:: Name of the Conda environment
set ENV_NAME=cellpose-gradio

:: Activate the environment
call conda activate %ENV_NAME%
if %errorlevel% neq 0 (
    echo Failed to activate Conda environment.
    exit /b 1
)

:: Launch the Gradio app
echo Launching Cellpose Gradio app...
python Cellpose_gradio.py

:: Deactivate the environment
call conda deactivate

echo App closed.
pause