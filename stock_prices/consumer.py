import json
from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
import logging

log = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")
KAFKA_STOCK_GROUP_ID = os.getenv("KAFKA_STOCK_GROUP_ID")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


consumer_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP,
    "group.id": KAFKA_STOCK_GROUP_ID,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
}

consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC_NAME])

# TimescaleDB config
DB_CONFIG = {
    "dbname": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

INSERT_QUERY = """
    INSERT INTO bronze.stock_prices_bronze (time, symbol, open, high, low, close, volume)
    VALUES %s
    ON CONFLICT DO NOTHING;
"""

print("Starting stock consumer...")
log.info("Starting stock consumer...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        try:
            data = json.loads(msg.value().decode("utf-8"))
            # Convert ISO string to proper timestamptz
            record = (
                data["time"],
                data["symbol"],
                data["open"],
                data["high"],
                data["low"],
                data["close"],
                data["volume"],
            )

            execute_values(cur, INSERT_QUERY, [record])
            conn.commit()
            print(f"Inserted stock data: {data['symbol']} @ {data['time']}")

        except Exception as e:
            print(f"Error processing message: {e}")
            conn.rollback()

except KeyboardInterrupt:
    print("Shutting down consumer...")

finally:
    cur.close()
    conn.close()
    consumer.close()