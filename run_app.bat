@echo off

REM Set the path to the Anaconda installation directory
set ANACONDA_PATH=C:\Users\your_username\AppData\Local\anaconda3

REM Set the path to the Anaconda Scripts directory
set SCRIPTS_PATH=%ANACONDA_PATH%\Scripts

REM Name of the Conda environment
set ENV_NAME=cellpose-gradio

REM Activate the environment
call conda activate %ENV_NAME%
if %errorlevel% neq 0 (
    echo Failed to activate Conda environment.
    exit /b 1
)

REM Launch the Gradio app
echo Launching Cellpose Gradio app...
python Cellpose_gradio.py

REM Pause to keep the window open
pause
