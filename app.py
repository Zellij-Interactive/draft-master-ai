import streamlit as st
from dotenv import load_dotenv
import os

from components.sidebar import render_sidebar
from components.header import render_header
from components.team_analysis import render_team_analysis
from components.player_analysis import render_player_analysis
from components.matchup_insights import render_matchup_insights
from utils.session_state import initialize_session_state

# Load environment variables
load_dotenv()  # This will load from .env by default
if os.path.exists(""):
    load_dotenv("", override=True)

# App configuration
st.set_page_config(
    page_title="LoL Pre-Game Analysis",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render header
    render_header()
    
    # If analysis has been performed
    if st.session_state.get("analysis_performed", False):
        # Main analysis tabs
        tabs = st.tabs(["Team Analysis", "Player Analysis", "Matchup Insights"])
        
        with tabs[0]:
            render_team_analysis()
            
        with tabs[1]:
            render_player_analysis()
            
        with tabs[2]:
            render_matchup_insights()
    else:
        # Welcome screen
        st.markdown("""
        <div class="welcome-container">
            <h2>Welcome to LoL Pre-Game Analysis</h2>
            <p>Enter your summoner name and team information in the sidebar to get started.</p>
            <div class="features-grid">
                <div class="feature-card">
                    <h3>Team Composition</h3>
                    <p>Analyze team synergies and weaknesses</p>
                </div>
                <div class="feature-card">
                    <h3>Player Insights</h3>
                    <p>Review performance stats and tendencies</p>
                </div>
                <div class="feature-card">
                    <h3>Matchup Analysis</h3>
                    <p>Get lane-specific tips and strategies</p>
                </div>
                <div class="feature-card">
                    <h3>Win Predictions</h3>
                    <p>AI-powered match outcome forecasting</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()