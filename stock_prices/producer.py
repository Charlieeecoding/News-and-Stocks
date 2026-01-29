from kafka import KafkaProducer
import os 
from dotenv import load_dotenv
import json
import logging 
import time
from datetime import datetime
import yfinance as yf

log = logging.getLogger(__name__)

# importing information from .env file
load_dotenv()

# Define constants for Kafka access
