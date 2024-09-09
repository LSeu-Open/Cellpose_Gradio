@echo off
setlocal enabledelayedexpansion

REM Name of the virtual environment
set ENV_NAME=cellpose-gradio-env

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Create the virtual environment
echo Creating virtual environment: %ENV_NAME%
python -m venv %ENV_NAME%
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate the environment
echo Activating virtual environment...
call %ENV_NAME%\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install numpy matplotlib pillow gradio seaborn cellpose tifffile
if %errorlevel% neq 0 (
    echo Failed to install packages.
    pause
    exit /b 1
)

REM Launch the Gradio app
echo Launching Cellpose Gradio app...
python Cellpose_gradio.py
if %errorlevel% neq 0 (
    echo Failed to run Cellpose_gradio.py.
    pause
    exit /b 1
)

REM Deactivate the environment
call deactivate

echo Setup complete and app launched.
pause
