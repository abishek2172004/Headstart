import re
import logging
import yfinance as yf

from agent.agent_model import AgentModel
from backend.utils.yf_utils import YFinanceHelper
from backend.utils.ticker_map import INDIA_TICKER_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMMON_WORDS = {
    "WHAT", "THE", "IS", "A", "AN", "OF", "TO", "IN", "FOR",
    "PRICE", "HOW", "ARE", "YOU", "STOCK", "STOCKS", "TELL",
    "ME", "TODAY", "CHECK", "SHOW", "MARKET", "UPDATES",
    "NEWS", "LONG", "BEST", "TERM", "INDIA", "SHORT",
    "BETWEEN", "VS", "VERSUS", "AND", "ON", "ABOUT", "WITH",
    "WHICH", "BETTER", "GOOD", "GIVE", "COMPARE", "VS", "VERSUS", "CAN", "YOU", "PLEASE", "MY", "ADVISE", "SUGGEST", "LOOKING", "AT", "FORWARD", "INVESTMENT", "INVEST", "TRADING", "I", "WANT", "TO", "KNOW", "CURRENT", "VALUE", "OF", "HOW'S", "DOING", "PERFORMANCE"
}

FINANCE_KEYWORDS = [
    "stock", "stocks", "share", "shares", "equity", "equities",
    "nifty", "sensex", "index", "indices", "market", "markets",
    "invest", "investment", "investing", "trading", "intraday",
    "swing", "long term", "short term", "portfolio", "risk",
    "returns", "profit", "loss", "valuation", "pe ratio", "pe",
    "dividend", "eps", "earnings", "results", "balance sheet",
    "cash flow", "financials", "fundamental", "technical",
    "mutual fund", "mf", "etf", "sip", "brokerage", "ticker",
    "price", "cmp", "quote", "trading", "bull", "bear", "rally",
    "crash", "momentum", "resistance", "support", "volatility",
    "hedge", "diversify", "sector", "rupee", "currency", "inflation",
    "ipo", "startup", "unicorn", "financial", "economy", "gdp",
    "rbi", "rbi rate", "interest rate", "bond", "crypto", "bitcoin"
]


