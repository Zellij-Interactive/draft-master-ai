import streamlit as st
from utils.lol_data import get_champion_icon_url

def render_team_analysis():
    """Render the team analysis section"""
    
    # Get analysis data
    team_analysis = st.session_state.analysis_results.get("team_analysis", {})
    
    if not team_analysis:
        st.warning("Team analysis data is not available.")
        return
    
    # Team composition overview
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0;">
            <h2 style="color: var(--lol-gold);">Team Composition Analysis</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Show champions in the team
    perspective = st.session_state.get("perspective", "Blue")
    team_champions = st.session_state.team_comp.get(perspective.lower(), [""] * 5)
    
    # Show champion icons
    st.markdown("<div style='display: flex; justify-content: center; padding: 20px 0;'>", unsafe_allow_html=True)
    
    for champion in team_champions:
        if champion:
            icon_url = get_champion_icon_url(champion)
            st.markdown(
                f"""
                <div style="text-align: center; margin: 0 10px;">
                    <img src="{icon_url}" width="64" height="64" class="champion-icon" alt="{champion}">
                    <p style="margin-top: 5px; font-size: 0.9rem;">{champion}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Team composition summary
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>Composition Overview</h3>
            <p>{team_analysis.get('summary', 'No summary available')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Strengths and weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        strengths = team_analysis.get('strengths', [])
        if strengths:
            strengths_html = "".join([f"<li>{strength}</li>" for strength in strengths])
            st.markdown(
                f"""
                <div class="insight-card">
                    <h3>Team Strengths</h3>
                    <ul>{strengths_html}</ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="insight-card">
                    <h3>Team Strengths</h3>
                    <p>No strengths identified</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with col2:
        weaknesses = team_analysis.get('weaknesses', [])
        if weaknesses:
            weaknesses_html = "".join([f"<li>{weakness}</li>" for weakness in weaknesses])
            st.markdown(
                f"""
                <div class="insight-card">
                    <h3>Team Weaknesses</h3>
                    <ul>{weaknesses_html}</ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="insight-card">
                    <h3>Team Weaknesses</h3>
                    <p>No weaknesses identified</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Team scaling and playstyle
    scaling = team_analysis.get('scaling', 'Not available')
    playstyle = team_analysis.get('playstyle', 'Not available')
    teamfight = team_analysis.get('teamfight', 'Not available')
    
    st.markdown(
        """
        <div style="padding: 20px 0 10px 0;">
            <h3 style="color: var(--lol-gold);">Strategic Analysis</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Show scaling as a visual indicator
    if scaling and "10" in scaling:
        try:
            # Try to extract a number from the scaling text
            scaling_parts = scaling.split('/')
            if len(scaling_parts) >= 1:
                scaling_value = scaling_parts[0].strip()
                try:
                    scaling_number = int(scaling_value)
                    
                    # Show as a progress bar
                    st.markdown(
                        f"""
                        <div class="insight-card">
                            <h3>Team Scaling</h3>
                            <p>{scaling}</p>
                            <div class="progress-container">
                                <div class="progress-label">
                                    <span>Early Game</span>
                                    <span>Late Game</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {scaling_number * 10}%;"></div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except ValueError:
                    st.markdown(
                        f"""
                        <div class="insight-card">
                            <h3>Team Scaling</h3>
                            <p>{scaling}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    f"""
                    <div class="insight-card">
                        <h3>Team Scaling</h3>
                        <p>{scaling}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except Exception:
            st.markdown(
                f"""
                <div class="insight-card">
                    <h3>Team Scaling</h3>
                    <p>{scaling}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            f"""
            <div class="insight-card">
                <h3>Team Scaling</h3>
                <p>{scaling}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Playstyle and teamfight
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="insight-card">
                <h3>Recommended Playstyle</h3>
                <p>{playstyle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="insight-card">
                <h3>Team Fight Analysis</h3>
                <p>{teamfight}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Win conditions
    win_conditions = team_analysis.get('win_conditions', [])
    if win_conditions:
        win_conditions_html = "".join([f"<li>{condition}</li>" for condition in win_conditions])
        st.markdown(
            f"""
            <div class="insight-card">
                <h3>Win Conditions</h3>
                <ul>{win_conditions_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="insight-card">
                <h3>Win Conditions</h3>
                <p>No win conditions identified</p>
            </div>
            """,
            unsafe_allow_html=True
        )