import openai
import os
import streamlit as st
import json

def get_analysis(analysis_type, data):
    """
    Get analysis from OpenAI API
    
    Args:
        analysis_type: Type of analysis (team_analysis, player_analysis, matchup_insights)
        data: Data for analysis
        
    Returns:
        dict: Analysis results
    """
    # Get API key from session state first, then environment
    api_key = st.session_state.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return {
            "error": "OpenAI API key not found. Please set your API key in the sidebar."
        }
    
    # Set the API key
    openai.api_key = api_key
    
    try:
        system_prompt = SYSTEM_PROMPTS.get(analysis_type, SYSTEM_PROMPTS["team_analysis"])
        
        # Prepare user prompt based on analysis type
        if analysis_type == "team_analysis":
            user_prompt = f"""
            Blue Team: {', '.join(data['blue'])}
            Red Team: {', '.join(data['red'])}
            Team to analyze: {data['side']}
            
            Provide detailed team composition analysis.
            """
        elif analysis_type == "player_analysis":
            user_prompt = f"""
            Summoner Name: {data['summoner_name']}
            Region: {data['region']}
            Champion: {data['champion']}
            Role: {data['role']}
            
            Provide detailed player analysis for this champion and role.
            """
        elif analysis_type == "matchup_insights":
            user_prompt = f"""
            Blue Team: 
            - Top: {data['blue'][0]}
            - Jungle: {data['blue'][1]}
            - Mid: {data['blue'][2]}
            - ADC: {data['blue'][3]}
            - Support: {data['blue'][4]}
            
            Red Team:
            - Top: {data['red'][0]}
            - Jungle: {data['red'][1]}
            - Mid: {data['red'][2]}
            - ADC: {data['red'][3]}
            - Support: {data['red'][4]}
            
            Perspective: {data['perspective']} team
            
            Provide detailed matchup analysis for all lanes.
            """
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Parse response
        result = json.loads(response.choices[0].message.content)
        return result
            
    except openai.AuthenticationError:
        return {
            "error": "Invalid OpenAI API key. Please check your API key and try again."
        }
    except openai.RateLimitError:
        return {
            "error": "OpenAI API rate limit exceeded. Please try again later."
        }
    except Exception as e:
        return {
            "error": f"Error generating analysis: {str(e)}"
        }

# System prompts for different analysis types
SYSTEM_PROMPTS = {
    "team_analysis": """
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
    """,
    
    "player_analysis": """
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
    """,
    
    "matchup_insights": """
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
}