import os
import re

import requests
import streamlit as st
from dotenv import load_dotenv


DEFAULT_BACKEND_URL = "http://localhost:8000"
load_dotenv()


def get_backend_url():
    """Return the configured FastAPI backend URL."""
    return os.getenv("BACKEND_URL", DEFAULT_BACKEND_URL).rstrip("/")


def send_alert_config(email, ticker, threshold_type, threshold_value):
    """
    Run the alert check through the FastAPI backend.
    Returns: (success: bool, message: str)
    """
    backend_url = f"{get_backend_url()}/run_NAV_Alert_Trigger"
    try:
        payload = {
            "ticker": ticker,
            "threshold": threshold_value,
            "email": email,
        }

        response = requests.post(backend_url, json=payload, timeout=30)

        if response.status_code in (200, 201, 202):
            try:
                data = response.json()
                alert = data.get("alert", {})
                status = alert.get("alert_status", "CHECKED")
                message = alert.get("message")
                msg = message or f"Alert check completed: {status}."
                notification = data.get("email_notification")
                if notification and not notification.get("sent"):
                    msg = f"{msg} {notification.get('message', '')}".strip()
            except Exception:
                msg = "Alert check completed successfully."
            return True, msg
        try:
            error_text = response.text
        except Exception:
            error_text = "Unknown error"
        return False, f"Backend error {response.status_code}: {error_text}"

    except requests.exceptions.ConnectionError:
        return False, (
            f"Could not connect to the backend at {backend_url}. "
            "Please make sure FastAPI is running."
        )
    except Exception as e:
        return False, f"Request failed: {e}"


def render_alert_config():
    st.markdown("## Configure Stock Price Alerts")
    st.markdown(
        "Set up automated alerts for stock price movements. "
        "You'll receive notifications via email when your conditions are met."
    )

    st.markdown("---")

    st.caption(f"Direct alert check via FastAPI: {get_backend_url()}")

    # Create form
    with st.form("alert_config_form", clear_on_submit=False):
        st.markdown("### Alert Configuration")

        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input(
                "Email Address *",
                placeholder="your.email@example.com",
                help="Email address where you'll receive alerts",
            )

            ticker = st.text_input(
                "Stock Ticker *",
                placeholder="RELIANCE.NS or AAPL",
                help="Stock symbol to monitor (e.g., RELIANCE.NS for Indian stocks, AAPL for US stocks)",
            ).upper()

        with col2:
            threshold_type = st.selectbox(
                "Threshold Type *",
                ["Percentage Drop"],
                help="Choose how you want to define the alert threshold",
            )

            if threshold_type == "Percentage Drop":
                threshold_value = st.number_input(
                    "Threshold Value (%) *",
                    min_value=0.1,
                    max_value=100.0,
                    value=5.0,
                    step=0.1,
                    help="Alert when price drops by this percentage",
                )

        st.markdown("---")

        # Submit button
        submitted = st.form_submit_button("Configure Alert", use_container_width=True)

        if submitted:
            # Validation
            errors = []

            # Email validation
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not email:
                errors.append("Email address is required")
            elif not re.match(email_pattern, email):
                errors.append("Invalid email address format")

            # Ticker validation
            if not ticker:
                errors.append("Stock ticker is required")
            elif len(ticker) < 1:
                errors.append("Invalid ticker symbol")

            # Threshold validation
            if threshold_value <= 0:
                errors.append("Threshold value must be greater than 0")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Run the alert check through the backend.
                with st.spinner("Configuring alert..."):
                    success, message = send_alert_config(
                        email=email,
                        ticker=ticker,
                        threshold_type=threshold_type,
                        threshold_value=threshold_value,
                    )

                if success:
                    st.success(f"{message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")

    # Info section
    st.markdown("---")
    st.info(
        """
    **How it works:**
    1. Enter your email address and the stock ticker you want to monitor  
    2. Choose your alert threshold (percentage drop)  
    3. Click "Configure Alert" to run a live price check  
    4. The FastAPI backend calculates the alert status directly  

    **Note:** This direct mode checks the current alert immediately and sends an
    email only when the configured threshold is exceeded. It does not persist
    subscriptions for future automatic checks.
    """
    )
