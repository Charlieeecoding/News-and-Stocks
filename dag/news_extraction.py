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
NEWS_CATEGORY = os.getenv('NEWS_CATEGORY')

# fetching news data 
news_api_everything_url = f"{NEWS_API_EVERYTHING_URL}{NEWS_API_KEY}{NEWS_API_LANGUAGE}{NEWS_API_TOPIC}&pageSize=5"
news_api_top_headlines_url = f"{NEWS_API_TOP_HEADLINES_URL}{NEWS_API_KEY}{NEWS_CATEGORY}"

# fetch everything news
def fetch_news_everything():
    try:
        log.info(f"Fetching news data - everything")
        news_everything_response = requests.get(news_api_everything_url)
        news_everything_response.raise_for_status()
        log.info(f"News data - everything fetched successfully")
    except Exception as e:
        log.error(f"Error fetching news everything data: {e}")
    return news_everything_response.json()

# fetch top headlines news
def fetch_news_top_headlines():
    try:
        log.info(f"Fetching news data - top headlines")
        news_top_headlines_response = requests.get(news_api_top_headlines_url)
        news_top_headlines_response.raise_for_status()
        log.info(f"News data - top headlines fetched successfully")
    except Exception as e:
        log.error(f"Error fetching news top headlines data: {e}")
    return news_top_headlines_response.json()



if __name__ == "__main__":
    try:
        # news - everything
        news_everything_data = fetch_news_everything()
        log.info("Fetched news everything data successfully.")
        print(json.dumps(news_everything_data, indent=4))

        # news - top headlines
        # news_top_headlines_data = fetch_news_top_headlines()
        log.info("Fetched news top headlines data successfully.")

    except Exception as e:
        log.error(f"Error fetching news data: {e}")