# League of Legends Pre-Game Analysis Tool

An AI-powered application that provides comprehensive pre-game analysis for League of Legends players.

## Features

- Team composition analysis with strengths, weaknesses, and win conditions
- Player-specific insights based on champion selection and match history
- Lane matchup analysis with tips and counter strategies
- Beautiful, League of Legends-themed UI with responsive design

## Requirements

- Python 3.9+
- Streamlit
- OpenAI API key

## Getting Started

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Enter your summoner name and region
2. Select champions for both blue and red teams
3. Choose your analysis perspective (Blue or Red team)
4. Click "Generate Analysis" to get comprehensive pre-game insights

## Project Structure

- `app.py`: Main Streamlit application
- `components/`: UI components for different sections
- `utils/`: Utility functions for data and API calls
- `static/`: CSS and static assets

## Note

This is a demonstration application. In a production environment, you would need to:
1. Integrate with the official Riot Games API
2. Implement caching and rate limiting
3. Add user authentication
4. Optimize API calls to reduce costs

## License

MIT