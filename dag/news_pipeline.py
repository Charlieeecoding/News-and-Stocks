import requests
import os
from dotenv import load_dotenv
import logging
import json
import psycopg2

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
news_api_top_headlines_url = f"{NEWS_API_TOP_HEADLINES_URL}{NEWS_API_KEY}{NEWS_CATEGORY}&pageSize=5"

# fetch everything news
def fetch_news_everything():
    response = requests.get(news_api_everything_url)
    response.raise_for_status()
    return response.json()

# fetch top headlines news
def fetch_news_top_headlines():
    response = requests.get(news_api_top_headlines_url)
    response.raise_for_status()
    return response.json()

# connecting to Postgres database and save data
def connect_to_postgres():
    print("Connecting to PostgreSQL database...")
    try:
        connection = psycopg2.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB')
        )

        print("Connection successful.")
        return connection
    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None, None

if __name__ == "__main__":
    try:
        # news_everything_data = fetch_news_everything()
        # log.info("Fetched news everything data successfully.")
        # pretty = json.dumps(news_everything_data, indent=2)
        # print(pretty)
        # log.info(pretty)

        print("Connecting to Postgres db")
        connect_to_postgres()
    except Exception as e:
        log.error(f"Error fetching news data: {e}")