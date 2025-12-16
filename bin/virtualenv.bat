@echo off
REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
	REM Python version 3.12.4
	REM install virtualenv
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies

venv\Scripts\python.exe -m pip cache purge

venv\Scripts\python.exe -m pip install -r requirements.txt

REM Run the main script
venv\Scripts\python.exe ..\src\main.py

deactivate