from kafka import KafkaProducer
import os 
from dotenv import load_dotenv
import json
import logging 
from datetime import datetime
import yfinance as yf

log = logging.getLogger(__name__)

# importing information from .env file
load_dotenv()

# Define constants for Kafka access


# Stock price data source - yFinance API for streaming
ibm = yf.Ticker("IBM")

ibm_history = ibm.history(period="max", interval='1m')

print(ibm_history)
