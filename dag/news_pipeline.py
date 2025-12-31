import requests
import os
from dotenv import load_dotenv
import logging
import json

log = logging.getLogger(__name__)

# importing information from .env file
load_dotenv()

# Define constants for API access
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

NEWS_API_EVERYTHING_URL = os.getenv('NEWS_API_EVERYTHING_URL')
NEWS_API_LANGUAGE = os.getenv('NEWS_API_LANGUAGE')
NEWS_API_TOPIC = os.getenv('NEWS_API_TOPIC')

NEWS_API_TOP_HEADLINES_URL = os.getenv('NEWS_API_TOP_HEADLINES_URL')


# fetching news data 
news_api_everything_url = f"{NEWS_API_EVERYTHING_URL}{NEWS_API_KEY}{NEWS_API_LANGUAGE}{NEWS_API_TOPIC}&pageSize=5"
news_api_top_headlines_url = f"{NEWS_API_TOP_HEADLINES_URL}{NEWS_API_KEY}&pageSize=5&category=technology&country=us"

def fetch_news():
    response = requests.get(news_api_everything_url)
    response.raise_for_status()
    return response.json()

# fetch_news({NEWS_API_URL}, {NEWS_API_KEY}, 'IBM', 'en')

if __name__ == "__main__":
    try:
        news_data = fetch_news()
        log.info("Fetched news data successfully.")
        pretty = json.dumps(news_data, indent=2)
        print(pretty)
        log.info(pretty)
    except Exception as e:
        log.error(f"Error fetching news data: {e}")