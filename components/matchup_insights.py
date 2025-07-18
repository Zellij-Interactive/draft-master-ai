import streamlit as st
from utils.lol_data import get_champion_icon_url

def render_matchup_insights():
    """Render the matchup insights section"""
    
    # Get analysis data
    matchup_insights = st.session_state.analysis_results.get("matchup_insights", {})
    
    if not matchup_insights:
        st.warning("Matchup insights data is not available.")
        return
    
    # Matchup header
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0;">
            <h2 style="color: var(--lol-gold);">Lane Matchup Analysis</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Team compositions
    blue_team = st.session_state.team_comp.get("blue", [""] * 5)
    red_team = st.session_state.team_comp.get("red", [""] * 5)
    perspective = st.session_state.get("perspective", "Blue")
    
    # Positions
    positions = ["top", "jungle", "mid", "adc", "support"]
    position_display = ["Top", "Jungle", "Mid", "ADC", "Support"]
    
    # Create a matchup visual
    st.markdown("<div style='display: flex; justify-content: center; margin-bottom: 30px;'>", unsafe_allow_html=True)
    
    # Blue team
    st.markdown("<div style='text-align: center; margin-right: 40px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #5383E8;'>Blue Team</h3>", unsafe_allow_html=True)
    
    for champion in blue_team:
        if champion:
            icon_url = get_champion_icon_url(champion)
            st.markdown(
                f"""
                <div style="margin: 10px 0;">
                    <img src="{icon_url}" width="48" height="48" class="champion-icon" style="border: 2px solid #5383E8;" alt="{champion}">
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # VS indicator
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; justify-content: center; margin: 0 10px;">
            <div style="font-size: 24px; font-weight: bold; color: var(--lol-gold); margin-bottom: 10px;">VS</div>
            <div style="font-size: 20px; color: var(--lol-gold);">↕️</div>
            <div style="font-size: 20px; color: var(--lol-gold);">↕️</div>
            <div style="font-size: 20px; color: var(--lol-gold);">↕️</div>
            <div style="font-size: 20px; color: var(--lol-gold);">↕️</div>
            <div style="font-size: 20px; color: var(--lol-gold);">↕️</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Red team
    st.markdown("<div style='text-align: center; margin-left: 40px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #E84057;'>Red Team</h3>", unsafe_allow_html=True)
    
    for champion in red_team:
        if champion:
            icon_url = get_champion_icon_url(champion)
            st.markdown(
                f"""
                <div style="margin: 10px 0;">
                    <img src="{icon_url}" width="48" height="48" class="champion-icon" style="border: 2px solid #E84057;" alt="{champion}">
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Lane matchup analysis
    for i, position in enumerate(positions):
        if position in matchup_insights:
            matchup = matchup_insights[position]
            
            # Determine which champions are in this matchup
            blue_champion = blue_team[i] if i < len(blue_team) else "Unknown"
            red_champion = red_team[i] if i < len(red_team) else "Unknown"
            
            # Create matchup card
            with st.container():
                # Card header with champion matchup
                st.markdown(
                    f"""
                    <div style="background-color: var(--lol-blue-light); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: var(--lol-gold); margin-bottom: 10px;">{position_display[i]} Lane: {blue_champion} vs {red_champion}</h3>
                    """,
                    unsafe_allow_html=True
                )
                
                # Determine advantage color and icon
                favorable = matchup.get("favorable", False)
                advantage_text = matchup.get("advantage", "Unknown")
                
                if favorable:
                    advantage_color = "var(--success-color)"
                    advantage_icon = "↗️"
                elif advantage_text == "Even":
                    advantage_color = "var(--warning-color)"
                    advantage_icon = "↔️"
                else:
                    advantage_color = "var(--danger-color)"
                    advantage_icon = "↘️"
                
                # Advantage indicator
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; margin: 10px 0;">
                        <span style="font-size: 1.2rem; font-weight: bold; color: {advantage_color}; margin-right: 10px;">
                            {advantage_icon} {advantage_text}
                        </span>
                        <span>
                            {perspective} team {favorable and "has advantage" or "is at a disadvantage"}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Tips section
                st.markdown(
                    """
                    <div style="margin-top: 15px;">
                        <h4 style="color: var(--lol-gold);">Key Tips</h4>
                        <ul style="list-style-type: disc; margin-left: 20px;">
                    """,
                    unsafe_allow_html=True
                )
                
                for tip in matchup.get("tips", ["No tips available"]):
                    st.markdown(f"<li>{tip}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
                
                # Counter strategy section
                st.markdown(
                    f"""
                    <div style="margin-top: 15px;">
                        <h4 style="color: var(--lol-gold);">Counter Strategy</h4>
                        <p>{matchup.get("counter_strategy", "No counter strategy available")}</p>
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )