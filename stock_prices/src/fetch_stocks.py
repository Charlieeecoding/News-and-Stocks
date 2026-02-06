# import os
# import string
# from dotenv import load_dotenv
# from massive import RESTClient
# from datetime import datetime, timedelta

# load_dotenv()
# stock_api_key = os.getenv("STOCK_API_KEY")

# client = RESTClient(api_key=stock_api_key)


# # def fetch_stock_data():

# ticker = "IBM"
# now_utc = datetime.now()

#     # We fetch the last completed 5-min bar (adjust multiplier/timespan as needed)
#     # Free tier → limited calls/min → fetching one recent bar per symbol is safe
# end_date = now_utc.date()
# start_date = end_date - timedelta(days=3)

# # List Aggregates (Bars)
# aggs = []
# for a in client.list_aggs(
#     ticker=ticker, 
#     multiplier=5, 
#     timespan="minute", 
#     from_=start_date,
#     to=end_date,
#     limit=500000
#     ):
    
#     aggs.append(a)

# print(aggs)





from datetime import datetime, timedelta
from polygon import RESTClient
from typing import List, Dict, Any
import os
import string
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
stock_api_key = os.getenv("STOCK_API_KEY")
STOCK_SYMBOLS = os.getenv("STOCK_SYMBOLS").split(", ")


def fetch_stock_data(symbols: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch the most recent 5-minute bar(s) for each symbol using Massive (Polygon) API.
    Returns list of dicts ready for Kafka.
    """
    client = RESTClient(api_key=stock_api_key)

    results = []
    now_utc = datetime.now()
    end_date = now_utc.date()
    start_date = end_date - timedelta(days=3) 

    for symbol in symbols:
        try:
            aggs = client.get_aggs(
                ticker=symbol,
                multiplier=5,           # 5-minute bars
                timespan="minute",
                from_=start_date,
                to=end_date,
                adjusted=True
            )

            if not aggs:
                print(f"No aggregates returned for {symbol}")
                continue

            # Take the most recent bar
            latest_bar = aggs[-1]
            print(latest_bar)

            record = {
                "time": datetime.fromtimestamp(latest_bar.timestamp / 1000).isoformat() + "Z",  # ms → ISO
                "symbol": symbol,
                "open": float(latest_bar.open),
                "high": float(latest_bar.high),
                "low": float(latest_bar.low),
                "close": float(latest_bar.close),
                "volume": int(latest_bar.volume),
                "fetched_at": now_utc.isoformat() + "Z",
                "vwap": float(latest_bar.vwap) if hasattr(latest_bar, 'vwap') else None, 
                "transactions": int(latest_bar.transactions) if hasattr(latest_bar, 'transactions') else None,
            }

            results.append(record)
            print(f"Fetched {symbol} → close={record['close']} @ {record['time']}")

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    return results


if __name__ == "__main__":
    fetch_stock_data(STOCK_SYMBOLS)