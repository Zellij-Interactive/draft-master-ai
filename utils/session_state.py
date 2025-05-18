import streamlit as st
import os

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "summoner_name" not in st.session_state:
        st.session_state.summoner_name = ""
    
    if "region" not in st.session_state:
        st.session_state.region = "EUW1"  # Updated to match Riot API region format
    
    if "analysis_performed" not in st.session_state:
        st.session_state.analysis_performed = False
    
    if "team_comp" not in st.session_state:
        st.session_state.team_comp = {
            "blue": ["", "", "", "", ""],
            "red": ["", "", "", "", ""]
        }
    
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = {
            "team_analysis": {},
            "player_analysis": {},
            "matchup_insights": {}
        }
    
    # Initialize API keys from environment variables
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if "RIOT_API_KEY" not in st.session_state:
        st.session_state.RIOT_API_KEY = os.getenv("RIOT_API_KEY")

def reset_analysis():
    """Reset analysis data"""
    st.session_state.analysis_performed = False
    st.session_state.analysis_results = {
        "team_analysis": {},
        "player_analysis": {},
        "matchup_insights": {}
    }

def update_team_comp(side, position, champion):
    """Update team composition"""
    positions = ["Top", "Jungle", "Mid", "ADC", "Support"]
    idx = positions.index(position)
    st.session_state.team_comp[side][idx] = champion