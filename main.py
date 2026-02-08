import argparse
import os
import sys
import time
import subprocess
from typing import List

from dotenv import load_dotenv

# Load env
load_dotenv()


def fetch_once(symbols: List[str]):
    from stock_prices.src.fetch_stocks import fetch_stock_data

    print(f"Fetching stocks for: {symbols}")
    records = fetch_stock_data(symbols)
    print(f"Fetched {len(records)} records")
    return records


def produce_once(records: List[dict]):
    if not records:
        print("No records to produce")
        return

    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    topic = os.getenv("KAFKA_TOPIC_NAME")

    if not bootstrap or not topic:
        print("KAFKA_BOOTSTRAP_SERVERS or KAFKA_TOPIC_NAME not set in env")
        return

    from stock_prices.src.producer import StockKafkaProducer

    producer = StockKafkaProducer(bootstrap_servers=bootstrap)
    producer.produce_records(topic, records)


def run_consumer():
    # Run the existing consumer script as a subprocess so it runs in its own process
    script = os.path.join(os.path.dirname(__file__), "stock_prices", "consumer.py")
    if not os.path.exists(script):
        print(f"Consumer script not found at {script}")
        return 1

    print(f"Starting consumer subprocess: {script}")
    proc = subprocess.Popen([sys.executable, "-u", script], stdout=sys.stdout, stderr=sys.stderr)
    return proc


def e2e_loop(symbols: List[str], interval: int):
    consumer_proc = run_consumer()
    try:
        while True:
            records = fetch_once(symbols)
            produce_once(records)
            print(f"Sleeping {interval} seconds before next run...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopping e2e run (KeyboardInterrupt)")
    finally:
        if consumer_proc and getattr(consumer_proc, "poll", None) is not None:
            print("Terminating consumer subprocess...")
            consumer_proc.terminate()
            try:
                consumer_proc.wait(timeout=5)
            except Exception:
                consumer_proc.kill()


def main():
    parser = argparse.ArgumentParser(description="Run repo components locally for testing")
    sub = parser.add_subparsers(dest="cmd")

    parser_fetch = sub.add_parser("fetch", help="Fetch stock data once and print")
    parser_fetch.add_argument("--symbols", help="Comma separated symbols override env", default=None)

    parser_produce = sub.add_parser("produce", help="Fetch then produce to Kafka once")
    parser_produce.add_argument("--symbols", help="Comma separated symbols override env", default=None)

    parser_consume = sub.add_parser("consume", help="Run the consumer script (blocks)")

    parser_e2e = sub.add_parser("e2e", help="Run consumer and periodically produce every interval seconds")
    parser_e2e.add_argument("--interval", type=int, default=300, help="Interval seconds between produces")
    parser_e2e.add_argument("--symbols", help="Comma separated symbols override env", default=None)

    args = parser.parse_args()

    # Determine symbols
    if args.cmd in ("fetch", "produce", "e2e"):
        if getattr(args, "symbols", None):
            symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
        else:
            env_syms = os.getenv("STOCK_SYMBOLS")
            if not env_syms:
                print("STOCK_SYMBOLS not set in .env and no --symbols provided")
                sys.exit(1)
            symbols = [s.strip() for s in env_syms.split(",") if s.strip()]

    if args.cmd == "fetch":
        fetch_once(symbols)
    elif args.cmd == "produce":
        records = fetch_once(symbols)
        produce_once(records)
    elif args.cmd == "consume":
        proc = run_consumer()
        if isinstance(proc, int):
            sys.exit(proc)
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
    elif args.cmd == "e2e":
        e2e_loop(symbols, args.interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
