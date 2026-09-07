@echo off
REM HeadStart Financial Analyst POC - Run All Services
REM This script starts both Backend (FastAPI) and Frontend (Streamlit) services

echo.
echo =====================================
echo   HeadStart Financial Analyst POC
echo =====================================
echo.

REM Check if we're in the correct directory
if not exist "backend\app.py" (
    echo ERROR: Please run this script from the project root directory
    pause
    exit /b 1
)

echo Checking dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Streamlit is not installed. Run: pip install streamlit
    pause
    exit /b 1
)

echo.
echo Starting services...
echo.

REM Start Backend in a new window
echo [Backend] Starting FastAPI on http://127.0.0.1:8000
start "HeadStart Backend" python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

REM Wait for backend to start
timeout /t 3 >nul

REM Start Frontend in a new window
echo [Frontend] Starting Streamlit on http://localhost:8501
start "HeadStart Frontend" streamlit run ui/streamlit_app.py

echo.
echo =====================================
echo   Services Started Successfully!
echo =====================================
echo.
echo Dashboard:     http://localhost:8501
echo AI Assistant:  http://localhost:8501/AI_Assistant
echo Backend API:   http://127.0.0.1:8000
echo.
echo Powered by:
echo  - Groq AI (llama-3.3-70b-versatile)
echo  - YFinance (Real-time market data)
echo  - LangGraph (Workflow orchestration)
echo.
pause
