import streamlit as st

def render_header():
    """Render the header of the app"""
    
    st.markdown(
        """
        <div class="header-container">
            <h1>LoL Pre-Game Analysis</h1>
            <p>Powered by AI to give you the competitive edge before the match begins.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # If analysis has been performed, show a summary
    if st.session_state.get("analysis_performed", False):
        st.markdown("---")
        
        # Get analysis data
        team_analysis = st.session_state.analysis_results.get("team_analysis", {})
        matchup_insights = st.session_state.analysis_results.get("matchup_insights", {})
        
        # Display summary info
        cols = st.columns(3)
        
        with cols[0]:
            # Team composition summary
            st.markdown(
                f"""
                <div class="stat-card">
                    <h3>Team Composition</h3>
                    <p>{team_analysis.get('summary', 'Analysis not available')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with cols[1]:
            # Win conditions
            win_conditions = team_analysis.get('win_conditions', [])
            if win_conditions:
                win_conditions_html = "".join([f"<li>{condition}</li>" for condition in win_conditions])
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <h3>Win Conditions</h3>
                        <ul>{win_conditions_html}</ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="stat-card">
                        <h3>Win Conditions</h3>
                        <p>Analysis not available</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with cols[2]:
            # Overall matchup assessment
            if matchup_insights:
                # Count favorable matchups
                favorable_count = sum(
                    1 for lane in ["top", "jungle", "mid", "adc", "support"]
                    if lane in matchup_insights and matchup_insights[lane].get("favorable", False)
                )
                
                # Calculate overall assessment
                total_lanes = 5
                favorable_percent = (favorable_count / total_lanes) * 100
                
                if favorable_percent >= 60:
                    assessment = "Favorable Draft"
                    color = "var(--success-color)"
                elif favorable_percent >= 40:
                    assessment = "Even Draft"
                    color = "var(--warning-color)"
                else:
                    assessment = "Challenging Draft"
                    color = "var(--danger-color)"
                
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <h3>Draft Assessment</h3>
                        <p style="font-size: 1.5rem; color: {color}; font-weight: bold;">{assessment}</p>
                        <p>{favorable_count}/{total_lanes} favorable matchups</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="stat-card">
                        <h3>Draft Assessment</h3>
                        <p>Analysis not available</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )