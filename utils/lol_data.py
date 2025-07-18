import os
import json
import streamlit as st
import requests
from typing import Dict, List, Any

# Champion data
@st.cache_data
def load_champion_list():
    """Load list of LoL champions from Data Dragon API"""
    try:
        # Get latest version
        versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        versions_response = requests.get(versions_url)
        versions_response.raise_for_status()
        latest_version = versions_response.json()[0]
        
        # Get champion data
        champions_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
        champions_response = requests.get(champions_url)
        champions_response.raise_for_status()
        champions_data = champions_response.json()
        
        # Extract champion names and sort alphabetically
        champion_list = sorted(champions_data["data"].keys())
        return champion_list
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching champion data: {str(e)}")
        # Fallback to empty list if API fails
        return []

@st.cache_data
def get_champion_roles():
    """Get champion roles from Data Dragon API"""
    try:
        # Get latest version
        versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        versions_response = requests.get(versions_url)
        versions_response.raise_for_status()
        latest_version = versions_response.json()[0]
        
        # Get champion data
        champions_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
        champions_response = requests.get(champions_url)
        champions_response.raise_for_status()
        champions_data = champions_response.json()
        
        # Initialize role lists
        roles = {
            "Top": [],
            "Jungle": [],
            "Mid": [],
            "ADC": [],
            "Support": []
        }
        
        # Map Data Dragon tags to roles
        role_mapping = {
            "Fighter": ["Top", "Jungle"],
            "Tank": ["Top", "Support", "Jungle"],
            "Mage": ["Mid", "Support"],
            "Assassin": ["Mid", "Jungle"],
            "Marksman": ["ADC"],
            "Support": ["Support"]
        }
        
        # Categorize champions by their tags
        for champ_name, champ_data in champions_data["data"].items():
            for tag in champ_data["tags"]:
                for role in role_mapping.get(tag, []):
                    if champ_name not in roles[role]:
                        roles[role].append(champ_name)
        
        # Sort champions in each role
        for role in roles:
            roles[role].sort()
        
        return roles
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching champion roles: {str(e)}")
        # Return empty role lists if API fails
        return {role: [] for role in ["Top", "Jungle", "Mid", "ADC", "Support"]}

def get_regions():
    """Get list of LoL regions"""
    return ["NA1", "EUW1", "EUNE1", "KR", "BR1", "LA1", "LA2", "OC1", "RU", "TR1", "JP1"]

def get_region_routing(region: str) -> str:
    """Get routing value for a region"""
    region_routes = {
        "NA1": "americas",
        "BR1": "americas",
        "LA1": "americas",
        "LA2": "americas",
        "EUW1": "europe",
        "EUNE1": "europe",
        "TR1": "europe",
        "RU": "europe",
        "KR": "asia",
        "JP1": "asia",
        "OC1": "sea"
    }
    return region_routes.get(region, "americas")

def get_summoner_data(summoner_name: str, region: str) -> Dict[str, Any]:
    """Get summoner data from Riot API"""
    # Get API key from session state first, then environment
    api_key = st.session_state.get("RIOT_API_KEY") or os.getenv("RIOT_API_KEY")
    
    if not api_key:
        st.error("Riot API key not found. Please set your API key in the sidebar.")
        return {}

    try:
        # Base URLs
        base_url = f"https://{region}.api.riotgames.com"
        routing = get_region_routing(region)
        region_url = f"https://{routing}.api.riotgames.com"
        
        # Headers
        headers = {"X-Riot-Token": api_key}
        
        # Get summoner data
        summoner_response = requests.get(
            f"{base_url}/lol/summoner/v4/summoners/by-name/{summoner_name}",
            headers=headers
        )
        summoner_response.raise_for_status()
        summoner_data = summoner_response.json()
        
        # Get ranked data
        ranked_response = requests.get(
            f"{base_url}/lol/league/v4/entries/by-summoner/{summoner_data['id']}",
            headers=headers
        )
        ranked_response.raise_for_status()
        ranked_data = ranked_response.json()
        
        # Get match history
        matches_response = requests.get(
            f"{region_url}/lol/match/v5/matches/by-puuid/{summoner_data['puuid']}/ids",
            params={"start": 0, "count": 5},
            headers=headers
        )
        matches_response.raise_for_status()
        match_ids = matches_response.json()
        
        # Process ranked data
        solo_queue_data = next(
            (queue for queue in ranked_data if queue["queueType"] == "RANKED_SOLO_5x5"),
            None
        )
        
        rank = "Unranked"
        win_rate = "0%"
        if solo_queue_data:
            rank = f"{solo_queue_data['tier']} {solo_queue_data['rank']}"
            total_games = solo_queue_data["wins"] + solo_queue_data["losses"]
            win_rate = f"{(solo_queue_data['wins'] / total_games * 100):.1f}%" if total_games > 0 else "0%"
        
        # Get recent matches data
        recent_matches = []
        for match_id in match_ids:
            match_response = requests.get(
                f"{region_url}/lol/match/v5/matches/{match_id}",
                headers=headers
            )
            match_response.raise_for_status()
            match_data = match_response.json()
            
            # Find player in match
            participant = next(
                p for p in match_data["info"]["participants"]
                if p["puuid"] == summoner_data["puuid"]
            )
            
            recent_matches.append({
                "champion": participant["championName"],
                "result": "Victory" if participant["win"] else "Defeat",
                "kda": f"{participant['kills']}/{participant['deaths']}/{participant['assists']}",
                "cs": participant["totalMinionsKilled"] + participant.get("neutralMinionsKilled", 0)
            })
        
        # Get mastery data for top champions
        mastery_response = requests.get(
            f"{base_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_data['puuid']}/top",
            params={"count": 3},
            headers=headers
        )
        mastery_response.raise_for_status()
        mastery_data = mastery_response.json()
        
        # Get champion data to map IDs to names
        versions_response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        versions_response.raise_for_status()
        latest_version = versions_response.json()[0]
        
        champions_response = requests.get(
            f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
        )
        champions_response.raise_for_status()
        champions_data = champions_response.json()["data"]
        
        # Map champion IDs to names
        champion_id_to_name = {
            int(champ_data["key"]): champ_name 
            for champ_name, champ_data in champions_data.items()
        }
        
        top_champions = [
            champion_id_to_name[mastery["championId"]]
            for mastery in mastery_data
        ]
        
        # Determine main role based on recent matches and champion masteries
        role_counts = {"Top": 0, "Jungle": 0, "Mid": 0, "ADC": 0, "Support": 0}
        champion_roles = get_champion_roles()
        
        for champion in top_champions + [match["champion"] for match in recent_matches]:
            for role, champions in champion_roles.items():
                if champion in champions:
                    role_counts[role] += 1
        
        main_role = max(role_counts.items(), key=lambda x: x[1])[0]
        
        return {
            "name": summoner_data["name"],
            "level": summoner_data["summonerLevel"],
            "rank": rank,
            "winRate": win_rate,
            "mainRole": main_role,
            "topChampions": top_champions,
            "recentMatches": recent_matches
        }
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching summoner data: {str(e)}")
        return {}

def get_champion_icon_url(champion_name):
    """Get champion icon URL from Data Dragon"""
    try:
        # Get latest version
        versions_response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        versions_response.raise_for_status()
        latest_version = versions_response.json()[0]
        
        sanitized_name = champion_name.replace("'", "").replace(" ", "").replace(".", "")
        return f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{sanitized_name}.png"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching champion icon URL: {str(e)}")
        return ""