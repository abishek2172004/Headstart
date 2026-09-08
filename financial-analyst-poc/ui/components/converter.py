import streamlit as st
import requests


def render_currency_converter():
    """USD to INR Converter Widget"""
    st.markdown("### Currency Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        usd_amount = st.number_input(
            "USD Amount",
            min_value=0.0,
            value=100.0,
            step=10.0,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<div style='text-align: center; padding-top: 0.5rem;'>USD to INR</div>", 
                    unsafe_allow_html=True)
    
    with col3:
        # Try to fetch live rate, fallback to fixed rate
        try:
            response = requests.get(
                "https://api.exchangerate-api.com/v4/latest/USD",
                timeout=3
            )
            if response.status_code == 200:
                rate = response.json().get("rates", {}).get("INR", 83.0)
            else:
                rate = 83.0
        except:
            rate = 83.0  # Fallback rate
        
        inr_amount = usd_amount * rate
        st.markdown(
            f"<div style='font-size: 1.2rem; font-weight: bold; color: #22c55e;'>"
            f"₹ {inr_amount:,.2f}</div>",
            unsafe_allow_html=True
        )
    
    st.caption(f"Exchange Rate: 1 USD = ₹{rate:.2f}")