class FinancialAgent:
    def __init__(self):
        self.model = AgentModel()

    def is_finance_query(self, query: str) -> bool:
        q = query.lower()
        return any(keyword in q for keyword in FINANCE_KEYWORDS)

    # ------------------------------------------------------------------
    # Improved Ticker Extraction
    # ------------------------------------------------------------------
    def extract_tickers(self, query: str) -> list[str]:
        """
        Best priority:
        1️⃣ Exact India mapping from INDIA_TICKER_MAP
        2️⃣ NSE (.NS)
        3️⃣ BSE (.BO)
        4️⃣ Raw symbol fallback
        """
        query_upper = query.upper()
        tokens = re.findall(r"\b[A-Z]{2,10}\b", query_upper)
        logger.info(f"[Agent] Tokens from query '{query}': {tokens}")

        found = set()

        for token in tokens:
            if token in COMMON_WORDS:
                continue

            # Top Priority → India mapping
            if token in INDIA_TICKER_MAP:
                mapped = INDIA_TICKER_MAP[token]
                found.add(mapped)
                logger.info(f"[Agent] Mapped ticker: {token} → {mapped}")
                continue

            # Check NSE, BSE, raw via yfinance validation
            for suffix in [".NS", ".BO", ""]:
                candidate = token + suffix
                try:
                    t = yf.Ticker(candidate)
                    info = t.fast_info
                    if info and "lastPrice" in info:
                        found.add(candidate)
                        logger.info(f"[Agent] Valid ticker detected: {candidate}")
                        break
                except Exception:
                    continue

        tickers = list(found)
        logger.info(f"[Agent] Final tickers extracted: {tickers}")
        return tickers

    # ------------------------------------------------------------------
    def classify_intent(self, query_lower: str, tickers: list[str]) -> str:
        if any(k in query_lower for k in ["compare", "vs", "versus", "better than", "between"]):
            return "compare" if len(tickers) >= 2 else "general"

        if "news" in query_lower:
            return "news"

        if any(k in query_lower for k in ["market", "indices", "index", "nifty", "sensex"]):
            return "market"

        if any(k in query_lower for k in ["profit", "financial", "valuation", "balance"]
               ) and tickers:
            return "financials"

        if any(k in query_lower for k in ["price", "cmp", "quote", "trading at"]) and tickers:
            return "price"

        if tickers and any(k in query_lower for k in ["long term", "short term", "buy", "sell"]):
            return "financials"

        return "general"

    # ------------------------------------------------------------------
    # NEW: Groq AI Enhancement for deeper analysis
    # ------------------------------------------------------------------
    def enrich_with_ai_insights(self, intent: str, data: dict, query: str) -> str:
        """Use Groq to provide AI-powered insights on the data"""
        try:
            if intent == "price":
                ticker = data.get('ticker', '')
                price = data.get('current_price', 0)
                change = data.get('change_pct', 0)
                high = data.get('current_high', 0)
                low = data.get('current_low', 0)

                prompt = f"""Financial Analysis Brief - Provide actionable insight (2-3 sentences):
Stock: {ticker}
Current Price: ₹{price}
Today's Change: {change:+.2f}%
52W Range: ₹{low} - ₹{high}"""

                return self.model.query_model(prompt)

            elif intent == "compare":
                prompt = f"""Compare these stocks briefly (2-3 sentences):
{str(data)[:800]}

Which is better for long-term investors?"""
                return self.model.query_model(prompt)

            elif intent == "market":
                prompt = f"""Analyze market sentiment in 1-2 sentences:
{str(data)[:500]}"""
                return self.model.query_model(prompt)

            elif intent == "financials":
                prompt = f"""Financial health assessment (2-3 sentences):
{str(data)[:600]}"""
                return self.model.query_model(prompt)

        except Exception as e:
            logger.error(f"AI enrichment error: {str(e)}")
            return ""

    # ------------------------------------------------------------------
    def run(self, query: str) -> dict:
        query_lower = query.lower()
        steps = [{"thought": f"User asked: {query}"}]

        tickers = self.extract_tickers(query)
        primary = tickers[0] if tickers else None

        intent = self.classify_intent(query_lower, tickers)
        steps.append({"thought": f"Detected intent: {intent}, tickers: {tickers or 'none'}"})

        # PRICE
        if intent == "price" and primary:
            steps.append({"thought": f"Fetching price via YFinanceHelper.get_price"})
            price_data = YFinanceHelper.get_price(primary)
            ai_insights = self.enrich_with_ai_insights("price", price_data, query)
            return {
                "type": "tool",
                "intent": "price",
                "ticker": primary,
                "data": price_data,
                "ai_insights": ai_insights,
                "steps": steps,
            }

        # FINANCIALS
        if intent == "financials" and primary:
            steps.append({"thought": f"Fetching financials via YFinanceHelper.get_financials"})
            financials_data = YFinanceHelper.get_financials(primary)
            ai_insights = self.enrich_with_ai_insights("financials", financials_data, query)
            return {
                "type": "tool",
                "intent": "financials",
                "ticker": primary,
                "data": financials_data,
                "ai_insights": ai_insights,
                "steps": steps,
            }

        # COMPARISON
        if intent == "compare":
            if len(tickers) < 2:
                return {"type": "error", "message": "I need two stock symbols to compare."}
            steps.append({"thought": "Comparing stocks"})
            compare_data = YFinanceHelper.compare_stocks(tickers)

            summary = self.model.query_model(
                f"Explain comparison in beginner terms:\n\n{compare_data}"
            )
            
            ai_insights = self.enrich_with_ai_insights("compare", compare_data, query)

            return {
                "type": "tool",
                "intent": "compare",
                "tickers": tickers,
                "data": compare_data,
                "summary": summary,
                "ai_insights": ai_insights,
                "steps": steps,
            }

        # MARKET SUMMARY
        if intent == "market":
            steps.append({"thought": "Fetching market summary"})
            market_data = YFinanceHelper.get_market_summary()
            ai_insights = self.enrich_with_ai_insights("market", market_data, query)
            return {
                "type": "tool",
                "intent": "market_summary",
                "data": market_data,
                "ai_insights": ai_insights,
                "steps": steps,
            }

        # NEWS
        if intent == "news":
            if not primary:
                return {"type": "error", "message": "Please specify stock for news."}
            steps.append({"thought": "Fetching news"})
            return {
                "type": "tool",
                "intent": "news",
                "ticker": primary,
                "data": YFinanceHelper.get_news(primary, limit=5),
                "steps": steps,
            }

        # OUT OF SCOPE
        if not self.is_finance_query(query):
            msg = (
                "⚠️ I’m a **Financial Markets Assistant**\n\n"
                "Try asking:\n"
                "• Price of INFY\n"
                "• Compare TCS and INFY\n"
                "• Give me market updates"
            )
            return {
                "type": "llm",
                "intent": "out_of_scope",
                "response": msg,
                "steps": steps,
            }

        # GENERAL LLM
        steps.append({"thought": "General finance query → LLM response"})
        return {
            "type": "llm",
            "intent": "general",
            "ticker": primary,
            "response": self.model.query_model(query),
            "steps": steps,
        }
