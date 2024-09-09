@echo off
setlocal enabledelayedexpansion

REM Set the path to the virtual environment
set VENV_PATH=.\cellpose-gradio-env

REM Activate the virtual environment
call %VENV_PATH%\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Launch the Gradio app
echo Launching Cellpose Gradio app...
python Cellpose_gradio.py

REM Pause to keep the window open
pause
