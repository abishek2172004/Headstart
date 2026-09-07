# PowerShell script to run the complete stack (Backend + Frontend)
# Right-click and run as administrator if needed

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Financial Analyst POC - Full Stack Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate venv
Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SETUP COMPLETE - Choose an option:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "1) Run BACKEND ONLY (FastAPI on port 8000)" -ForegroundColor Cyan
Write-Host "   API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "2) Run FRONTEND ONLY (Streamlit)" -ForegroundColor Cyan
Write-Host "   URL: http://localhost:8501" -ForegroundColor Gray
Write-Host ""
Write-Host "3) Run BOTH (Backend + Frontend)" -ForegroundColor Cyan
Write-Host "   Backend: http://127.0.0.1:8000/docs" -ForegroundColor Gray
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter your choice (1/2/3)"

switch($choice) {
    "1" {
        Write-Host ""
        Write-Host "Starting FastAPI Backend..." -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
        Write-Host ""
        python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
    }
    "2" {
        Write-Host ""
        Write-Host "Starting Streamlit Frontend..." -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
        Write-Host ""
        streamlit run ui/streamlit_app.py
    }
    "3" {
        Write-Host ""
        Write-Host "Starting both Backend and Frontend..." -ForegroundColor Green
        Write-Host ""
        Write-Host "Please run in TWO separate terminals:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Terminal 1 - Backend:" -ForegroundColor Cyan
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000" -ForegroundColor White
        Write-Host ""
        Write-Host "Terminal 2 - Frontend:" -ForegroundColor Cyan
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  streamlit run ui/streamlit_app.py" -ForegroundColor White
        Write-Host ""
        Write-Host "Then open:" -ForegroundColor Cyan
        Write-Host "  Backend:  http://127.0.0.1:8000/docs" -ForegroundColor Green
        Write-Host "  Frontend: http://localhost:8501" -ForegroundColor Green
    }
    default {
        Write-Host "Invalid choice. Please run again and select 1, 2, or 3." -ForegroundColor Red
    }
}
