import requests
import os
from dotenv import load_dotenv
import logging
import json

log = logging.getLogger(__name__)

# importing information from .env file
load_dotenv()

# Define constants for API access
NEWS_API_URL = os.getenv('NEWS_API_URL')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# fetching news data 
# def fetch_news(news_url, api_key, query, language):
#     params = {
#         'apiKey': api_key,
#         'q': query,
#         'language': language,
#     }
#     response = requests.get(news_url, params=params)
#     response.raise_for_status()
#     return response.json()

api_url = f"{NEWS_API_URL}{NEWS_API_KEY}&language=en&pageSize=5"

def fetch_news():
    response = requests.get(api_url)
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