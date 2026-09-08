@echo off
REM Quick script to run the Streamlit frontend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Streamlit frontend on http://localhost:8501
echo Opening in default browser...
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run ui/streamlit_app.py

pause
