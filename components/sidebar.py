import streamlit as st
from utils.lol_data import get_regions, load_champion_list, get_champion_roles
from utils.openai_utils import get_analysis
from utils.session_state import update_team_comp, reset_analysis

def render_sidebar():
    """Render the sidebar for input and controls"""
    with st.sidebar:
        st.markdown("<h2 style='color: #C89B3C;'>Input Details</h2>", unsafe_allow_html=True)
        
        # Personal info
        st.markdown("### Your Details")
        
        # Summoner name input
        summoner_name = st.text_input(
            "Summoner Name",
            value=st.session_state.get("summoner_name", ""),
            placeholder="Enter your summoner name"
        )
        
        # Region selection
        region = st.selectbox(
            "Region",
            options=get_regions(),
            index=get_regions().index(st.session_state.get("region", "NA1"))
        )
        
        # Team composition
        st.markdown("### Team Composition")
        
        # Tab selection for Blue/Red team
        team_tabs = st.tabs(["Blue Team", "Red Team"])
        
        positions = ["Top", "Jungle", "Mid", "ADC", "Support"]
        champion_list = load_champion_list()
        roles_map = get_champion_roles()
        
        # Your team (Blue)
        with team_tabs[0]:
            st.markdown("#### Blue Side")
            for i, position in enumerate(positions):
                # Filter champions by position
                position_champions = roles_map.get(position, champion_list)
                
                # Add empty option first
                position_champions = [""] + position_champions
                
                # Get current value
                current_value = st.session_state.team_comp["blue"][i] if i < len(st.session_state.team_comp["blue"]) else ""
                
                # If current value not in list, default to empty
                if current_value not in position_champions:
                    current_value = ""
                
                # Champion selection
                champion = st.selectbox(
                    f"{position} Champion",
                    options=position_champions,
                    index=position_champions.index(current_value),
                    key=f"blue_{position}"
                )
                
                # Update team comp
                if champion:
                    update_team_comp("blue", position, champion)
        
        # Enemy team (Red)
        with team_tabs[1]:
            st.markdown("#### Red Side")
            for i, position in enumerate(positions):
                # Filter champions by position
                position_champions = roles_map.get(position, champion_list)
                
                # Add empty option first
                position_champions = [""] + position_champions
                
                # Get current value
                current_value = st.session_state.team_comp["red"][i] if i < len(st.session_state.team_comp["red"]) else ""
                
                # If current value not in list, default to empty
                if current_value not in position_champions:
                    current_value = ""
                
                # Champion selection
                champion = st.selectbox(
                    f"{position} Champion",
                    options=position_champions,
                    index=position_champions.index(current_value),
                    key=f"red_{position}"
                )
                
                # Update team comp
                if champion:
                    update_team_comp("red", position, champion)
        
        # Analysis settings
        st.markdown("### Analysis Settings")
        
        perspective = st.radio(
            "Analysis Perspective",
            options=["Blue", "Red"],
            index=0,
            key="perspective"
        )
        
        # Analyze button
        if st.button("Generate Analysis", type="primary"):
            with st.spinner("Generating comprehensive analysis..."):
                # Update session state
                st.session_state.summoner_name = summoner_name
                st.session_state.region = region
                
                # Validate inputs
                blue_team = st.session_state.team_comp["blue"]
                red_team = st.session_state.team_comp["red"]
                
                if "" in blue_team or "" in red_team:
                    st.error("Please fill in all champion selections for both teams.")
                    return
                
                if not summoner_name:
                    st.error("Please enter your summoner name.")
                    return
                
                # Get team analysis
                team_analysis = get_analysis("team_analysis", {
                    "blue": blue_team,
                    "red": red_team,
                    "side": perspective
                })
                
                # Get player analysis
                # Find the champion played by the summoner
                player_position = positions[0]  # Default to top
                player_champion = blue_team[0]  # Default to top champion
                
                if perspective == "Blue":
                    for i, position in enumerate(positions):
                        player_position = position
                        player_champion = blue_team[i]
                else:
                    for i, position in enumerate(positions):
                        player_position = position
                        player_champion = red_team[i]
                
                player_analysis = get_analysis("player_analysis", {
                    "summoner_name": summoner_name,
                    "region": region,
                    "champion": player_champion,
                    "role": player_position
                })
                
                # Get matchup insights
                matchup_insights = get_analysis("matchup_insights", {
                    "blue": blue_team,
                    "red": red_team,
                    "perspective": perspective
                })
                
                # Store results
                st.session_state.analysis_results = {
                    "team_analysis": team_analysis,
                    "player_analysis": player_analysis,
                    "matchup_insights": matchup_insights
                }
                
                # Set analysis performed flag
                st.session_state.analysis_performed = True
        
        # Reset button
        if st.button("Reset Analysis", type="secondary"):
            reset_analysis()
            st.experimental_rerun()
        
        # API key configuration section
        st.markdown("---")
        st.markdown("### API Configuration")
        
        # OpenAI API key input
        if not st.session_state.get("OPENAI_API_KEY"):
            st.info(
                "To generate analysis, you need to set your OpenAI API key. "
                "You can add it to a .env file with OPENAI_API_KEY=your_key."
            )
            
            openai_api_key = st.text_input("OpenAI API Key", type="password", key="openai_key")
            if openai_api_key:
                st.session_state.OPENAI_API_KEY = openai_api_key
                st.success("OpenAI API key set for this session!")
        
        # Riot API key input
        if not st.session_state.get("RIOT_API_KEY"):
            st.info(
                "To fetch real summoner data, you need to set your Riot API key. "
                "You can add it to a .env file with RIOT_API_KEY=your_key."
            )
            
            riot_api_key = st.text_input("Riot API Key", type="password", key="riot_key")
            if riot_api_key:
                st.session_state.RIOT_API_KEY = riot_api_key
                st.success("Riot API key set for this session!")