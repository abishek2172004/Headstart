# HeadStart - Integration Guide
## How Groq API, YFinance, and LangGraph Work Together

### 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│             Streamlit Frontend (Port 8501)                   │
│  • AI Assistant Chat Interface                               │
│  • Dashboard with Market Data                                │
│  • Stock Analysis & Charts                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│            FinancialAgent (ui/pages/AI_Assistant.py)         │
│  • Processes user queries                                    │
│  • Classifies intent (price, compare, market, news, etc)    │
│  • Extracts stock tickers                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
   ┌──────────────┐        ┌────────────────┐
   │   YFinance   │        │  Groq API      │
   │ Real-time    │        │  AI Insights   │
   │ Stock Data   │        │  Analysis      │
   └──────────────┘        └────────────────┘
         │ Data                    │ Insights
         └────────────┬───────────┘
                      ▼
          ┌────────────────────────┐
          │   LangGraph Workflow   │
          │  (NAV Alert Trigger)  │
          │  • State Management   │
          │  • Alert Orchestration │
          └────────────────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │     FastAPI Backend    │
          │    (Port 8000)         │
          │  /get_price            │
          │  /compare_stocks       │
          │  /get_market_summary   │
          │  /run_NAV_Alert_Trigger│
          └────────────────────────┘
```

---

### 📊 AI Assistant Data Flow

#### 1. **User asks a question** (e.g., "Price of INFY")
```
Input: "Price of INFY"
↓
FinancialAgent.run(query)
```

#### 2. **Agent processes the query**
- Extracts ticker: INFY ("INFY" → INFY.NS)
- Classifies intent: "price"
- Calls YFinanceHelper.get_price("INFY.NS")

#### 3. **YFinance fetches real-time data**
```python
YFinanceHelper.get_price("INFY.NS")
Returns: {
    "ticker": "INFY.NS",
    "current_price": 2850.50,
    "change_pct": 1.25,
    "highest_price": 2950.00,
    "lowest_price": 2800.00,
    ...
}
```

#### 4. **Groq AI generates insights**
```python
FinancialAgent.enrich_with_ai_insights(
    intent="price",
    data={price_info},
    query="Price of INFY"
)
```
Prompt to Groq:
```
Financial Analysis Brief - Provide actionable insight (2-3 sentences):
Stock: INFY.NS
Current Price: ₹2850.50
Today's Change: +1.25%
52W Range: ₹2800 - ₹2950
```

Groq Response (using llama-3.3-70b-versatile):
```
"Infosys remains bullish as it breaks above the 2850 level with strong buying. 
The positive momentum suggests continued upside toward 2900. 
Investors can consider fresh positions with a stop loss at 2820."
```

#### 5. **Response formatted and displayed**
```
INFY ↑
₹2850.50 | Change: +1.25%

Analysis:
Infosys remains bullish as it breaks above the 2850 level with strong buying.
The positive momentum suggests continued upside toward 2900.
Investors can consider fresh positions with a stop loss at 2820.
```

---

### 🔄 Multi-Intent Support

| Intent | Data Source | AI Enhancement | LangGraph |
|--------|------------|-----------------|-----------|
| **price** | YFinance | Price analysis & outlook | N/A |
| **compare** | YFinance | Verdict on which stock is better | N/A |
| **market** | YFinance | Market sentiment analysis | N/A |
| **financials** | YFinance | Financial health assessment | N/A |
| **news** | YFinance | News aggregation | N/A |
| **general** | Groq | General finance Q&A | N/A |
| **NAV Alert** | YFinance | Triggers alerts | ✓ Workflow |

---

### 🛠️ Key Files & Their Roles

#### **Agent Layer** (`agent/`)
- `financial_agent.py` - Core agent orchestration
  - `extract_tickers()` - Parse ticker symbols
  - `classify_intent()` - Determine query type
  - `enrich_with_ai_insights()` - Call Groq for analysis
  - `run()` - Main orchestration method

- `agent_model.py` - Groq API wrapper
  - `query_model(prompt)` - Send prompt to Groq

#### **Frontend** (`ui/`)
- `streamlit_app.py` - Main dashboard
- `pages/AI_Assistant.py` - Chat interface
  - Calls `FinancialAgent.run(query)`
  - Formats responses with `format_bot_response()`

#### **Backend** (`backend/`)
- `app.py` - FastAPI server
- `routers/finance.py` - API endpoints
- `langgraph_integration.py` - LangGraph workflow nodes
- `NAV_Alert_Trigger.py` - Alert workflow definition
- `utils/yf_utils.py` - YFinance wrapper

---

### 🚀 Running the System

#### **Option 1: Batch File (Windows)**
```bash
RUN_ALL.bat
```
This opens two terminal windows:
- Backend service (FastAPI)
- Frontend service (Streamlit)

#### **Option 2: PowerShell Script**
```bash
.\RUN_ALL.ps1
```

#### **Option 3: Manual Start**
```bash
# Terminal 1: Backend
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
streamlit run ui/streamlit_app.py
```

#### **Access Points:**
- **Dashboard**: http://localhost:8501
- **AI Assistant**: http://localhost:8501/AI_Assistant
- **Backend API**: http://127.0.0.1:8000

---

### 🤖 Configuration

#### **Environment Variables** (`.env`)
```
GROQ_API_KEY=gsk_[your-key-here]
```

#### **Agent Settings**
- Model: `llama-3.3-70b-versatile`
- Temperature: 0.7 (default)
- Max tokens: 1000

#### **YFinance Settings**
- Data source: Yahoo Finance
- Update frequency: Real-time
- Supported markets: NSE, BSE (India)

---

### 📈 Example Queries

```
1. "Price of INFY"
   → YFinance data + Groq analysis

2. "Compare TCS and INFY"
   → Compare both stocks + AI verdict

3. "Market updates"
   → Nifty 50, Sensex indices + Market sentiment

4. "INFY news"
   → Latest news for Infosys

5. "What is PE ratio?"
   → General finance knowledge from Groq
```

---

### 🔐 Security

- ✅ CORS enabled for frontend access
- ✅ API key stored in environment variables
- ✅ No sensitive data in logs
- ✅ Input sanitization in Streamlit

---

### ⚡ Performance

- **Query Response Time**: 2-5 seconds (includes YFinance + Groq)
- **Cache**: Streamlit session state caching
- **Concurrent Requests**: FastAPI handles multiple requests
- **Rate Limits**: Follow Groq API limits (default: 2000 requests/day)

---

### 🐛 Troubleshooting

#### Backend not responding:
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID [PID] /F
```

#### Groq API error:
```
Error: "Invalid API key"
Solution: Check .env file has GROQ_API_KEY=gsk_...
```

#### YFinance data unavailable:
```
Error: "No data found for ticker"
Solution: Check ticker is correctly mapped or try NSE format (e.g., INFY.NS)
```

#### Streamlit caching issues:
```
Solution: Clear cache with Ctrl+Shift+C or restart service
```

---

### 📚 Next Steps

1. **Custom LangGraph Workflows** - Add complex multi-step workflows
2. **Portfolio Management** - Track multiple stock portfolios
3. **Alerts & Notifications** - Set price alerts via n8n
4. **ML Predictions** - Add price prediction models
5. **Mobile App** - Build mobile interface using React Native

---

### 📖 Documentation

- [Groq API Docs](https://console.groq.com/docs)
- [YFinance Docs](https://yfinance.readthedocs.io)
- [LangGraph Docs](https://docs.langchain.com/langgraph)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Streamlit Docs](https://docs.streamlit.io)

---

**Last Updated**: April 7, 2026  
**Status**: ✅ All components integrated and running
