import streamlit as st


def render_sdg_goals():
    """SDG Goals Component - Collapsible"""
    
    sdg_data = {
        "SDG 8 - Decent Work and Economic Growth": {
            "color": "#A21942",
            "points": [
                "Supports better financial decision-making",
                "Helps investors and businesses plan investments",
                "Identifies market trends and opportunities",
                "Encourages economic growth using data insights"
            ]
        },
        "SDG 9 - Industry, Innovation and Infrastructure": {
            "color": "#DD1C3B",
            "points": [
                "Uses AI and modern technologies",
                "Represents innovation in FinTech",
                "Built using full-stack development",
                "Enables intelligent financial systems"
            ]
        },
        "SDG 12 - Responsible Consumption and Production": {
            "color": "#BF8B2E",
            "points": [
                "Promotes responsible financial behavior",
                "Reduces impulsive investment decisions",
                "Encourages data-driven investments",
                "Minimizes financial risks"
            ]
        },
        "SDG 10 - Reduced Inequalities": {
            "color": "#DD1C3B",
            "points": [
                "Provides affordable financial insights",
                "Makes analysis accessible to beginners",
                "Supports small businesses and individuals",
                "Reduces dependency on expensive tools"
            ]
        },
        "SDG 17 - Partnerships for the Goals": {
            "color": "#0A3161",
            "points": [
                "Integrates multiple APIs and data sources",
                "Combines AI, automation, and finance",
                "Encourages collaboration between tech and finance",
                "Supports connected financial systems"
            ]
        }
    }
    
    with st.expander("Learn about our SDG Impact", expanded=False):
        st.markdown("### UN Sustainable Development Goals")
        st.markdown("HeadStart contributes to multiple SDG targets through technology and innovation.")
        
        cols = st.columns(2)
        for idx, (goal_title, goal_info) in enumerate(sdg_data.items()):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, {goal_info["color"]}22, {goal_info["color"]}11);
                        border-left: 4px solid {goal_info["color"]};
                        padding: 1rem;
                        border-radius: 8px;
                        margin-bottom: 1rem;
                    '>
                        <h4 style='margin: 0 0 0.5rem 0; color: {goal_info["color"]};'>{goal_title}</h4>
                        <ul style='margin: 0; padding-left: 1.2rem;'>
                """, unsafe_allow_html=True)
                
                for point in goal_info["points"]:
                    st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
