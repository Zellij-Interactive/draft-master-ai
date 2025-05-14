# OpenAI Utilities

This module (`openai_utils.py`) provides utility functions and predefined prompts to interact with the OpenAI API for generating League of Legends analyses. It is designed to handle different types of analyses, including team composition, player performance, and matchup insights.

---

## Features

### 1. **System Prompts**
The `SYSTEM_PROMPTS` dictionary contains predefined instructions for the OpenAI API to guide the AI's behavior. These prompts ensure consistent and structured responses for the following analysis types:
- **Team Analysis**: Evaluates team compositions, strengths, weaknesses, win conditions, scaling, playstyle, and team fight potential.
- **Player Analysis**: Analyzes a player's performance with a specific champion and role, including strengths, areas for improvement, itemization, and key metrics.
- **Matchup Insights**: Provides insights into lane matchups, including favorable/unfavorable matchups, lane priority, tips, and counter-strategies.

### 2. **Dynamic User Prompts**
The `get_analysis` function dynamically generates user prompts based on the analysis type and input data. This ensures that the AI receives the necessary context to produce accurate and relevant results.

### 3. **Fallback Responses**
For testing purposes, the module includes mock responses for each analysis type when the OpenAI API is unavailable.

---

## How It Works

### **API Key Setup**
The OpenAI API key is retrieved from the `OPENAI_API_KEY` environment variable. Ensure this variable is set before running the application.

### **Analysis Function**
The `get_analysis` function takes two arguments:
- `analysis_type`: The type of analysis to perform (`team_analysis`, `player_analysis`, or `matchup_insights`).
- `data`: The input data required for the analysis (e.g., team compositions, player details, etc.).

### **OpenAI API Call**
The function sends a request to the OpenAI API with the appropriate system and user prompts. The response is parsed and returned as a structured JSON object.

---

## Example Usage

### Team Analysis
```python
data = {
    "blue": ["Champion1", "Champion2", "Champion3", "Champion4", "Champion5"],
    "red": ["Champion6", "Champion7", "Champion8", "Champion9", "Champion10"],
    "side": "blue"
}

result = get_analysis("team_analysis", data)
print(result)
```

### Player Analysis
```python
data = {
    "summoner_name": "Player123",
    "region": "NA",
    "champion": "Ahri",
    "role": "Mid"
}

result = get_analysis("player_analysis", data)
print(result)
```

### Matchup Insights
```python
data = {
    "blue": ["TopBlue", "JungleBlue", "MidBlue", "ADCBlue", "SupportBlue"],
    "red": ["TopRed", "JungleRed", "MidRed", "ADCRed", "SupportRed"],
    "perspective": "blue"
}

result = get_analysis("matchup_insights", data)
print(result)
```

## `get_analysis` Function

The `get_analysis` function is a utility function designed to interact with the OpenAI API. It generates structured analyses for League of Legends data based on the type of analysis requested.

---

### **Function Definition**
```python
def get_analysis(analysis_type, data):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return {"error": "API key not found"}
    
    system_prompt = SYSTEM_PROMPTS.get(analysis_type, SYSTEM_PROMPTS["team_analysis"])
    
    if analysis_type == "team_analysis":
        user_prompt = f"""
        Blue Team: {', '.join(data['blue'])}
        Red Team: {', '.join(data['red'])}
        Team to analyze: {data['side']}
        
        Provide detailed team composition analysis.
        """
```

# OpenAI Utilities

This module (`openai_utils.py`) provides utility functions and predefined prompts to interact with the OpenAI API for generating League of Legends analyses. It is designed to handle different types of analyses, including team composition, player performance, and matchup insights.

---

## Features

### 1. **System Prompts**
The `SYSTEM_PROMPTS` dictionary contains predefined instructions for the OpenAI API to guide the AI's behavior. These prompts ensure consistent and structured responses for the following analysis types:
- **Team Analysis**: Evaluates team compositions, strengths, weaknesses, win conditions, scaling, playstyle, and team fight potential.
- **Player Analysis**: Analyzes a player's performance with a specific champion and role, including strengths, areas for improvement, itemization, and key metrics.
- **Matchup Insights**: Provides insights into lane matchups, including favorable/unfavorable matchups, lane priority, tips, and counter-strategies.

### 2. **Dynamic User Prompts**
The `get_analysis` function dynamically generates user prompts based on the analysis type and input data. This ensures that the AI receives the necessary context to produce accurate and relevant results.

### 3. **Fallback Responses**
For testing purposes, the module includes mock responses for each analysis type when the OpenAI API is unavailable.

---

## How It Works

### **API Key Setup**
The OpenAI API key is retrieved from the `OPENAI_API_KEY` environment variable. Ensure this variable is set before running the application.

### **Analysis Function**
The `get_analysis` function takes two arguments:
- `analysis_type`: The type of analysis to perform (`team_analysis`, `player_analysis`, or `matchup_insights`).
- `data`: The input data required for the analysis (e.g., team compositions, player details, etc.).

### **OpenAI API Call**
The function sends a request to the OpenAI API with the appropriate system and user prompts. The response is parsed and returned as a structured JSON object.

---

## Example Usage

### Team Analysis
```python
data = {
    "blue": ["Champion1", "Champion2", "Champion3", "Champion4", "Champion5"],
    "red": ["Champion6", "Champion7", "Champion8", "Champion9", "Champion10"],
    "side": "blue"
}

result = get_analysis("team_analysis", data)
print(result)
```
### Player Analysis


```python
data = {
    "summoner_name": "Player123",
    "region": "NA",
    "champion": "Ahri",
    "role": "Mid"
}

result = get_analysis("player_analysis", data)
print(result)
```

### Matchup Insights

```python
data = {
    "blue": ["TopBlue", "JungleBlue", "MidBlue", "ADCBlue", "SupportBlue"],
    "red": ["TopRed", "JungleRed", "MidRed", "ADCRed", "SupportRed"],
    "perspective": "blue"
}

result = get_analysis("matchup_insights", data)
print(result)
```