import streamlit as st
from utils.gemini_api import GeminiMetaAnalyzer, VideoContentFetcher
from utils.lol_data import get_champion_icon_url

def render_enhanced_welcome():
    """Render enhanced welcome page with AI-powered patch analysis"""
    
    # Welcome header
    st.markdown("""
    <div class="welcome-container">
        <h2>🎮 Welcome to LoL Pre-Game Analysis</h2>
        <p>Stay ahead of the meta with AI-powered insights and latest patch analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Always show patch section and videos (with fallback data if no API key)
    render_latest_patch_section()
    render_featured_videos_section()
    render_trending_champions_section()
    
    # Original Features Grid
    render_features_grid()

def render_latest_patch_section():
    """Render the latest patch analysis section"""
    st.markdown("### 🔥 Latest Patch Insights")
    
    # Check if Gemini API key is available
    if st.session_state.get("GEMINI_API_KEY"):
        # Get AI-powered patch analysis
        with st.spinner("Analyzing latest patch with AI..."):
            try:
                gemini_analyzer = GeminiMetaAnalyzer(st.session_state.GEMINI_API_KEY)
                patch_analysis = gemini_analyzer.get_latest_patch_analysis()
            except Exception as e:
                st.warning(f"AI analysis unavailable: {str(e)}")
                patch_analysis = get_fallback_patch_analysis()
    else:
        # Show fallback patch analysis
        patch_analysis = get_fallback_patch_analysis()
        st.info("🤖 Add your Gemini API key in the sidebar for AI-powered patch analysis!")
    
    # Display patch analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="patch-card">
            <div class="patch-header">
                <h3>🎯 Patch {patch_analysis.get('version', 'Unknown')} Analysis</h3>
                <span class="patch-badge">Latest</span>
            </div>
            <p class="patch-summary">{patch_analysis.get('summary', 'Analysis not available')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Champion changes
        champion_changes = patch_analysis.get('champion_changes', [])
        if champion_changes:
            st.markdown("**🏆 Key Champion Changes:**")
            for change in champion_changes[:3]:
                st.markdown(f"• {change}")
    
    with col2:
        # Meta predictions
        meta_predictions = patch_analysis.get('meta_predictions', [])
        if meta_predictions:
            st.markdown("**📈 Meta Predictions:**")
            for prediction in meta_predictions[:3]:
                st.markdown(f"• {prediction}")
        
        # Item changes
        item_changes = patch_analysis.get('item_changes', [])
        if item_changes:
            st.markdown("**⚔️ Item Updates:**")
            for change in item_changes[:2]:
                st.markdown(f"• {change}")
    
    # Store patch analysis in session state for other components
    st.session_state.current_patch_analysis = patch_analysis

def render_featured_videos_section():
    """Render featured patch videos section"""
    st.markdown("### 📺 Featured Patch Videos")
    
    try:
        # Get current patch version
        patch_version = st.session_state.get('current_patch_analysis', {}).get('version', '14.1')
        
        # Fetch videos (will use fallback if no YouTube API key)
        video_fetcher = VideoContentFetcher(st.session_state.get("YOUTUBE_API_KEY"))
        videos = video_fetcher.get_patch_videos(patch_version)
        
        # Display videos in grid
        video_cols = st.columns(3)
        for i, video in enumerate(videos[:3]):
            with video_cols[i]:
                st.markdown(f"""
                <div class="video-card">
                    <img src="{video['thumbnail']}" class="video-thumbnail" alt="Video thumbnail">
                    <div class="video-content">
                        <h4 class="video-title">{video['title'][:45]}{'...' if len(video['title']) > 45 else ''}</h4>
                        <p class="video-channel">📺 {video['channel']}</p>
                        <p class="video-description">{video['description'][:60]}...</p>
                        <a href="{video['url']}" target="_blank" class="video-link">Watch Video →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Show more videos button
        if len(videos) > 3:
            with st.expander("🎬 View More Videos"):
                more_video_cols = st.columns(3)
                for i, video in enumerate(videos[3:6]):
                    with more_video_cols[i]:
                        st.markdown(f"""
                        <div class="video-card-small">
                            <h5>{video['title'][:40]}...</h5>
                            <p>📺 {video['channel']}</p>
                            <a href="{video['url']}" target="_blank">Watch →</a>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Show info about YouTube integration
        if not st.session_state.get("YOUTUBE_API_KEY"):
            st.info("📺 Add YouTube API key in sidebar for live video content!")
                        
    except Exception as e:
        st.error(f"Error loading videos: {str(e)}")

def render_trending_champions_section():
    """Render trending champions by role"""
    st.markdown("### 🌟 Trending Champions")
    
    try:
        patch_analysis = st.session_state.get('current_patch_analysis', {})
        trending_picks = patch_analysis.get('trending_picks', {})
        
        if trending_picks:
            # Create tabs for each role
            role_tabs = st.tabs(["🛡️ Top", "🌲 Jungle", "⚡ Mid", "🏹 ADC", "🛡️ Support"])
            
            roles = ["Top", "Jungle", "Mid", "ADC", "Support"]
            
            for i, role in enumerate(roles):
                with role_tabs[i]:
                    champions = trending_picks.get(role, [])
                    if champions:
                        champ_cols = st.columns(len(champions))
                        for j, champion in enumerate(champions):
                            with champ_cols[j]:
                                icon_url = get_champion_icon_url(champion)
                                st.markdown(f"""
                                <div class="trending-champion">
                                    <img src="{icon_url}" class="champion-icon-trending" alt="{champion}">
                                    <p class="champion-name">{champion}</p>
                                    <span class="trending-badge">🔥 Trending</span>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info(f"No trending champions data for {role}")
        else:
            st.info("Trending champions data not available")
            
    except Exception as e:
        st.error(f"Error loading trending champions: {str(e)}")

def render_features_grid():
    """Render the original features grid"""
    st.markdown("### 🎮 Analysis Features")
    
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <h3>Team Composition</h3>
            <p>AI-powered analysis of team synergies, strengths, and win conditions</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">👤</div>
            <h3>Player Insights</h3>
            <p>Personalized performance analysis and champion-specific recommendations</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚔️</div>
            <h3>Matchup Analysis</h3>
            <p>Lane-by-lane breakdown with counter strategies and tips</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔮</div>
            <h3>Meta Insights</h3>
            <p>Stay updated with current patch analysis and trending picks</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_fallback_patch_analysis():
    """Get fallback patch analysis when AI is not available"""
    return {
        "version": "14.1",
        "summary": "Current patch brings significant balance changes to ADC champions and support items, with a focus on improving late-game scaling and team fight dynamics.",
        "champion_changes": [
            "Jinx and Caitlyn received damage buffs to improve late-game carry potential",
            "Tank supports like Nautilus and Leona got defensive improvements",
            "Mid lane assassins saw slight nerfs to reduce early game dominance"
        ],
        "item_changes": [
            "Mythic ADC items received cost reductions for better power spikes",
            "Support items got utility improvements and better gold generation"
        ],
        "meta_predictions": [
            "Scaling ADC compositions will become more viable in ranked play",
            "Tank supports will see increased pick rates in professional matches",
            "Early game jungle pressure remains crucial for map control"
        ],
        "trending_picks": {
            "Top": ["Aatrox", "Gnar", "Camille"],
            "Jungle": ["Graves", "Nidalee", "Kindred"],
            "Mid": ["Azir", "Orianna", "Syndra"],
            "ADC": ["Jinx", "Caitlyn", "Aphelios"],
            "Support": ["Thresh", "Nautilus", "Lulu"]
        },
        "player_tips": [
            "Focus on scaling team compositions for better late-game impact",
            "Prioritize vision control around objectives and jungle entrances",
            "Practice team fighting positioning with new item builds"
        ]
    }