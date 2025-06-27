@echo off
REM --- go to project directory ---
cd /d "C:\Users\localuser\Desktop\evil"

REM --- activate virtual environment ---
call venv\Scripts\activate

REM --- run the application ---
python app.py

REM --- keep the window open so you can see output/errors ---
pause