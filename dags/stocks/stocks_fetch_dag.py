import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from stock_prices.src.fetch_stocks import fetch_stock_data
from stock_prices.src.producer import StockKafkaProducer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_NAME")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
STOCK_SYMBOLS = os.getenv("STOCK_SYMBOLS").split(", ")


default_args = {
    "owner": "Charlie",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="stock_fetch_to_kafka",
    default_args=default_args,
    description="Fetch stock data to Kafka every 5 minutes",
    schedule="*/5 * * * *",           # every 5 minutes
    start_date=datetime(2026, 2, 1),
    catchup=False,
    tags=["stocks", "kafka"],
    max_active_runs=1,
) as dag:

    def fetch_and_send_to_kafka():
        print("Starting stock fetch task...")

        records = fetch_stock_data(STOCK_SYMBOLS)

        if not records:
            print("No new records fetched → skipping Kafka produce")
            return {"status": "no_data", "count": 0}

        producer = StockKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
        producer.produce_records(KAFKA_TOPIC, records)

        print(f"Successfully sent {len(records)} records to Kafka")
        return {"status": "success", "count": len(records)}

    fetch_task = PythonOperator(
        task_id="fetch_stock_data_and_produce_kafka",
        python_callable=fetch_and_send_to_kafka,
    )

    fetch_task