import html
import os
import sys
from datetime import datetime, timezone

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agent.financial_agent import FinancialAgent


def _timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def _append_chat(role: str, message: str) -> None:
    st.session_state.chat_history.append(
        {"role": role, "message": message, "time": _timestamp()}
    )


def _format_response(agent_response: dict) -> str:
    intent = agent_response.get("intent", "")
    data = agent_response.get("data") or {}
    response_text = agent_response.get("response", "")
    ai_insights = agent_response.get("ai_insights", "")

    if agent_response.get("type") == "error":
        return agent_response.get("message", "I could not process that request.")
    if isinstance(data, dict) and data.get("error"):
        return f"Error: {data['error']}"

    if intent == "price" and isinstance(data, dict) and "current_price" in data:
        ticker = data.get("ticker", agent_response.get("ticker", "Unknown"))
        currency = data.get("currency", "INR")
        change = float(str(data.get("change_pct", 0)).replace("%", ""))
        arrow = "up" if change > 0 else "down" if change < 0 else "unchanged"
        result = (
            f"**{ticker} live price**\n\n"
            f"- Price: **{currency} {data.get('current_price', 'N/A')}**\n"
            f"- Change: **{change:+.2f}%** ({arrow})\n"
            f"- Previous close: {currency} {data.get('previous_price', 'N/A')}\n"
            f"- 52-week range: {currency} {data.get('52_week_low', 'N/A')} - "
            f"{currency} {data.get('52_week_high', 'N/A')}"
        )
        return f"{result}\n\n{ai_insights}" if ai_insights else result

    if intent == "compare" and isinstance(data, dict):
        lines = ["**Stock comparison**"]
        for ticker, info in data.get("comparison", {}).items():
            currency = info.get("currency", "INR")
            lines.extend(
                [
                    f"\n**{ticker}**",
                    f"- Price: {currency} {info.get('current_price', 'N/A')}",
                    f"- Change: {info.get('change_pct', 0):+.2f}%",
                    f"- P/E: {info.get('pe_ratio', 'N/A')}",
                    f"- Profit margin: {info.get('profit_margin', 'N/A')}",
                    f"- ROE: {info.get('roe', 'N/A')}",
                    f"- Analyst view: {info.get('recommendation', 'N/A')}",
                ]
            )
        if agent_response.get("summary"):
            lines.extend(["", agent_response["summary"]])
        if ai_insights:
            lines.extend(["", ai_insights])
        return "\n".join(lines)

    if intent == "financials" and isinstance(data, dict):
        stats = data.get("key_stats", {})
        ticker = data.get("ticker", agent_response.get("ticker", "Stock"))
        currency = data.get("currency", "INR")
        lines = [f"**{ticker} financial snapshot** ({currency})"]
        labels = (
            ("Market cap", "market_cap"),
            ("Trailing P/E", "trailing_pe"),
            ("Forward P/E", "forward_pe"),
            ("Profit margin", "profit_margins"),
            ("ROE", "return_on_equity"),
            ("Debt to equity", "debt_to_equity"),
            ("Dividend yield", "dividend_yield"),
        )
        for label, key in labels:
            if key in stats:
                lines.append(f"- {label}: {stats[key]}")
        if data.get("income_statement"):
            lines.append("- Latest income statement data: available")
        if data.get("balance_sheet"):
            lines.append("- Latest balance sheet data: available")
        if data.get("cash_flow"):
            lines.append("- Latest cash flow data: available")
        if ai_insights:
            lines.extend(["", ai_insights])
        return "\n".join(lines)

    if intent == "market_summary" and isinstance(data, dict):
        lines = ["**Market summary**"]
        for name, info in data.get("indices", {}).items():
            lines.append(
                f"- {name}: {info.get('value', 'N/A')} "
                f"({info.get('change_pct', 0):+.2f}%)"
            )
        if data.get("timestamp"):
            lines.append(f"\nAs of {data['timestamp']}")
        if ai_insights:
            lines.extend(["", ai_insights])
        return "\n".join(lines)

    if intent == "news" and isinstance(data, dict):
        lines = [f"**Latest news for {data.get('ticker', agent_response.get('ticker', 'stock'))}**"]
        for article in data.get("articles", [])[:5]:
            lines.append(f"- [{article.get('title', 'Untitled')}]({article.get('link', '#')})")
        return "\n".join(lines)

    return response_text or "I could not find a response for that question."


def _run_query(query: str) -> None:
    if not query.strip():
        return
    _append_chat("user", query)
    try:
        response = st.session_state.agent.run(query)
        _append_chat("bot", _format_response(response))
    except Exception as exc:
        _append_chat("bot", f"I could not complete that request: {exc}")


def run_assistant_page() -> None:
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("theme", "dark")
    if "agent" not in st.session_state:
        st.session_state.agent = FinancialAgent()

    st.markdown(
        """
        <section class="assistant-header">
            <div>
                <div class="assistant-kicker">RESEARCH DESK / AI ASSISTANT</div>
                <h1 class="assistant-title">Ask sharper market questions.</h1>
                <p class="assistant-lede">Prices, valuation, market mood, and company context in one focused conversation.</p>
            </div>
            <div class="assistant-status"><span class="status-dot"></span>Ready for research</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    suggestions = ["Price of AAPL", "What is the TCS ticker value?", "Compare AAPL and TCS", "What is market sentiment today?"]
    st.markdown("<div class='suggestion-label'>Start with a question</div>", unsafe_allow_html=True)
    columns = st.columns(len(suggestions))
    for index, suggestion in enumerate(suggestions):
        with columns[index]:
            if st.button(suggestion, key=f"assistant_suggestion_{index}", use_container_width=True):
                _run_query(suggestion)
                st.rerun()

    st.markdown("<div class='conversation-heading'>Conversation</div>", unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown(
            """
            <div class="assistant-empty">
                <div class="assistant-empty-mark">↗</div>
                <div>
                    <strong>Your research thread is empty.</strong>
                    <p>Ask about a ticker, compare two companies, or request a market summary to begin.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for message in st.session_state.chat_history:
            role = "You" if message["role"] == "user" else "Assistant"
            content = html.escape(str(message["message"]))
            content = content.replace("\n", "<br>")
            st.markdown(
                f"<div class='chat-row {message['role']}'><div class='chat-bubble'>"
                f"<div class='chat-role'>{role}</div><div>{content}</div>"
                f"<div class='chat-meta'>{message['time']}</div>"
                "</div></div>",
                unsafe_allow_html=True,
            )

    query = st.chat_input("Ask about any stock or market topic...")
    if query:
        _run_query(query)
        st.rerun()
