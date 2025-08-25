import requests
from datetime import datetime, date, timedelta
import time
import json
import os
import threading

def append_data(date, data, worker_idx):
    if not os.path.exists(f"prices_{worker_idx}.json"):
        with open(f"prices_{worker_idx}.json", "w") as f:
            json.dump({}, f)

    with open(f"prices_{worker_idx}.json", "r") as f:
        existing_data = json.load(f)
    
    existing_data[date.strftime("%Y-%m-%d")] = data

    with open(f"prices_{worker_idx}.json", "w") as f:
        json.dump(existing_data, f, indent=4)

start_date = date(year=2017, month=9, day=4)
dates = [start_date + timedelta(days=i) for i in range(0, 365 * 8)]

with open("prices.json", "r") as f:
    skip_dates = json.load(f).keys()

dates = [d for d in dates if d.strftime("%Y-%m-%d") not in skip_dates]

# split into 10 equal lists
dates_split = [dates[i:i + len(dates) // 10] for i in range(0, len(dates), len(dates) // 10)]

def worker(worker_idx, dates_chunk):
    for date in dates_chunk:
        url = f"https://pricewidget-api.agroprosperis.com/api/v2/proxy/?query=price_grain/terminals/?date={date.strftime('%Y-%m-%d')}"

        response = requests.get(url)
        data = response.json()["data"]

        if not data:
            print(f"No data for {date}")
            continue

        processed = {
            "date": data[0]["date"],
            "organizations": {}
        }
        for organization in data:
            crops = []
            for crop in organization["crops"]:
                crops.append({
                    "name": crop["name"],
                    "price": crop["price"],
                    "priceUsd": crop["priceUsd"],
                })
            processed["organizations"][organization["name"]] = crops

        append_data(date, processed, worker_idx)

        print(f"Processed data for {date}")

        time.sleep(1)

if __name__ == "__main__":
    threads = []
    for i, dates_chunk in enumerate(dates_split):
        thread = threading.Thread(target=worker, args=(i, dates_chunk))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All data processed.")