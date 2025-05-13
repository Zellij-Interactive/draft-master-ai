import streamlit as st
from utils.lol_data import get_summoner_data, get_champion_icon_url

def render_player_analysis():
    """Render the player analysis section"""
    
    # Get analysis data
    player_analysis = st.session_state.analysis_results.get("player_analysis", {})
    
    if not player_analysis:
        st.warning("Player analysis data is not available.")
        return
    
    # Get summoner data
    summoner_name = st.session_state.get("summoner_name", "")
    region = st.session_state.get("region", "NA")
    
    if not summoner_name:
        st.warning("Summoner name is not available.")
        return
    
    summoner_data = get_summoner_data(summoner_name, region)
    
    # Player header with summoner info
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0;">
            <h2 style="color: var(--lol-gold);">Player Analysis</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Show summoner info
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Placeholder for summoner icon
        st.markdown(
            """
            <div style="background-color: var(--lol-blue-light); width: 100px; height: 100px; 
                        border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                        justify-content: center; border: 2px solid var(--lol-gold);">
                <span style="font-size: 36px; color: var(--lol-gold);">👤</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Summoner info
        st.markdown(
            f"""
            <div style="padding: 10px;">
                <h3 style="color: var(--lol-gold); margin-bottom: 5px;">{summoner_data['name']}</h3>
                <p>Level: {summoner_data['level']} | Rank: {summoner_data['rank']}</p>
                <p>Win Rate: {summoner_data['winRate']} | Main Role: {summoner_data['mainRole']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        # Top champions
        st.markdown("<div style='text-align: center;'><h4>Top Champions</h4></div>", unsafe_allow_html=True)
        
        for champion in summoner_data['topChampions'][:3]:
            icon_url = get_champion_icon_url(champion)
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin: 5px 0;">
                    <img src="{icon_url}" width="24" height="24" class="champion-icon" style="margin-right: 10px;">
                    <span>{champion}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Recent matches section
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: var(--lol-gold);'>Recent Matches</h3>", unsafe_allow_html=True)
    
    # Limit to 5 recent matches
    recent_matches = summoner_data['recentMatches'][:5]
    
    # Create a row for recent matches
    match_cols = st.columns(len(recent_matches))
    
    for i, match in enumerate(recent_matches):
        with match_cols[i]:
            # Set color based on result
            result_color = "var(--success-color)" if match['result'] == "Victory" else "var(--danger-color)"
            
            # Get champion icon
            icon_url = get_champion_icon_url(match['champion'])
            
            st.markdown(
                f"""
                <div style="text-align: center; padding: 10px; background-color: var(--lol-blue-light); 
                            border-radius: 5px; border-left: 3px solid {result_color};">
                    <img src="{icon_url}" width="40" height="40" style="border-radius: 50%; margin-bottom: 5px;">
                    <p style="margin: 5px 0; font-weight: bold; color: {result_color};">{match['result']}</p>
                    <p>KDA: {match['kda']}</p>
                    <p>CS: {match['cs']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Champion-specific analysis
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Determine which champion to analyze
    perspective = st.session_state.get("perspective", "Blue")
    positions = ["Top", "Jungle", "Mid", "ADC", "Support"]
    
    # Find the first non-empty champion
    player_champion = None
    player_position = None
    
    for i, pos in enumerate(positions):
        if perspective == "Blue" and st.session_state.team_comp["blue"][i]:
            player_champion = st.session_state.team_comp["blue"][i]
            player_position = pos
            break
        elif perspective == "Red" and st.session_state.team_comp["red"][i]:
            player_champion = st.session_state.team_comp["red"][i]
            player_position = pos
            break
    
    if not player_champion:
        st.warning("No champion selected for analysis.")
        return
    
    # Champion analysis header
    icon_url = get_champion_icon_url(player_champion)
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="{icon_url}" width="64" height="64" style="border-radius: 50%; margin-right: 15px; border: 2px solid var(--lol-gold);">
            <div>
                <h3 style="color: var(--lol-gold); margin: 0;">{player_champion} Analysis</h3>
                <p style="margin: 5px 0 0 0;">Position: {player_position}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Player analysis summary
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>Champion Performance Assessment</h3>
            <p>{player_analysis.get('summary', 'No summary available')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Strengths and areas for improvement
    col1, col2 = st.columns(2)
    
    with col1:
        strengths = player_analysis.get('strengths', [])
        if strengths:
            strengths_html = "".join([f"<li>{strength}</li>" for strength in strengths])
            st.markdown(
                f"""
                <div class="insight-card">
                    <h3>Champion Strengths</h3>
                    <ul>{strengths_html}</ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="insight-card">
                    <h3>Champion Strengths</h3>
                    <p>No strengths identified</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with col2:
        improvements = player_analysis.get('improvements', [])
        if improvements:
            improvements_html = "".join([f"<li>{improvement}</li>" for improvement in improvements])
            st.markdown(
                f"""
                <div class="insight-card">
                    <h3>Areas for Improvement</h3>
                    <ul>{improvements_html}</ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="insight-card">
                    <h3>Areas for Improvement</h3>
                    <p>No areas for improvement identified</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Itemization
    itemization = player_analysis.get('itemization', [])
    if itemization:
        itemization_html = "".join([f"<li>{item}</li>" for item in itemization])
        st.markdown(
            f"""
            <div class="insight-card">
                <h3>Recommended Itemization</h3>
                <ul>{itemization_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="insight-card">
                <h3>Recommended Itemization</h3>
                <p>No itemization recommendations available</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Performance metrics
    performance_metrics = player_analysis.get('performance_metrics', {})
    if performance_metrics:
        st.markdown("<h3 style='color: var(--lol-gold); margin-top: 20px;'>Key Performance Metrics</h3>", unsafe_allow_html=True)
        
        metrics_cols = st.columns(min(3, len(performance_metrics)))
        
        # Convert dict to list of (key, value) pairs for iteration
        metrics_list = list(performance_metrics.items())
        
        for i, (metric, description) in enumerate(metrics_list):
            with metrics_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background-color: var(--lol-blue-light); padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid var(--lol-gold);">
                        <h4 style="margin: 0 0 10px 0; color: var(--lol-gold);">{metric}</h4>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )