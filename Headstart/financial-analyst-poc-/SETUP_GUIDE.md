# Financial Analyst POC - Setup & Run Guide

## 📋 Quick Start (One-Time Setup)

### Prerequisites
- **Python 3.12 or 3.11** (NOT 3.14 - lacks wheel support)
- Windows, Mac, or Linux
- GROQ API Key ([Get it here](https://console.groq.com/))

### Step 1: Create Virtual Environment
```powershell
# Navigate to project directory
cd E:\DEEPTHI\financial-analyst-poc-

# Create venv with Python 3.12
py -3.12 -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
# Inside venv, upgrade pip and install packages
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create `.env` file in the **root directory** (not in config folder):
```env
GROQ_API_KEY=gsk_YourActualKeyHere
```

**Get your GROQ API key:**
1. Go to https://console.groq.com/
2. Create an account / Login
3. Go to "API Keys" section
4. Create a new API key
5. Copy and paste into `.env`

---

## 🚀 Running the Project

### Option A: FastAPI Backend Only (For Testing API)
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Start server
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

# Open in browser: http://127.0.0.1:8000/docs
```

### Option B: Streamlit Frontend + Backend (FULL APP)
```powershell
# Terminal 1 - Start Backend
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Start Frontend
.\venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py

# Frontend will open at: http://localhost:8501
```

### Option C: Run Just the AI Assistant (Streamlit Only)
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run AI Assistant page
streamlit run ui/pages/AI_Assistant.py

# Frontend will open at: http://localhost:8501
```

---

## ⚠️ Troubleshooting

### Issue: "No module named X"
**Solution:**
```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Issue: "Missing GROQ_API_KEY"
**Solution:**
- Ensure `.env` exists in root directory (NOT config folder)
- Verify GROQ_API_KEY is set correctly in `.env`
- Restart the app after adding .env

### Issue: Server won't start on port 8000
```powershell
# Try different port
python -m uvicorn backend.app:app --host 127.0.0.1 --port 9000
```

### Issue: Python 3.14 causing "No module named pydantic_core"
**Solution:** Use Python 3.12 instead:
```powershell
# Remove old venv
Remove-Item -Recurse -Force venv

# Create new venv with Python 3.12
py -3.12 -m venv venv

# Reinstall dependencies
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## 📁 Project Structure

```
financial-analyst-poc-/
├── backend/
│   ├── app.py                 # FastAPI main app
│   ├── langgraph_integration.py
│   ├── NAV_Alert_Trigger.py
│   ├── models/
│   ├── routers/
│   └── utils/
├── agent/
│   ├── financial_agent.py     # Main AI agent logic
│   ├── agent_model.py         # GROQ API integration
│   ├── prompts.py
│   └── tools/
├── ui/
│   ├── streamlit_app.py       # Main frontend
│   ├── components/
│   ├── pages/
│   │   └── AI_Assistant.py    # Chat interface
│   └── assets/
├── config/
│   └── example.env
├── .env                        # YOUR GROQ API KEY GOES HERE
├── requirements.txt            # All dependencies
└── README.md

```

---

## 🔑 Environment Variables Reference

### `.env` File (Root Directory)
```env
# REQUIRED
GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# OPTIONAL
BACKEND_URL=http://localhost:8000
```

---

## 🧪 Testing the Setup

### 1. Test Backend
```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

# In browser: http://127.0.0.1:8000/docs
# Should see API documentation
```

### 2. Test AI Agent
```powershell
.\venv\Scripts\Activate.ps1
python -c "
from agent.financial_agent import FinancialAgent
agent = FinancialAgent()
result = agent.run_query('What is the current price of TCS?')
print(result)
"
```

### 3. Test Frontend
```powershell
.\venv\Scripts\Activate.ps1
streamlit run ui/streamlit_app.py

# Open http://localhost:8501
# Click on "AI Assistant" page
# Type a finance query
```

---

## 📝 Common Commands

| Command | Purpose |
|---------|---------|
| `.\venv\Scripts\Activate.ps1` | Activate virtual environment |
| `deactivate` | Deactivate virtual environment |
| `python -m pip list` | List installed packages |
| `python -m pip install -r requirements.txt` | Install all dependencies |
| `python -m uvicorn backend.app:app --reload` | Start backend server |
| `streamlit run ui/streamlit_app.py` | Start frontend UI |

---

## 🔗 Important Links

- **GROQ Console:** https://console.groq.com/
- **Streamlit Docs:** https://docs.streamlit.io/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **LangGraph Docs:** https://docs.langchain.com/langgraph

---

## ✅ Verification Checklist

Before running, ensure:
- [ ] Python 3.12 or 3.11 installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed: `pip list | findstr fastapi`
- [ ] `.env` file with GROQ_API_KEY in root directory
- [ ] Can access http://127.0.0.1:8000/docs (backend)
- [ ] Can access http://localhost:8501 (frontend)

---

## 🆘 Still Having Issues?

1. Check Python version: `python --version` (should be 3.12.x)
2. Check venv is activated: `(venv)` prefix in terminal
3. Check .env exists: `cat .env` (should show GROQ_API_KEY)
4. Delete venv and reinstall: `Remove-Item -Recurse venv; py -3.12 -m venv venv`
5. Run: `python -m pip install --force-reinstall -r requirements.txt`

---

**Last Updated:** March 25, 2026
