import os
import requests
from dotenv import load_dotenv

def get_summoner_info(summoner_name: str, region: str = "euw1"):
    """
    Fetch summoner information from Riot API
    
    Args:
        summoner_name (str): Name of the summoner to look up
        region (str): Server region (e.g., 'euw1', 'na1', 'kr')
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("RIOT_API_KEY")
    
    if not api_key:
        print("Error: RIOT_API_KEY not found in environment variables")
        print("Please create a .env file with RIOT_API_KEY=your_api_key")
        return None
    
    # Construct the API URL
    base_url = f"https://{region}.api.riotgames.com"
    endpoint = f"/lol/summoner/v4/summoners/by-name/{summoner_name}"
    url = base_url + endpoint
    
    # Set up headers with API key
    headers = {
        "X-Riot-Token": api_key
    }
    
    try:
        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse and return the JSON response
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 403:
            print("Error 403: Forbidden. Check if your API key is valid and has the correct permissions.")
        elif response.status_code == 404:
            print("Error 404: Summoner not found. Check the summoner name and region.")
        else:
            print(f"Status code: {response.status_code}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return None

if __name__ == "__main__":
    # Test with a summoner name (change this to a valid name in your region)
    test_summoner = "9imron"  # Example: Replace with a real summoner name
    region = "euw1"  # Change to your region (euw1, na1, etc.)
    
    print(f"Fetching data for summoner: {test_summoner} in region {region}")
    
    # Get summoner info
    summoner_data = get_summoner_info(test_summoner, region)
    
    # Print the results
    if summoner_data:
        print("\nSummoner Information:")
        print(f"Name: {summoner_data.get('name')}")
        print(f"Level: {summoner_data.get('summonerLevel')}")
        print(f"PUUID: {summoner_data.get('puuid')}")
        print(f"Account ID: {summoner_data.get('accountId')}")
        print(f"Summoner ID: {summoner_data.get('id')}")
        print(f"Profile Icon ID: {summoner_data.get('profileIconId')}")
        print(f"Revision Date: {summoner_data.get('revisionDate')}")
    else:
        print("Failed to retrieve summoner data.")
        print("\nTroubleshooting steps:")
        print("1. Make sure your RIOT_API_KEY is set in the .env file")
        print("2. Verify the summoner name exists in the specified region")
        print("3. Check if your API key has the required permissions")
        print("4. Ensure you're not rate limited (20 requests/1 second, 100 requests/2 minutes)")
