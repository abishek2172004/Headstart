import os
from groq import Groq
from dotenv import load_dotenv
from agent.prompts import SYSTEM_PROMPT

# Load .env from root directory or config folder
root_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
config_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")

if os.path.exists(root_env):
    load_dotenv(root_env)
elif os.path.exists(config_env):
    load_dotenv(config_env)
else:
    load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class AgentModel:
    """
    Thin wrapper around Groq chat completion with a safe local fallback.
    This ensures the app starts even when a Groq API key is not configured.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or GROQ_API_KEY
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = "llama-3.3-70b-versatile"

    def is_available(self) -> bool:
        return self.client is not None

    def _local_fallback(self, query: str) -> str:
        q = (query or "").strip()
        q_lower = q.lower()

        if any(k in q_lower for k in ["price", "quote", "trading at", "current value"]):
            return (
                "I can help analyze the stock price and daily move. "
                "For a live price, I would normally fetch the latest market data and compare it against recent levels, volume, and trend. "
                "If you share a ticker like INFY, TCS, or AAPL, I can break it down in simple terms."
            )

        if any(k in q_lower for k in ["compare", "vs", "versus", "better than", "between"]):
            return (
                "I can compare stocks by valuation, growth, momentum, and risk. "
                "In practice, I’d look at price trend, PE ratio, profit margins, ROE, and analyst sentiment before giving a balanced view."
            )

        if any(k in q_lower for k in ["market", "nifty", "sensex", "index", "sentiment"]):
            return (
                "The market mood usually depends on the broader index trend, sector rotation, and earnings momentum. "
                "I can help summarize whether the market looks bullish, neutral, or cautious based on the latest data."
            )

        if any(k in q_lower for k in ["financial", "balance sheet", "income", "cash flow", "valuation"]):
            return (
                "I can explain profitability, margins, ROE, debt, and valuation in plain English. "
                "For Indian companies, I’d usually compare PE, ROE, profit margin, and debt-to-equity to a peer group before drawing conclusions."
            )

        return (
            "I’m the HeadStart AI assistant for financial research. "
            "I can help with stock questions, market summaries, comparisons, and beginner-friendly investing explanations. "
            "Ask me about a ticker, valuation, or market trend and I’ll respond with a concise analysis."
        )

    def query_model(self, query: str) -> str:
        if not self.client:
            return self._local_fallback(query)

        context = f"""
                You are a professional financial analyst.

                Even if full financial data is not available:
                - Use general market knowledge
                - Make reasonable assumptions
                - Give practical advice

                Always respond in this format:

                Recommendation: (Buy / Hold / Wait / Avoid)

                Reason:
                - clear explanation

                Risks:
                - possible downsides
                """

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": context + "\nUser Question:\n" + query},
                ],
                temperature=0.3,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return self._local_fallback(query)
