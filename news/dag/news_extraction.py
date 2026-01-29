import requests
import os
from dotenv import load_dotenv
import logging
import json
from newsapi import NewsApiClient


log = logging.getLogger(__name__)

# importing information from .env file
load_dotenv()

# Define constants for API access
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

NEWS_ENDPOINT_URL = os.getenv('NEWS_ENDPOINT_URL')
NEWS_API_LANGUAGE = os.getenv('NEWS_API_LANGUAGE')
NEWS_API_TOPIC = os.getenv('NEWS_API_TOPIC')

# fetching news data 
newsapi_everything = NewsApiClient(api_key={NEWS_API_KEY})

# fetch everything news 
def fetch_news_everything():
    try:
        log.info(f"Fetching news data - everything")
        ibm_news = newsapi_everything.get_everything(q=NEWS_API_TOPIC,
                                                     language=NEWS_API_LANGUAGE, 
                                                     sort_by="publishedAt"
                                                     )
        log.info(f"News data - everything fetched successfully")
    except Exception as e:
        log.error(f"Error fetching news everything data: {e}")
    return ibm_news

if __name__ == "__main__":
    try:
        news_everything_data = fetch_news_everything()
        log.info("Fetched news everything data successfully.")
        print(json.dumps(news_everything_data, indent=4))
    except Exception as e:
        log.error(f"Error fetching news data: {e}")