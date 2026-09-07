import streamlit as st
import os
import sys

# Add the project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set page config MUST be the first Streamlit command
st.set_page_config(
    page_title="HeadStart - Financial Decision Support",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components after page config
from ui.components.dashboard import render_dashboard
from ui.components.stock_page import render_stock_page
from ui.components.alert_config import render_alert_config
from ui.components.charts_page import render_charts_page
from ui.components.converter import render_currency_converter
from ui.components.sdg_goals import render_sdg_goals
from ui.components.assistant_page import run_assistant_page

# Theme Configuration - Premium Colors
DARK_THEME = {
    "--primary-color": "#6366F1",
    "--secondary-color": "#EC4899",
    "--bg-color": "#0F172A",
    "--card-bg": "#1E293B",
    "--sidebar-bg": "#0F172A",
    "--text-color": "#F1F5F9",
    "--text-muted": "#94A3B8",
    "--border-color": "#334155",
    "--input-bg": "#1E293B",
    "--font-family": "'Inter', sans-serif"
}

LIGHT_THEME = {
    "--primary-color": "#6366F1",
    "--secondary-color": "#EC4899",
    "--bg-color": "#F8FAFC",
    "--card-bg": "#FFFFFF",
    "--sidebar-bg": "#FFFFFF",
    "--text-color": "#0F172A",
    "--text-muted": "#64748B",
    "--border-color": "#E2E8F0",
    "--input-bg": "#F1F5F9",
    "--font-family": "'Inter', sans-serif"
}

# Load Custom CSS with Theme
def load_css(file_path, theme):
    with open(file_path) as f:
        css_content = f.read()
    
    # Generate :root variables
    root_vars = ":root {\n"
    for var, value in theme.items():
        root_vars += f"    {var}: {value};\n"
    root_vars += "}\n"
    
    st.markdown(f"<style>{root_vars}{css_content}</style>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("HeadStart")
st.sidebar.markdown(
    """
    <div style='text-align: center; margin-bottom: 1rem;'>
    <p style='font-size: 0.85rem; color: var(--text-muted); margin-top: -0.5rem;'>
    <em>A Financial Decision Support System</em>
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Theme Toggle
is_light_mode = st.sidebar.toggle("☀️ Light Mode", value=False)
current_theme = LIGHT_THEME if is_light_mode else DARK_THEME
plotly_template = "plotly_white" if is_light_mode else "plotly_dark"

# Path to CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    load_css(css_path, current_theme)

st.sidebar.markdown("---")

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

page_options = ["Dashboard", "Stock Analysis", "Charts", "Alert Config", "AI Assistant"]
page = st.sidebar.radio(
    "Navigate",
    page_options,
    index=page_options.index(st.session_state.current_page)
)
if page != st.session_state.current_page:
    st.session_state.current_page = page

st.sidebar.markdown("---")
st.sidebar.caption("Financial intelligence for faster decisions")

# ============= MODERN HERO HEADER =============
st.markdown("""
<div class="hero-shell">
    <div class="hero-orb orb-one"></div>
    <div class="hero-orb orb-two"></div>
    <div class="hero-panel">
        <div class="eyebrow">AI-powered portfolio intelligence</div>
        <h1>
            <span class="brand-blue">Head</span><span class="brand-green">Start</span>
        </h1>
        <p class="hero-subtitle">Financial Decision Support System</p>
    </div>
</div>
""", unsafe_allow_html=True)

hero_buttons = [
    ("Market Insights", "Dashboard"),
    ("Stock Analysis", "Stock Analysis"),
    ("AI Assistant", "AI Assistant")
]
hero_cols = st.columns(3)
for col, (label, target) in zip(hero_cols, hero_buttons):
    with col:
        if st.button(label, key=f"hero_nav_{target}", use_container_width=True):
            st.session_state.current_page = target
            st.rerun()

st.markdown("---")

# Main Content Routing
page = st.session_state.get("current_page", "Dashboard")

if page == "Dashboard":
    render_dashboard(plotly_template)
elif page == "Stock Analysis":
    render_stock_page(plotly_template)
elif page == "Charts":
    render_charts_page(plotly_template)
elif page == "Alert Config":
    render_alert_config()
elif page == "AI Assistant":
    run_assistant_page()

# Footer Components
st.markdown("---")
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

# Currency Converter
col1, col2 = st.columns([1, 1])
with col1:
    render_currency_converter()

with col2:
    render_sdg_goals()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 1rem; color: gray; font-size: 0.85rem;'>
    <p><strong>HeadStart</strong> - Financial Decision Support System</p>
    <p>Powered by LangGraph, Groq AI, and Real-time Market Data</p>
    <p style='margin-top: 1rem;'>Built with Streamlit | Data from YFinance</p>
</div>
""", unsafe_allow_html=True)
