# HeadStart - Financial Analyst POC
# Run Backend + Frontend together

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  HeadStart Financial Analyst POC" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python availability
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Streamlit availability
try {
    $streamlitVersion = streamlit --version 2>&1
    Write-Host "✓ Streamlit: $streamlitVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Streamlit not found. Install with: pip install streamlit" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start Backend (FastAPI) in background
Write-Host "🚀 Starting Backend (FastAPI on port 8000)..." -ForegroundColor Cyan
$backendProc = Start-Process -FilePath python `
    -ArgumentList "-m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000" `
    -WindowStyle Hidden `
    -PassThru

Write-Host "   Backend PID: $($backendProc.Id)" -ForegroundColor Green

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend (Streamlit) in background
Write-Host "🚀 Starting Frontend (Streamlit on port 8501)..." -ForegroundColor Cyan
$frontendProc = Start-Process -FilePath streamlit `
    -ArgumentList "run ui/streamlit_app.py" `
    -WindowStyle Hidden `
    -PassThru

Write-Host "   Frontend PID: $($frontendProc.Id)" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Services Running Successfully!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Dashboard:     http://localhost:8501" -ForegroundColor Yellow
Write-Host "📊 AI Assistant:  http://localhost:8501/AI_Assistant" -ForegroundColor Yellow
Write-Host "🔌 Backend API:   http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Cyan
Write-Host ""

# Keep script running and monitor processes
$backendActive = $true
$frontendActive = $true

while ($backendActive -or $frontendActive) {
    if ($backendProc.HasExited) {
        $backendActive = $false
        Write-Host "⚠️  Backend stopped" -ForegroundColor Red
    }
    if ($frontendProc.HasExited) {
        $frontendActive = $false
        Write-Host "⚠️  Frontend stopped" -ForegroundColor Red
    }
    Start-Sleep -Seconds 5
}

Write-Host "All services stopped." -ForegroundColor Yellow
