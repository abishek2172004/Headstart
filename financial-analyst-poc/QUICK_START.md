# 🚀 Quick Start

## One-Time Setup (First Time Only)

```powershell
# Create Python 3.12 virtual environment
py -3.12 -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt
```

## Add GROQ API Key

Create `.env` file in root directory with:
```
GROQ_API_KEY=your_actual_key_here
```

Get free API key from: https://console.groq.com/

---

## Running the Project (Every Time)

### Linux / GitHub Codespaces

From the project directory, run:

```bash
./run.sh
```

Then open **http://127.0.0.1:8501**. This starts or reuses the FastAPI and
Streamlit services. n8n is optional and is only needed for the Alert Config
workflow.

### Quick Run Script (Recommended)
```powershell
.\RUN.ps1
```

### Or Manual Commands

**Start Backend:**
```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

**Start Frontend (in NEW terminal):**
```powershell
.\venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py
```

---

## 📍 Access Points

| Component | URL |
|-----------|-----|
| **API Docs** | http://127.0.0.1:8000/docs |
| **Frontend** | http://localhost:8501 |
| **AI Assistant** | http://localhost:8501/AI_Assistant |

---

## 📖 Full Documentation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:
- Detailed setup instructions
- Troubleshooting
- Project structure
- Environment variables
- Testing procedures

---

## ✅ Verify Setup

```powershell
# Check Python version
python --version

# Check installed packages
python -m pip list | findstr fastapi

# Test venv activation
# Should show "(venv)" in terminal
```

---

## ⚠️ Important Notes

- **Use Python 3.12 or 3.11** (NOT 3.14)
- **GROQ API Key must be in `.env`** (root directory, not config/)
- **Backend must run for AI features to work**
- **Two terminals needed** for full app (backend + frontend)

## Configure Stock Alerts with n8n

The Alert Config page sends subscriptions to n8n's production webhook:

```text
http://localhost:5678/webhook/alert
```

1. Start n8n with `n8n start` or `npx n8n`.
2. Import `n8n/stock_alert_workflow.json` from this project.
3. Configure the Postgres, Gmail, and Groq credentials in the imported workflow.
4. Confirm the HTTP Request node calls `http://127.0.0.1:8000/run_NAV_Alert_Trigger`.
5. Activate the workflow using the **Active** toggle in n8n.
6. Copy `config/example.env` to `.env` if needed and set `N8N_WEBHOOK_URL` when n8n runs on another host or port.

Use `/webhook-test/alert` only for a manual test while the workflow is open and
the **Execute Workflow** button is running. Normal app use requires the active
production webhook at `/webhook/alert`.

---

**Having issues?** Check [SETUP_GUIDE.md](SETUP_GUIDE.md#-troubleshooting) for common fixes.
