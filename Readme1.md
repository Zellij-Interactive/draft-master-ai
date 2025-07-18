# League of Legends Pre-Game Analysis Tool
## Complete Technical Documentation

### 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Language Model Integration](#language-model-integration)
4. [Implementation Details](#implementation-details)
5. [API Integration](#api-integration)
6. [User Interface](#user-interface)
7. [Data Flow](#data-flow)
8. [Security](#security)
9. [Performance](#performance)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The League of Legends Pre-Game Analysis Tool is a sophisticated AI-powered application that provides comprehensive pre-game insights for League of Legends players. It combines multiple language models, real-time data APIs, and advanced analytics to deliver actionable intelligence before matches begin.

### Key Features
- **AI-Powered Team Analysis**: Deep composition analysis using OpenAI GPT models
- **Real-Time Patch Insights**: Google Gemini integration for current meta analysis
- **Player Performance Analytics**: Riot API integration for personalized insights
- **Matchup Intelligence**: Lane-by-lane strategic recommendations
- **Video Content Integration**: YouTube API for educational content
- **Responsive Design**: Modern UI with League of Legends theming

### Target Users
- **Competitive Players**: Ranked ladder climbers seeking strategic advantages
- **Coaches**: Team analysts requiring detailed composition breakdowns
- **Content Creators**: Streamers and educators needing analytical insights
- **Casual Players**: Anyone wanting to improve their game understanding

---

## 🏗️ Architecture

### System Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Streamlit  │  │    React    │  │   Tailwind  │        │
│  │   Backend   │  │ Components  │  │     CSS     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Components  │  │   Utils     │  │   Session   │        │
│  │   Module    │  │   Module    │  │   State     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   AI/API Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   OpenAI    │  │   Gemini    │  │   Riot API  │        │
│  │    GPT      │  │     AI      │  │   YouTube   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Data Dragon │  │   Session   │  │   Cache     │        │
│  │     API     │  │   Storage   │  │   Layer     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture
```
app.py (Main Application)
├── components/
│   ├── sidebar.py (Input Controls)
│   ├── header.py (Status Display)
│   ├── enhanced_welcome.py (AI-Powered Landing)
│   ├── team_analysis.py (Composition Analysis)
│   ├── player_analysis.py (Individual Insights)
│   └── matchup_insights.py (Lane Analysis)
├── utils/
│   ├── session_state.py (State Management)
│   ├── openai_utils.py (GPT Integration)
│   ├── gemini_api.py (Gemini Integration)
│   └── lol_data.py (Game Data APIs)
└── static/
    └── style.css (UI Styling)
```

---

## 🤖 Language Model Integration

### Multi-Model AI Strategy

The application employs a sophisticated multi-model approach, leveraging different AI systems for specialized tasks:

#### 1. OpenAI GPT-3.5 Turbo (Primary Analysis Engine)
**Purpose**: Deep strategic analysis and tactical recommendations
**Use Cases**:
- Team composition analysis
- Player performance evaluation
- Matchup strategic insights
- Win condition identification

**Implementation**:
```python
def get_analysis(analysis_type, data):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
```

**Prompt Engineering Strategy**:
- **System Prompts**: Define expert persona and output format
- **Structured JSON**: Ensures consistent, parseable responses
- **Context Injection**: Includes current meta and patch information
- **Temperature Control**: Balanced creativity vs. consistency (0.7)

#### 2. Google Gemini 1.5 Flash (Meta Analysis Engine)
**Purpose**: Real-time patch analysis and meta trend prediction
**Use Cases**:
- Current patch impact analysis
- Meta shift predictions
- Champion tier assessments
- Strategic meta recommendations

**Implementation**:
```python
class GeminiMetaAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_latest_patch_analysis(self):
        response = self.model.generate_content(prompt)
        return self._parse_json_response(response.text)
```

**Advantages of Gemini**:
- **Speed**: Faster response times for real-time analysis
- **Context Window**: Larger context for comprehensive patch data
- **Cost Efficiency**: More economical for frequent meta updates
- **Multimodal Capability**: Future integration with patch note images

### Language Model Theory Implementation

#### Prompt Engineering Principles

1. **Role-Based Prompting**
```python
system_prompt = """
You are an expert League of Legends analyst specializing in team compositions.
Analyze the given team composition and provide insights on:
1. Team strengths and weaknesses
2. Win conditions
3. Overall team scaling
4. Suggested playstyle
5. Team fight potential
"""
```

2. **Structured Output Formatting**
```python
response_format = {
    "summary": "Brief overall team comp summary",
    "strengths": ["strength1", "strength2", ...],
    "weaknesses": ["weakness1", "weakness2", ...],
    "win_conditions": ["condition1", "condition2", ...],
    "scaling": "early/mid/late game rating out of 10",
    "playstyle": "suggested playstyle description",
    "teamfight": "team fight analysis"
}
```

3. **Context-Aware Analysis**
- Current patch version injection
- Meta trend consideration
- Historical performance data
- Regional play style differences

#### Advanced AI Techniques

1. **Chain-of-Thought Reasoning**
```python
prompt = f"""
Analyze this team step by step:
1. First, identify each champion's role and strengths
2. Then, evaluate team synergies
3. Consider current meta implications
4. Finally, provide strategic recommendations

Team: {team_composition}
Current Meta: {meta_context}
"""
```

2. **Few-Shot Learning Examples**
```python
examples = """
Example Analysis:
Team: Malphite, Graves, Yasuo, Jinx, Leona
Analysis: This is a teamfight-oriented composition with strong engage...
"""
```

3. **Dynamic Temperature Adjustment**
```python
# Higher temperature for creative strategies
creative_temp = 0.8
# Lower temperature for factual analysis
factual_temp = 0.3
```

---

## 🔧 Implementation Details

### Core Application Structure

#### Main Application (`app.py`)
```python
def main():
    # Initialize session state
    initialize_session_state()
    
    # Render components
    render_sidebar()
    render_header()
    
    # Conditional rendering based on analysis state
    if st.session_state.get("analysis_performed", False):
        # Show analysis tabs
        tabs = st.tabs(["🏠 Home", "🏆 Team Analysis", 
                       "👤 Player Analysis", "⚔️ Matchup Insights"])
    else:
        # Show enhanced welcome page
        render_enhanced_welcome()
```

#### Session State Management (`utils/session_state.py`)
```python
def initialize_session_state():
    """Initialize all session state variables"""
    default_states = {
        "summoner_name": "",
        "region": "EUW1",
        "analysis_performed": False,
        "team_comp": {"blue": [""] * 5, "red": [""] * 5},
        "analysis_results": {},
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "RIOT_API_KEY": os.getenv("RIOT_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
        "current_patch_analysis": {}
    }
    
    for key, default_value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
```

#### Component Architecture

Each component follows a consistent pattern:
```python
def render_component():
    """Render component with error handling and fallbacks"""
    try:
        # Get data from session state
        data = st.session_state.get("component_data", {})
        
        # Validate data
        if not data:
            st.warning("Data not available")
            return
        
        # Render UI with proper styling
        st.markdown("""
        <div class="component-container">
            <!-- Component content -->
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error rendering component: {str(e)}")
```

### Data Processing Pipeline

#### 1. Input Validation
```python
def validate_team_composition(blue_team, red_team):
    """Validate team composition inputs"""
    if "" in blue_team or "" in red_team:
        raise ValueError("All champion selections required")
    
    # Check for duplicate champions
    all_champions = blue_team + red_team
    if len(all_champions) != len(set(all_champions)):
        raise ValueError("Duplicate champions not allowed")
    
    return True
```

#### 2. Data Enrichment
```python
def enrich_analysis_data(team_comp, summoner_data, patch_data):
    """Enrich analysis with contextual data"""
    enriched_data = {
        "team_composition": team_comp,
        "player_context": summoner_data,
        "meta_context": patch_data,
        "timestamp": datetime.now().isoformat(),
        "region": st.session_state.get("region", "EUW1")
    }
    return enriched_data
```

#### 3. Response Processing
```python
def process_ai_response(response_text, analysis_type):
    """Process and validate AI responses"""
    try:
        # Clean response text
        cleaned_text = response_text.strip()
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:-3]
        
        # Parse JSON
        parsed_response = json.loads(cleaned_text)
        
        # Validate structure
        validate_response_structure(parsed_response, analysis_type)
        
        return parsed_response
        
    except json.JSONDecodeError:
        return get_fallback_response(analysis_type)
```

---

## 🔌 API Integration

### Riot Games API Integration

#### Authentication and Rate Limiting
```python
class RiotAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.rate_limiter = RateLimiter()
        self.base_urls = {
            "NA1": "https://na1.api.riotgames.com",
            "EUW1": "https://euw1.api.riotgames.com",
            # ... other regions
        }
    
    def make_request(self, endpoint: str, region: str):
        """Make rate-limited API request"""
        self.rate_limiter.wait_if_needed()
        
        headers = {"X-Riot-Token": self.api_key}
        url = f"{self.base_urls[region]}{endpoint}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
```

#### Data Fetching Strategy
```python
def get_summoner_data(summoner_name: str, region: str):
    """Comprehensive summoner data fetching"""
    try:
        # 1. Get basic summoner info
        summoner_data = api_client.get_summoner(summoner_name, region)
        
        # 2. Get ranked information
        ranked_data = api_client.get_ranked_stats(summoner_data['id'], region)
        
        # 3. Get match history
        match_history = api_client.get_match_history(summoner_data['puuid'], region)
        
        # 4. Get champion mastery
        mastery_data = api_client.get_champion_mastery(summoner_data['puuid'], region)
        
        # 5. Combine and process data
        return process_summoner_data(summoner_data, ranked_data, 
                                   match_history, mastery_data)
        
    except requests.exceptions.RequestException as e:
        handle_api_error(e)
        return get_fallback_summoner_data()
```

### Data Dragon API Integration

#### Champion Data Management
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_champion_list():
    """Load and cache champion data"""
    try:
        # Get latest version
        versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        versions = requests.get(versions_url).json()
        latest_version = versions[0]
        
        # Get champion data
        champions_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
        champions_data = requests.get(champions_url).json()
        
        return process_champion_data(champions_data)
        
    except Exception as e:
        st.error(f"Error loading champion data: {e}")
        return get_fallback_champion_list()
```

### YouTube API Integration

#### Video Content Fetching
```python
class VideoContentFetcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.youtube_service = None
        
        if api_key:
            self.youtube_service = build('youtube', 'v3', 
                                       developerKey=api_key)
    
    def get_patch_videos(self, patch_version: str):
        """Fetch relevant patch videos"""
        if not self.youtube_service:
            return self.get_fallback_videos()
        
        try:
            search_query = f"League of Legends patch {patch_version} analysis"
            
            request = self.youtube_service.search().list(
                part="snippet",
                q=search_query,
                type="video",
                order="relevance",
                maxResults=6,
                publishedAfter=self.get_recent_date()
            )
            
            response = request.execute()
            return self.process_video_results(response)
            
        except Exception as e:
            st.warning(f"YouTube API error: {e}")
            return self.get_fallback_videos()
```

---

## 🎨 User Interface

### Design Philosophy

The UI follows League of Legends' visual design language while maintaining modern web standards:

#### Color Scheme
```css
:root {
    --lol-blue: #0A1428;        /* Primary dark background */
    --lol-blue-light: #0A323C;  /* Secondary background */
    --lol-gold: #C89B3C;        /* Primary accent color */
    --lol-gold-light: #F0E6D2;  /* Secondary accent */
    --lol-accent: #5B5A56;      /* Neutral accent */
}
```

#### Component Design Patterns

1. **Card-Based Layout**
```css
.feature-card {
    background: var(--gradient-primary);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(200, 155, 60, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--lol-gold);
}
```

2. **Interactive Elements**
```css
.champion-icon {
    border-radius: 50%;
    transition: transform 0.3s ease;
}

.champion-icon:hover {
    transform: scale(1.1);
}
```

3. **Responsive Design**
```css
@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: 1fr;
    }
    
    .video-thumbnail {
        height: 120px;
    }
}
```

### Streamlit Customization

#### Custom CSS Integration
```python
# Load custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

#### Component Styling
```python
def render_styled_component(title, content, style_class):
    """Render component with custom styling"""
    st.markdown(f"""
    <div class="{style_class}">
        <h3>{title}</h3>
        <div class="content">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## 📊 Data Flow

### Analysis Pipeline

```
User Input → Validation → Data Enrichment → AI Processing → Response Processing → UI Rendering
```

#### Detailed Flow Diagram
```
┌─────────────────┐
│   User Input    │
│ - Summoner Name │
│ - Team Comp     │
│ - Region        │
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Validation    │
│ - Input Check   │
│ - API Keys      │
│ - Data Format   │
└─────────┬───────┘
          │
┌─────────▼───────┐
│ Data Enrichment │
│ - Riot API      │
│ - Data Dragon   │
│ - Patch Info    │
└─────────┬───────┘
          │
┌─────────▼───────┐
│ AI Processing   │
│ - OpenAI GPT    │
│ - Gemini AI     │
│ - Prompt Eng.   │
└─────────┬───────┘
          │
┌─────────▼───────┐
│ Response Proc.  │
│ - JSON Parse    │
│ - Validation    │
│ - Fallbacks     │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  UI Rendering   │
│ - Components    │
│ - Styling       │
│ - Interactions  │
└─────────────────┘
```

### State Management

#### Session State Flow
```python
# State initialization
initialize_session_state()

# State updates during analysis
def update_analysis_state(analysis_results):
    st.session_state.analysis_results = analysis_results
    st.session_state.analysis_performed = True
    st.session_state.last_analysis_time = datetime.now()

# State persistence across reruns
def persist_user_preferences():
    st.session_state.user_preferences = {
        "region": st.session_state.region,
        "summoner_name": st.session_state.summoner_name,
        "preferred_analysis_depth": "detailed"
    }
```

---

## 🔒 Security

### API Key Management

#### Environment Variables
```python
# Secure API key loading
def load_api_keys():
    """Load API keys from environment with fallbacks"""
    api_keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "RIOT_API_KEY": os.getenv("RIOT_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY")
    }
    
    # Validate key formats
    for key, value in api_keys.items():
        if value and not validate_api_key_format(key, value):
            st.warning(f"Invalid format for {key}")
            api_keys[key] = None
    
    return api_keys
```

#### Session-Based Key Storage
```python
def handle_api_key_input(key_type, user_input):
    """Securely handle user API key input"""
    if user_input:
        # Validate key format
        if validate_api_key_format(key_type, user_input):
            # Store in session (not persistent)
            st.session_state[key_type] = user_input
            st.success(f"{key_type} set for this session!")
        else:
            st.error(f"Invalid {key_type} format")
```

### Data Privacy

#### User Data Handling
```python
def sanitize_user_data(data):
    """Remove sensitive information from user data"""
    sanitized = data.copy()
    
    # Remove sensitive fields
    sensitive_fields = ['email', 'phone', 'real_name']
    for field in sensitive_fields:
        sanitized.pop(field, None)
    
    return sanitized
```

#### Request Logging
```python
def log_api_request(endpoint, success, error=None):
    """Log API requests without sensitive data"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "success": success,
        "error": str(error) if error else None,
        "user_id": hash(st.session_state.get("summoner_name", "anonymous"))
    }
    
    # Log to secure location
    logger.info(json.dumps(log_entry))
```

---

## ⚡ Performance

### Caching Strategy

#### Streamlit Caching
```python
@st.cache_data(ttl=3600)  # 1 hour cache
def get_champion_data():
    """Cache champion data to reduce API calls"""
    return fetch_champion_data_from_api()

@st.cache_data(ttl=1800)  # 30 minute cache
def get_patch_analysis(patch_version):
    """Cache patch analysis to reduce AI API costs"""
    return generate_patch_analysis(patch_version)
```

#### Custom Caching Layer
```python
class AnalysisCache:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 1800  # 30 minutes
    
    def get(self, key):
        """Get cached analysis if still valid"""
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < timedelta(seconds=self.cache_ttl):
                return entry['data']
        return None
    
    def set(self, key, data):
        """Cache analysis result"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
```

### API Rate Limiting

#### Rate Limiter Implementation
```python
class RateLimiter:
    def __init__(self, calls_per_second=1):
        self.calls_per_second = calls_per_second
        self.last_call_time = 0
    
    def wait_if_needed(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        min_interval = 1.0 / self.calls_per_second
        
        if time_since_last_call < min_interval:
            sleep_time = min_interval - time_since_last_call
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
```

### Memory Management

#### Session State Cleanup
```python
def cleanup_old_session_data():
    """Clean up old session data to prevent memory leaks"""
    current_time = datetime.now()
    
    # Remove old analysis results
    if 'analysis_timestamp' in st.session_state:
        analysis_age = current_time - st.session_state.analysis_timestamp
        if analysis_age > timedelta(hours=2):
            st.session_state.analysis_results = {}
            st.session_state.analysis_performed = False
```

---

## 🚀 Deployment

### Local Development Setup

#### Requirements Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

#### Running the Application
```bash
# Start Streamlit server
streamlit run app.py

# Custom configuration
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Production Deployment

#### Docker Configuration
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Environment Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  lol-analysis:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RIOT_API_KEY=${RIOT_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - YOUTUBE_API_KEY=${YOUTUBE_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### Cloud Deployment Options

#### Streamlit Cloud
```toml
# .streamlit/config.toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#C89B3C"
backgroundColor = "#0A1428"
secondaryBackgroundColor = "#0A323C"
textColor = "#F0E6D2"
```

#### Heroku Deployment
```python
# Procfile
web: sh setup.sh && streamlit run app.py
```

```bash
# setup.sh
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### API Key Issues
```python
def diagnose_api_keys():
    """Diagnose API key issues"""
    issues = []
    
    # Check OpenAI key
    if not st.session_state.get("OPENAI_API_KEY"):
        issues.append("OpenAI API key not set")
    elif not st.session_state.OPENAI_API_KEY.startswith("sk-"):
        issues.append("Invalid OpenAI API key format")
    
    # Check Riot API key
    if not st.session_state.get("RIOT_API_KEY"):
        issues.append("Riot API key not set")
    elif len(st.session_state.RIOT_API_KEY) != 42:
        issues.append("Invalid Riot API key length")
    
    return issues
```

#### Rate Limiting Issues
```python
def handle_rate_limit_error(error):
    """Handle API rate limit errors gracefully"""
    if "rate limit" in str(error).lower():
        st.warning("⏳ API rate limit reached. Please wait a moment and try again.")
        st.info("💡 Tip: Consider upgrading your API plan for higher limits.")
        return True
    return False
```

#### Memory Issues
```python
def check_memory_usage():
    """Monitor memory usage and provide warnings"""
    import psutil
    
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 80:
        st.warning("⚠️ High memory usage detected. Consider refreshing the page.")
        
        # Clear non-essential cache
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
```

### Debug Mode

#### Debugging Configuration
```python
def enable_debug_mode():
    """Enable comprehensive debugging"""
    if st.sidebar.checkbox("🐛 Debug Mode"):
        st.sidebar.json(dict(st.session_state))
        
        # Show API response times
        if 'api_response_times' in st.session_state:
            st.sidebar.write("API Response Times:")
            for api, time_taken in st.session_state.api_response_times.items():
                st.sidebar.write(f"- {api}: {time_taken:.2f}s")
```

### Performance Monitoring

#### Response Time Tracking
```python
def track_response_time(func):
    """Decorator to track function response times"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Store response time
        if 'api_response_times' not in st.session_state:
            st.session_state.api_response_times = {}
        
        st.session_state.api_response_times[func.__name__] = end_time - start_time
        return result
    
    return wrapper
```

---

## 📈 Future Enhancements

### Planned Features

1. **Advanced Analytics**
   - Win rate prediction models
   - Champion synergy scoring
   - Meta trend analysis

2. **Real-time Integration**
   - Live game analysis
   - In-game overlay support
   - Real-time coaching suggestions

3. **Machine Learning**
   - Custom model training on user data
   - Personalized recommendations
   - Predictive analytics

4. **Social Features**
   - Team collaboration tools
   - Analysis sharing
   - Community insights

### Technical Improvements

1. **Performance Optimization**
   - Database integration for caching
   - CDN for static assets
   - Async API calls

2. **Scalability**
   - Microservices architecture
   - Load balancing
   - Auto-scaling deployment

3. **Monitoring**
   - Application performance monitoring
   - Error tracking
   - User analytics

---

## 📚 Additional Resources

### API Documentation
- [Riot Games API](https://developer.riotgames.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Google Gemini API](https://ai.google.dev/docs)
- [YouTube Data API](https://developers.google.com/youtube/v3)

### Development Tools
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Best Practices](https://pep8.org/)
- [Docker Documentation](https://docs.docker.com/)

### League of Legends Resources
- [Data Dragon Documentation](https://developer.riotgames.com/docs/lol#data-dragon)
- [Champion.gg](https://champion.gg/) - Meta statistics
- [OP.GG](https://op.gg/) - Player statistics

---

*This documentation is maintained and updated regularly. For the latest version, please check the project repository.*