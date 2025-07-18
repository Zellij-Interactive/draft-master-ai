import google.generativeai as genai
import streamlit as st
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any

class GeminiMetaAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_latest_patch_analysis(self) -> Dict[str, Any]:
        """Get AI-powered analysis of the latest LoL patch"""
        try:
            # Get current patch data
            patch_data = self._fetch_current_patch_data()
            
            # Create analysis prompt
            prompt = f"""
            Analyze the latest League of Legends patch data and provide insights:
            
            Current Patch: {patch_data.get('version', 'Unknown')}
            Release Date: {patch_data.get('date', 'Unknown')}
            
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
            
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            st.error(f"Error getting patch analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def analyze_team_with_meta(self, team_comp: Dict[str, List[str]], current_meta: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze team composition considering current meta"""
        try:
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
            
            response = self.model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            st.error(f"Error analyzing team with meta: {str(e)}")
            return {}
    
    def _fetch_current_patch_data(self) -> Dict[str, str]:
        """Fetch current patch version and basic info"""
        try:
            # Get latest version from Data Dragon
            versions_response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
            versions_response.raise_for_status()
            latest_version = versions_response.json()[0]
            
            return {
                "version": latest_version,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        except Exception as e:
            return {
                "version": "14.1",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Gemini"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Fallback analysis when API fails"""
        return {
            "version": "14.1",
            "summary": "Current patch focuses on champion balance and item adjustments to maintain competitive integrity.",
            "champion_changes": [
                "Several ADC champions received minor buffs",
                "Tank supports got defensive improvements",
                "Mid lane assassins saw slight nerfs"
            ],
            "item_changes": [
                "Mythic items received cost adjustments",
                "Support items got utility improvements"
            ],
            "meta_predictions": [
                "Tank supports will see increased play",
                "Scaling ADCs become more viable",
                "Early game junglers remain strong"
            ],
            "trending_picks": {
                "Top": ["Aatrox", "Gnar"],
                "Jungle": ["Graves", "Nidalee"],
                "Mid": ["Azir", "Orianna"],
                "ADC": ["Jinx", "Caitlyn"],
                "Support": ["Thresh", "Nautilus"]
            },
            "player_tips": [
                "Focus on scaling compositions",
                "Prioritize vision control",
                "Practice team fighting"
            ]
        }

class VideoContentFetcher:
    def __init__(self, youtube_api_key: str = None):
        self.youtube_api_key = youtube_api_key
        self.fallback_videos = self._get_fallback_videos()
    
    def get_patch_videos(self, patch_version: str) -> List[Dict[str, str]]:
        """Get patch-related videos"""
        if self.youtube_api_key:
            return self._fetch_youtube_videos(patch_version)
        else:
            return self.fallback_videos
    
    def _fetch_youtube_videos(self, patch_version: str) -> List[Dict[str, str]]:
        """Fetch videos from YouTube API and translate descriptions to English using Gemini if available."""
        try:
            from googleapiclient.discovery import build
            import streamlit as st
            
            youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
            search_query = f"League of Legends patch {patch_version} analysis guide"
            request = youtube.search().list(
                part="snippet",
                q=search_query,
                type="video",
                order="relevance",
                maxResults=6,
                relevanceLanguage="en",
                publishedAfter=(datetime.now() - timedelta(days=30)).isoformat() + 'Z'
            )
            response = request.execute()
            
            # Helper function for translation using Gemini
            def translate_to_english(text, gemini_api_key):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Translate this text to English (output only the translation, no commentary):\n\n{text}"
                    response = model.generate_content(prompt)
                    return response.text.strip()
                except Exception as e:
                    st.warning(f"Translation failed: {str(e)}")
                    return text
            
            gemini_api_key = st.session_state.get("GEMINI_API_KEY") if hasattr(st, 'session_state') else None
            
            videos = []
            for item in response['items']:
                desc = item['snippet']['description'][:100] + "..."
                # Always translate if Gemini key is available
                if gemini_api_key:
                    desc = translate_to_english(desc, gemini_api_key)
                videos.append({
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'description': desc
                })
            
            return videos
            
        except Exception as e:
            st.error(f"Error fetching YouTube videos: {str(e)}")
            return self.fallback_videos
    
    def _get_fallback_videos(self) -> List[Dict[str, str]]:
        """Fallback videos when API is not available"""
        return [
            {
                'title': 'Patch 14.1 Complete Analysis - Meta Changes',
                'channel': 'ProGuides',
                'thumbnail': 'https://images.pexels.com/photos/442576/pexels-photo-442576.jpeg?auto=compress&cs=tinysrgb&w=300',
                'url': 'https://youtube.com',
                'description': 'Complete breakdown of the latest patch changes and meta shifts...'
            },
            {
                'title': 'Best Champions to Climb in Current Patch',
                'channel': 'Skill Capped',
                'thumbnail': 'https://images.pexels.com/photos/1293269/pexels-photo-1293269.jpeg?auto=compress&cs=tinysrgb&w=300',
                'url': 'https://youtube.com',
                'description': 'Discover the strongest champions for ranked climbing...'
            },
            {
                'title': 'Item Build Changes You Need to Know',
                'channel': 'League of Legends',
                'thumbnail': 'https://images.pexels.com/photos/735911/pexels-photo-735911.jpeg?auto=compress&cs=tinysrgb&w=300',
                'url': 'https://youtube.com',
                'description': 'Essential item build updates for the current patch...'
            },
            {
                'title': 'Pro Player Tier List - Current Meta',
                'channel': 'LoL Esports',
                'thumbnail': 'https://images.pexels.com/photos/1040157/pexels-photo-1040157.jpeg?auto=compress&cs=tinysrgb&w=300',
                'url': 'https://youtube.com',
                'description': 'Professional players rank champions in the current meta...'
            },
            {
                'title': 'Jungle Changes Explained',
                'channel': 'Virkayu',
                'thumbnail': 'https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&cs=tinysrgb&w=300',
                'url': 'https://youtube.com',
                'description': 'Understanding the latest jungle changes and their impact...'
            },
            {
                'title': 'Support Meta Guide - What to Play',
                'channel': 'CoreJJ',
                'thumbnail': 'https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg?auto=compress&cs=tinysrgb&w=300',
                'url': 'https://youtube.com',
                'description': 'Support champion recommendations for the current patch...'
            }
        ]