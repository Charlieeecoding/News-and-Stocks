from kafka import KafkaProducer
import os 
from dotenv import load_dotenv
import json
import logging 
from datetime import time
import yfinance as yf

log = logging.getLogger(__name__)

# importing information from .env file
load_dotenv()

# Define constants for Kafka access
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")
KAFKA_STOCK_PRICES_TOPIC = os.getenv("KAFKA_STOCK_PRICES_TOPIC")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stock price data source - yFinance API
stock_name = yf.Ticker(KAFKA_STOCK_PRICES_TOPIC)

def delivery_report(err, msg):
    if err:
        log.error(f"Message delivery failed: {err}")
    else:
        log.info(f"Message delivered: {msg.value().decode('utf-8')} to {msg.topic()}")


# Producing stock price data to Kafka topic
while True:
    try:
        ibm_history = stock_name.history(period="max", interval='1m')
        log.info(f"Fetched data from yFinance for {KAFKA_STOCK_PRICES_TOPIC}")
        for timestamp, row in ibm_history.iterrows():
            stock_data = {
                "Ticker": KAFKA_STOCK_PRICES_TOPIC,
                "Datetime_hkt": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "Open": row['Open'],
                "High": row['High'],
                "Low": row['Low'],
                "Close": row['Close'],
                "Volume": int(row['Volume']), 
                "Dividends": row['Dividends'], 
                "Stock_Splits": row['Stock Splits']
            }
            producer.produce(
                KAFKA_TOPIC_NAME, 
                value=stock_data, 
                callback = delivery_report
                )
            
        time.sleep(60)
        producer.flush()
    except Exception as e:
        log.error(f"Error producing data to Kafka: {e}")
        time.sleep(10)


# ibm_history = stock_name.history(period="max", interval='2m')
# ibm_download = yf.download(tickers=KAFKA_STOCK_PRICES_TOPIC, period="max", interval="2m")

# print(ibm_history)
# print("-----------------------------------------")
# print(ibm_download)