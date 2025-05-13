import os
import json
import streamlit as st
import requests

# Champion data
@st.cache_data
def load_champion_list():
    """Load list of LoL champions"""
    # In a real app, this would fetch from Riot API
    # For demo purposes, we use a static list
    champions = [
        "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", 
        "Ashe", "Aurelion Sol", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", 
        "Caitlyn", "Camille", "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", 
        "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", 
        "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", 
        "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", 
        "K'Sante", "Kai'Sa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", 
        "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", 
        "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", 
        "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", 
        "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu & Willump", "Olaf", "Orianna", "Ornn", 
        "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "Rek'Sai", "Rell", 
        "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", "Sejuani", 
        "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", 
        "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench", "Taliyah", "Talon", 
        "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", 
        "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex", "Vi", "Viego", "Viktor", 
        "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo", 
        "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
    ]
    return sorted(champions)

@st.cache_data
def get_champion_roles():
    """Get default roles for champions"""
    # This would typically come from an API or database
    # For demo purposes, we use a static mapping
    return {
        "Top": ["Aatrox", "Camille", "Darius", "Fiora", "Gangplank", "Garen", "Gnar", "Gwen", 
                "Illaoi", "Irelia", "Jax", "Jayce", "K'Sante", "Kayle", "Kennen", "Kled",
                "Malphite", "Mordekaiser", "Nasus", "Ornn", "Pantheon", "Poppy", "Renekton",
                "Riven", "Sett", "Shen", "Singed", "Sion", "Teemo", "Tryndamere", "Urgot",
                "Volibear", "Wukong", "Yorick"],
                
        "Jungle": ["Amumu", "Bel'Veth", "Diana", "Ekko", "Elise", "Evelynn", "Fiddlesticks", 
                  "Gragas", "Graves", "Hecarim", "Ivern", "Jarvan IV", "Karthus", "Kayn",
                  "Kha'Zix", "Kindred", "Lee Sin", "Lillia", "Master Yi", "Nidalee", 
                  "Nocturne", "Nunu & Willump", "Olaf", "Rammus", "Rek'Sai", "Rengar",
                  "Sejuani", "Shaco", "Shyvana", "Skarner", "Trundle", "Udyr", "Vi",
                  "Viego", "Warwick", "Xin Zhao", "Zac"],
                  
        "Mid": ["Ahri", "Akali", "Akshan", "Anivia", "Annie", "Aurelion Sol", "Azir", "Cassiopeia",
               "Corki", "Fizz", "Galio", "Heimerdinger", "Kassadin", "Katarina", "LeBlanc",
               "Lissandra", "Lux", "Malzahar", "Neeko", "Orianna", "Qiyana", "Ryze", "Sylas",
               "Syndra", "Taliyah", "Talon", "Twisted Fate", "Veigar", "Vex", "Viktor",
               "Vladimir", "Xerath", "Yasuo", "Yone", "Zed", "Ziggs", "Zoe"],
               
        "ADC": ["Aphelios", "Ashe", "Caitlyn", "Draven", "Ezreal", "Jhin", "Jinx", "Kai'Sa",
               "Kalista", "Kog'Maw", "Lucian", "Miss Fortune", "Nilah", "Samira", "Sivir",
               "Tristana", "Twitch", "Varus", "Vayne", "Xayah", "Zeri"],
               
        "Support": ["Alistar", "Bard", "Blitzcrank", "Brand", "Braum", "Janna", "Karma", "Leona",
                   "Lulu", "Morgana", "Nami", "Nautilus", "Pyke", "Rakan", "Rell", "Renata Glasc",
                   "Senna", "Seraphine", "Sona", "Soraka", "Tahm Kench", "Taric", "Thresh",
                   "Yuumi", "Zilean", "Zyra"]
    }

def get_regions():
    """Get list of LoL regions"""
    return ["NA", "EUW", "EUNE", "KR", "BR", "LAN", "LAS", "OCE", "RU", "TR", "JP"]

def get_summoner_data(summoner_name, region):
    """
    Get summoner data from Riot API
    In a real app, this would make API calls to Riot
    For demo purposes, we return mock data
    """
    # This would typically come from Riot API
    # For demo, we use mock data
    return {
        "name": summoner_name,
        "level": 150,
        "rank": "Gold II",
        "winRate": "53%",
        "mainRole": "Mid",
        "topChampions": ["Ahri", "Zed", "Syndra"],
        "recentMatches": [
            {"champion": "Ahri", "result": "Victory", "kda": "8/2/10", "cs": 187},
            {"champion": "Zed", "result": "Defeat", "kda": "4/5/3", "cs": 165},
            {"champion": "Syndra", "result": "Victory", "kda": "6/1/7", "cs": 201},
            {"champion": "Ahri", "result": "Victory", "kda": "10/4/9", "cs": 192},
            {"champion": "Viktor", "result": "Defeat", "kda": "2/6/3", "cs": 154}
        ]
    }

def get_champion_icon_url(champion_name):
    """Get champion icon URL"""
    # In a real app, this would use Riot's Data Dragon
    # For demo, we use a placeholder pattern
    sanitized_name = champion_name.replace("'", "").replace(" ", "").replace(".", "")
    return f"https://ddragon.leagueoflegends.com/cdn/13.24.1/img/champion/{sanitized_name}.png"