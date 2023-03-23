@echo off

:: Set the directory of the batch file as the current working directory
cd /d "%~dp0"

:: Activate the Python virtual environment stored in the .venv subdirectory
call .venv\Scripts\activate.bat

:: Run the Python file called main.py
python main.py

:: Deactivate the virtual environment
deactivate
