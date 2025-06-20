# API Reference Documentation
## Complete API Integration Guide

### 📋 Table of Contents
1. [OpenAI API Integration](#openai-api-integration)
2. [Google Gemini API](#google-gemini-api)
3. [Riot Games API](#riot-games-api)
4. [YouTube Data API](#youtube-data-api)
5. [Data Dragon API](#data-dragon-api)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Authentication](#authentication)

---

## 🤖 OpenAI API Integration

### Configuration
```python
import openai
from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo-1106"
        self.default_config = {
            "temperature": 0.7,
            "max_tokens": 2000,
            "response_format": {"type": "json_object"}
        }
```

### Team Analysis Endpoint
```python
def get_team_analysis(self, team_data: dict) -> dict:
    """
    Analyze team composition using OpenAI GPT
    
    Args:
        team_data (dict): {
            "blue": ["Champion1", "Champion2", ...],
            "red": ["Champion1", "Champion2", ...],
            "side": "Blue" | "Red"
        }
    
    Returns:
        dict: {
            "summary": str,
            "strengths": List[str],
            "weaknesses": List[str],
            "win_conditions": List[str],
            "scaling": str,
            "playstyle": str,
            "teamfight": str
        }
    """
    
    system_prompt = """
    You are an expert League of Legends analyst specializing in team compositions.
    Analyze the given team composition and provide insights on:
    1. Team strengths and weaknesses
    2. Win conditions
    3. Overall team scaling
    4. Suggested playstyle
    5. Team fight potential
    
    Format your response as JSON with the following structure:
    {
        "summary": "Brief overall team comp summary",
        "strengths": ["strength1", "strength2", ...],
        "weaknesses": ["weakness1", "weakness2", ...],
        "win_conditions": ["condition1", "condition2", ...],
        "scaling": "early/mid/late game rating out of 10",
        "playstyle": "suggested playstyle description",
        "teamfight": "team fight analysis"
    }
    """
    
    user_prompt = f"""
    Blue Team: {', '.join(team_data['blue'])}
    Red Team: {', '.join(team_data['red'])}
    Team to analyze: {team_data['side']}
    
    Provide detailed team composition analysis.
    """
    
    try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **self.default_config
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        raise OpenAIAPIError(f"Team analysis failed: {str(e)}")
```

### Player Analysis Endpoint
```python
def get_player_analysis(self, player_data: dict) -> dict:
    """
    Analyze player performance and provide recommendations
    
    Args:
        player_data (dict): {
            "summoner_name": str,
            "region": str,
            "champion": str,
            "role": str
        }
    
    Returns:
        dict: {
            "summary": str,
            "strengths": List[str],
            "improvements": List[str],
            "itemization": List[str],
            "performance_metrics": Dict[str, str]
        }
    """
    
    system_prompt = """
    You are an expert League of Legends analyst specializing in player performance.
    Based on the summoner name, champion selection, and match history provided, analyze:
    1. Player's strengths with the selected champion
    2. Areas for improvement
    3. Suggested itemization
    4. Key performance metrics to focus on
    
    Format your response as JSON with the following structure:
    {
        "summary": "Brief player analysis summary",
        "strengths": ["strength1", "strength2", ...],
        "improvements": ["area1", "area2", ...],
        "itemization": ["core item1", "core item2", "situational items", ...],
        "performance_metrics": {"metric1": "description", "metric2": "description", ...}
    }
    """
    
    user_prompt = f"""
    Summoner Name: {player_data['summoner_name']}
    Region: {player_data['region']}
    Champion: {player_data['champion']}
    Role: {player_data['role']}
    
    Provide detailed player analysis for this champion and role.
    """
    
    try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **self.default_config
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        raise OpenAIAPIError(f"Player analysis failed: {str(e)}")
```

### Matchup Analysis Endpoint
```python
def get_matchup_analysis(self, matchup_data: dict) -> dict:
    """
    Analyze lane matchups and provide strategic insights
    
    Args:
        matchup_data (dict): {
            "blue": List[str],  # 5 champions
            "red": List[str],   # 5 champions
            "perspective": "Blue" | "Red"
        }
    
    Returns:
        dict: {
            "top": {
                "favorable": bool,
                "advantage": str,
                "tips": List[str],
                "counter_strategy": str
            },
            "jungle": {...},
            "mid": {...},
            "adc": {...},
            "support": {...}
        }
    """
    
    system_prompt = """
    You are an expert League of Legends analyst specializing in champion matchups.
    Analyze the lane matchups between the given teams and provide insights on:
    1. Favorable and unfavorable matchups
    2. Lane priority
    3. Key matchup-specific tips
    4. Counter-play strategies
    
    Format your response as JSON with the following structure:
    {
        "top": {
            "favorable": true/false,
            "advantage": "Strong/Slight/Even/Slight Disadvantage/Strong Disadvantage",
            "tips": ["tip1", "tip2", ...],
            "counter_strategy": "description"
        },
        "jungle": {...},
        "mid": {...},
        "adc": {...},
        "support": {...}
    }
    """
    
    positions = ["Top", "Jungle", "Mid", "ADC", "Support"]
    user_prompt = f"""
    Blue Team: 
    - Top: {matchup_data['blue'][0]}
    - Jungle: {matchup_data['blue'][1]}
    - Mid: {matchup_data['blue'][2]}
    - ADC: {matchup_data['blue'][3]}
    - Support: {matchup_data['blue'][4]}
    
    Red Team:
    - Top: {matchup_data['red'][0]}
    - Jungle: {matchup_data['red'][1]}
    - Mid: {matchup_data['red'][2]}
    - ADC: {matchup_data['red'][3]}
    - Support: {matchup_data['red'][4]}
    
    Perspective: {matchup_data['perspective']} team
    
    Provide detailed matchup analysis for all lanes.
    """
    
    try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **self.default_config
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        raise OpenAIAPIError(f"Matchup analysis failed: {str(e)}")
```

---

## 🔮 Google Gemini API

### Configuration
```python
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "max_output_tokens": 1500
        }
```

### Patch Analysis Endpoint
```python
def get_patch_analysis(self, patch_version: str = None) -> dict:
    """
    Get AI-powered analysis of the latest LoL patch
    
    Args:
        patch_version (str, optional): Specific patch version to analyze
    
    Returns:
        dict: {
            "version": str,
            "summary": str,
            "champion_changes": List[str],
            "item_changes": List[str],
            "meta_predictions": List[str],
            "trending_picks": {
                "Top": List[str],
                "Jungle": List[str],
                "Mid": List[str],
                "ADC": List[str],
                "Support": List[str]
            },
            "player_tips": List[str]
        }
    """
    
    # Get current patch data if not specified
    if not patch_version:
        patch_data = self._fetch_current_patch_data()
        patch_version = patch_data.get('version', 'Unknown')
    
    prompt = f"""
    Analyze the latest League of Legends patch data and provide insights:
    
    Current Patch: {patch_version}
    Release Date: {datetime.now().strftime('%Y-%m-%d')}
    
    Based on general League of Legends knowledge and typical patch patterns, provide analysis on:
    1. Key meta shifts and champion tier changes
    2. Most impactful champion buffs/nerfs
    3. Item changes affecting gameplay
    4. Predicted trending picks for each role
    5. Strategic recommendations for players
    
    Format your response as JSON with this exact structure:
    {{
        "version": "patch version",
        "summary": "brief 2-3 sentence overview of patch impact",
        "champion_changes": ["change1", "change2", "change3"],
        "item_changes": ["item change1", "item change2"],
        "meta_predictions": ["prediction1", "prediction2", "prediction3"],
        "trending_picks": {{
            "Top": ["champ1", "champ2"],
            "Jungle": ["champ1", "champ2"],
            "Mid": ["champ1", "champ2"],
            "ADC": ["champ1", "champ2"],
            "Support": ["champ1", "champ2"]
        }},
        "player_tips": ["tip1", "tip2", "tip3"]
    }}
    """
    
    try:
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )
        
        return self._parse_json_response(response.text)
        
    except Exception as e:
        raise GeminiAPIError(f"Patch analysis failed: {str(e)}")
```

### Meta Analysis Endpoint
```python
def analyze_team_with_meta(self, team_comp: dict, current_meta: dict) -> dict:
    """
    Analyze team composition considering current meta
    
    Args:
        team_comp (dict): Team composition data
        current_meta (dict): Current meta context
    
    Returns:
        dict: {
            "meta_alignment": str,
            "meta_strengths": List[str],
            "meta_weaknesses": List[str],
            "meta_suggestions": List[str],
            "tier_rating": str
        }
    """
    
    prompt = f"""
    Analyze this League of Legends team composition considering the current meta:
    
    Team Composition:
    - Top: {team_comp.get('blue', [''])[0] or 'Not selected'}
    - Jungle: {team_comp.get('blue', ['', ''])[1] or 'Not selected'}
    - Mid: {team_comp.get('blue', ['', '', ''])[2] or 'Not selected'}
    - ADC: {team_comp.get('blue', ['', '', '', ''])[3] or 'Not selected'}
    - Support: {team_comp.get('blue', ['', '', '', '', ''])[4] or 'Not selected'}
    
    Current Meta Context:
    Trending Picks: {current_meta.get('trending_picks', {})}
    Meta Predictions: {current_meta.get('meta_predictions', [])}
    
    Provide analysis on how this team fits the current meta and suggestions for improvement.
    
    Format as JSON:
    {{
        "meta_alignment": "How well the team fits current meta (1-10)",
        "meta_strengths": ["strength1", "strength2"],
        "meta_weaknesses": ["weakness1", "weakness2"],
        "meta_suggestions": ["suggestion1", "suggestion2"],
        "tier_rating": "S/A/B/C/D tier in current meta"
    }}
    """
    
    try:
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )
        
        return self._parse_json_response(response.text)
        
    except Exception as e:
        raise GeminiAPIError(f"Meta analysis failed: {str(e)}")
```

---

## 🎮 Riot Games API

### Configuration
```python
import requests
from typing import Dict, List, Optional

class RiotAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_urls = {
            "NA1": "https://na1.api.riotgames.com",
            "EUW1": "https://euw1.api.riotgames.com",
            "EUNE1": "https://eune1.api.riotgames.com",
            "KR": "https://kr.api.riotgames.com",
            "BR1": "https://br1.api.riotgames.com",
            "LA1": "https://la1.api.riotgames.com",
            "LA2": "https://la2.api.riotgames.com",
            "OC1": "https://oc1.api.riotgames.com",
            "RU": "https://ru.api.riotgames.com",
            "TR1": "https://tr1.api.riotgames.com",
            "JP1": "https://jp1.api.riotgames.com"
        }
        self.regional_urls = {
            "americas": "https://americas.api.riotgames.com",
            "europe": "https://europe.api.riotgames.com",
            "asia": "https://asia.api.riotgames.com",
            "sea": "https://sea.api.riotgames.com"
        }
        self.headers = {"X-Riot-Token": self.api_key}
```

### Summoner Data Endpoint
```python
def get_summoner_by_name(self, summoner_name: str, region: str) -> dict:
    """
    Get summoner information by name
    
    Args:
        summoner_name (str): Summoner name
        region (str): Region code (e.g., "NA1", "EUW1")
    
    Returns:
        dict: {
            "id": str,
            "accountId": str,
            "puuid": str,
            "name": str,
            "profileIconId": int,
            "revisionDate": int,
            "summonerLevel": int
        }
    
    Raises:
        RiotAPIError: If summoner not found or API error
    """
    
    if region not in self.base_urls:
        raise ValueError(f"Invalid region: {region}")
    
    url = f"{self.base_urls[region]}/lol/summoner/v4/summoners/by-name/{summoner_name}"
    
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise RiotAPIError(f"Summoner '{summoner_name}' not found in {region}")
        elif response.status_code == 403:
            raise RiotAPIError("Invalid API key or access forbidden")
        elif response.status_code == 429:
            raise RiotAPIError("Rate limit exceeded")
        else:
            raise RiotAPIError(f"API error: {e}")
    except requests.exceptions.RequestException as e:
        raise RiotAPIError(f"Network error: {e}")
```

### Ranked Data Endpoint
```python
def get_ranked_stats(self, summoner_id: str, region: str) -> List[dict]:
    """
    Get ranked statistics for a summoner
    
    Args:
        summoner_id (str): Summoner ID
        region (str): Region code
    
    Returns:
        List[dict]: List of ranked queue entries
        [
            {
                "leagueId": str,
                "queueType": str,  # "RANKED_SOLO_5x5", "RANKED_FLEX_SR"
                "tier": str,       # "IRON", "BRONZE", etc.
                "rank": str,       # "I", "II", "III", "IV"
                "summonerId": str,
                "summonerName": str,
                "leaguePoints": int,
                "wins": int,
                "losses": int,
                "veteran": bool,
                "inactive": bool,
                "freshBlood": bool,
                "hotStreak": bool
            }
        ]
    """
    
    url = f"{self.base_urls[region]}/lol/league/v4/entries/by-summoner/{summoner_id}"
    
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        raise RiotAPIError(f"Failed to get ranked stats: {e}")
```

### Match History Endpoint
```python
def get_match_history(self, puuid: str, region: str, count: int = 20) -> List[str]:
    """
    Get match history for a player
    
    Args:
        puuid (str): Player UUID
        region (str): Region code
        count (int): Number of matches to retrieve (max 100)
    
    Returns:
        List[str]: List of match IDs
    """
    
    regional_url = self.get_regional_url(region)
    url = f"{regional_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    
    params = {
        "start": 0,
        "count": min(count, 100)
    }
    
    try:
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        raise RiotAPIError(f"Failed to get match history: {e}")
```

### Match Details Endpoint
```python
def get_match_details(self, match_id: str, region: str) -> dict:
    """
    Get detailed match information
    
    Args:
        match_id (str): Match ID
        region (str): Region code
    
    Returns:
        dict: Detailed match data including participants, timeline, etc.
    """
    
    regional_url = self.get_regional_url(region)
    url = f"{regional_url}/lol/match/v5/matches/{match_id}"
    
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        raise RiotAPIError(f"Failed to get match details: {e}")
```

### Champion Mastery Endpoint
```python
def get_champion_mastery(self, puuid: str, region: str, count: int = 10) -> List[dict]:
    """
    Get champion mastery data for a player
    
    Args:
        puuid (str): Player UUID
        region (str): Region code
        count (int): Number of champions to retrieve
    
    Returns:
        List[dict]: Champion mastery data
        [
            {
                "championId": int,
                "championLevel": int,
                "championPoints": int,
                "lastPlayTime": int,
                "championPointsSinceLastLevel": int,
                "championPointsUntilNextLevel": int,
                "chestGranted": bool,
                "tokensEarned": int,
                "summonerId": str
            }
        ]
    """
    
    url = f"{self.base_urls[region]}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
    
    params = {"count": count}
    
    try:
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        raise RiotAPIError(f"Failed to get champion mastery: {e}")
```

### Helper Methods
```python
def get_regional_url(self, region: str) -> str:
    """Get regional routing URL for a region"""
    region_routes = {
        "NA1": "americas", "BR1": "americas", "LA1": "americas", "LA2": "americas",
        "EUW1": "europe", "EUNE1": "europe", "TR1": "europe", "RU": "europe",
        "KR": "asia", "JP1": "asia",
        "OC1": "sea"
    }
    
    routing = region_routes.get(region, "americas")
    return self.regional_urls[routing]

def process_summoner_data(self, summoner_data: dict, ranked_data: List[dict], 
                         match_history: List[str], mastery_data: List[dict]) -> dict:
    """
    Process and combine summoner data from multiple endpoints
    
    Returns:
        dict: Processed summoner information
        {
            "name": str,
            "level": int,
            "rank": str,
            "winRate": str,
            "mainRole": str,
            "topChampions": List[str],
            "recentMatches": List[dict]
        }
    """
    
    # Process ranked data
    solo_queue = next(
        (queue for queue in ranked_data if queue["queueType"] == "RANKED_SOLO_5x5"),
        None
    )
    
    rank = "Unranked"
    win_rate = "0%"
    
    if solo_queue:
        rank = f"{solo_queue['tier']} {solo_queue['rank']}"
        total_games = solo_queue["wins"] + solo_queue["losses"]
        if total_games > 0:
            win_rate = f"{(solo_queue['wins'] / total_games * 100):.1f}%"
    
    # Process champion mastery
    top_champions = []
    if mastery_data:
        # Get champion names from IDs (requires Data Dragon integration)
        champion_id_to_name = self.get_champion_id_mapping()
        top_champions = [
            champion_id_to_name.get(mastery["championId"], "Unknown")
            for mastery in mastery_data[:3]
        ]
    
    # Process recent matches (simplified)
    recent_matches = []
    for match_id in match_history[:5]:
        try:
            match_details = self.get_match_details(match_id, region)
            # Process match details...
            recent_matches.append(self.process_match_data(match_details, summoner_data["puuid"]))
        except Exception as e:
            continue  # Skip failed matches
    
    return {
        "name": summoner_data["name"],
        "level": summoner_data["summonerLevel"],
        "rank": rank,
        "winRate": win_rate,
        "mainRole": self.determine_main_role(top_champions, recent_matches),
        "topChampions": top_champions,
        "recentMatches": recent_matches
    }
```

---

## 📺 YouTube Data API

### Configuration
```python
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class YouTubeAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
```

### Video Search Endpoint
```python
def search_patch_videos(self, patch_version: str, max_results: int = 6) -> List[dict]:
    """
    Search for League of Legends patch-related videos
    
    Args:
        patch_version (str): Patch version to search for
        max_results (int): Maximum number of results
    
    Returns:
        List[dict]: Video information
        [
            {
                "title": str,
                "channel": str,
                "thumbnail": str,
                "url": str,
                "description": str,
                "published_at": str,
                "view_count": int,
                "duration": str
            }
        ]
    """
    
    search_query = f"League of Legends patch {patch_version} analysis guide"
    published_after = (datetime.now() - timedelta(days=30)).isoformat() + 'Z'
    
    try:
        # Search for videos
        search_request = self.youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            order="relevance",
            maxResults=max_results,
            publishedAfter=published_after,
            regionCode="US",
            relevanceLanguage="en"
        )
        
        search_response = search_request.execute()
        
        # Get video IDs for additional details
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        # Get video statistics and details
        videos_request = self.youtube.videos().list(
            part="statistics,contentDetails",
            id=','.join(video_ids)
        )
        
        videos_response = videos_request.execute()
        
        # Combine search results with video details
        processed_videos = []
        for i, item in enumerate(search_response['items']):
            video_stats = videos_response['items'][i] if i < len(videos_response['items']) else {}
            
            processed_video = {
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'description': item['snippet']['description'][:100] + "...",
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(video_stats.get('statistics', {}).get('viewCount', 0)),
                'duration': video_stats.get('contentDetails', {}).get('duration', 'PT0S')
            }
            
            processed_videos.append(processed_video)
        
        return processed_videos
        
    except Exception as e:
        raise YouTubeAPIError(f"Video search failed: {str(e)}")
```

### Channel Videos Endpoint
```python
def get_channel_videos(self, channel_id: str, max_results: int = 10) -> List[dict]:
    """
    Get recent videos from a specific channel
    
    Args:
        channel_id (str): YouTube channel ID
        max_results (int): Maximum number of videos
    
    Returns:
        List[dict]: Channel video information
    """
    
    try:
        # Get channel's uploads playlist
        channel_request = self.youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        
        channel_response = channel_request.execute()
        
        if not channel_response['items']:
            raise YouTubeAPIError(f"Channel {channel_id} not found")
        
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get videos from uploads playlist
        playlist_request = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        )
        
        playlist_response = playlist_request.execute()
        
        videos = []
        for item in playlist_response['items']:
            video = {
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
                'description': item['snippet']['description'][:100] + "...",
                'published_at': item['snippet']['publishedAt']
            }
            videos.append(video)
        
        return videos
        
    except Exception as e:
        raise YouTubeAPIError(f"Channel videos fetch failed: {str(e)}")
```

---

## 🐉 Data Dragon API

### Configuration
```python
import requests
from typing import Dict, List

class DataDragonClient:
    def __init__(self):
        self.base_url = "https://ddragon.leagueoflegends.com"
        self.cdn_url = "https://ddragon.leagueoflegends.com/cdn"
        self.latest_version = None
```

### Version Management
```python
def get_latest_version(self) -> str:
    """
    Get the latest Data Dragon version
    
    Returns:
        str: Latest version string (e.g., "13.24.1")
    """
    
    if self.latest_version:
        return self.latest_version
    
    try:
        response = requests.get(f"{self.base_url}/api/versions.json")
        response.raise_for_status()
        versions = response.json()
        self.latest_version = versions[0]
        return self.latest_version
        
    except Exception as e:
        raise DataDragonError(f"Failed to get latest version: {e}")
```

### Champion Data Endpoint
```python
def get_champion_data(self, language: str = "en_US") -> dict:
    """
    Get all champion data
    
    Args:
        language (str): Language code (e.g., "en_US", "ko_KR")
    
    Returns:
        dict: Champion data
        {
            "type": "champion",
            "format": "standAloneComplex",
            "version": str,
            "data": {
                "ChampionName": {
                    "version": str,
                    "id": str,
                    "key": str,
                    "name": str,
                    "title": str,
                    "blurb": str,
                    "info": {
                        "attack": int,
                        "defense": int,
                        "magic": int,
                        "difficulty": int
                    },
                    "image": {
                        "full": str,
                        "sprite": str,
                        "group": str,
                        "x": int,
                        "y": int,
                        "w": int,
                        "h": int
                    },
                    "tags": List[str],
                    "partype": str,
                    "stats": dict
                }
            }
        }
    """
    
    version = self.get_latest_version()
    url = f"{self.cdn_url}/{version}/data/{language}/champion.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        raise DataDragonError(f"Failed to get champion data: {e}")
```

### Champion Icon URL
```python
def get_champion_icon_url(self, champion_name: str) -> str:
    """
    Get champion icon URL
    
    Args:
        champion_name (str): Champion name
    
    Returns:
        str: Champion icon URL
    """
    
    version = self.get_latest_version()
    
    # Sanitize champion name for URL
    sanitized_name = champion_name.replace("'", "").replace(" ", "").replace(".", "")
    
    return f"{self.cdn_url}/{version}/img/champion/{sanitized_name}.png"
```

### Item Data Endpoint
```python
def get_item_data(self, language: str = "en_US") -> dict:
    """
    Get all item data
    
    Args:
        language (str): Language code
    
    Returns:
        dict: Item data with similar structure to champion data
    """
    
    version = self.get_latest_version()
    url = f"{self.cdn_url}/{version}/data/{language}/item.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        raise DataDragonError(f"Failed to get item data: {e}")
```

---

## 🚨 Error Handling

### Custom Exception Classes
```python
class APIError(Exception):
    """Base API error class"""
    pass

class OpenAIAPIError(APIError):
    """OpenAI API specific errors"""
    pass

class GeminiAPIError(APIError):
    """Gemini API specific errors"""
    pass

class RiotAPIError(APIError):
    """Riot API specific errors"""
    pass

class YouTubeAPIError(APIError):
    """YouTube API specific errors"""
    pass

class DataDragonError(APIError):
    """Data Dragon API specific errors"""
    pass
```

### Error Handler Decorator
```python
def api_error_handler(fallback_func=None):
    """
    Decorator for handling API errors gracefully
    
    Args:
        fallback_func: Function to call if API fails
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except APIError as e:
                st.error(f"API Error: {str(e)}")
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                return None
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                return None
        return wrapper
    return decorator
```

### Usage Example
```python
@api_error_handler(fallback_func=get_fallback_analysis)
def get_team_analysis_safe(team_data):
    """Safe team analysis with error handling"""
    return openai_client.get_team_analysis(team_data)
```

---

## ⏱️ Rate Limiting

### Rate Limiter Implementation
```python
import time
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self):
        self.api_limits = {
            'riot': {'calls': 100, 'period': 120},  # 100 calls per 2 minutes
            'openai': {'calls': 60, 'period': 60},   # 60 calls per minute
            'gemini': {'calls': 60, 'period': 60},   # 60 calls per minute
            'youtube': {'calls': 100, 'period': 100} # 100 calls per 100 seconds
        }
        self.call_history = defaultdict(deque)
    
    def wait_if_needed(self, api_name: str):
        """Wait if rate limit would be exceeded"""
        if api_name not in self.api_limits:
            return
        
        limit_config = self.api_limits[api_name]
        current_time = time.time()
        call_times = self.call_history[api_name]
        
        # Remove old calls outside the time window
        while call_times and current_time - call_times[0] > limit_config['period']:
            call_times.popleft()
        
        # Check if we're at the limit
        if len(call_times) >= limit_config['calls']:
            # Calculate wait time
            oldest_call = call_times[0]
            wait_time = limit_config['period'] - (current_time - oldest_call)
            
            if wait_time > 0:
                st.info(f"Rate limit reached for {api_name}. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # Record this call
        call_times.append(current_time)
```

---

## 🔐 Authentication

### API Key Validation
```python
def validate_api_key(api_type: str, api_key: str) -> bool:
    """
    Validate API key format
    
    Args:
        api_type (str): Type of API key
        api_key (str): API key to validate
    
    Returns:
        bool: True if valid format
    """
    
    validation_patterns = {
        'openai': r'^sk-[a-zA-Z0-9]{48}$',
        'riot': r'^RGAPI-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$',
        'gemini': r'^[a-zA-Z0-9_-]{39}$',
        'youtube': r'^[a-zA-Z0-9_-]{39}$'
    }
    
    pattern = validation_patterns.get(api_type)
    if not pattern:
        return True  # Unknown type, assume valid
    
    import re
    return bool(re.match(pattern, api_key))
```

### Secure Key Storage
```python
def store_api_key_securely(api_type: str, api_key: str):
    """
    Store API key securely in session state
    
    Args:
        api_type (str): Type of API key
        api_key (str): API key to store
    """
    
    if validate_api_key(api_type, api_key):
        # Store in session state (not persistent)
        st.session_state[f"{api_type.upper()}_API_KEY"] = api_key
        
        # Log key usage (without exposing the key)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:8]
        st.success(f"{api_type.title()} API key stored (hash: {key_hash})")
    else:
        st.error(f"Invalid {api_type} API key format")
```

This comprehensive API reference provides detailed documentation for all external API integrations used in the League of Legends Pre-Game Analysis application. Each endpoint includes proper error handling, rate limiting, and authentication mechanisms to ensure reliable operation