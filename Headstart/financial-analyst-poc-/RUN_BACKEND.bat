@echo off
REM Quick script to run the FastAPI backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server on http://127.0.0.1:8000
echo API docs available at: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

pause
