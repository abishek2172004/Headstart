#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [[ ! -f ".venv/bin/activate" ]]; then
    echo "Virtual environment not found. Create it with: python3 -m venv .venv"
    exit 1
fi

# Use the project's interpreter for both services.
source .venv/bin/activate

if curl -fsS http://127.0.0.1:8000/ >/dev/null 2>&1; then
    echo "Backend already running: http://127.0.0.1:8000"
else
    echo "Starting backend on http://127.0.0.1:8000"
    python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 &
    backend_pid=$!
    trap 'kill "$backend_pid" 2>/dev/null || true' EXIT

    for attempt in {1..30}; do
        if curl -fsS http://127.0.0.1:8000/ >/dev/null 2>&1; then
            break
        fi
        sleep 1
    done
fi

if curl -fsS http://127.0.0.1:8501/_stcore/health >/dev/null 2>&1; then
    echo "Streamlit already running: http://127.0.0.1:8501"
    echo "Open http://127.0.0.1:8501 in the browser."
    wait
else
    echo "Starting Streamlit on http://127.0.0.1:8501"
    streamlit run ui/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
fi