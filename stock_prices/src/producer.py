from confluent_kafka import Producer
import json
from typing import List, Dict, Any
import logging

log = logging.getLogger(__name__)

class StockKafkaProducer:
    def __init__(self, bootstrap_servers: str):
        conf = {
            "bootstrap.servers": bootstrap_servers,
            "client.id": "stock-producer",
            "acks": "all", 
            "retries": 2, # ensure can send the messages after failed 
        }
        self.producer = Producer(conf)

    def delivery_report(self, err, msg):
        if err is not None:
            log.info(f"Delivery failed: {err}")
        else:
            log.info(f"Delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")

    def produce_records(self, topic: str, records: List[Dict[str, Any]]):
        for record in records:
            key = record["symbol"].encode("utf-8")
            value = json.dumps(record).encode("utf-8")

            self.producer.produce(
                topic,
                key=key,
                value=value,
                callback=self.delivery_report,
            )

        # Wait for deliveries
        self.producer.flush(timeout=15)
        log.info(f"Flushed {len(records)} messages to Kafka")