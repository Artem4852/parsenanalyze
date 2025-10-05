import requests
import json
from datetime import datetime, timedelta
import threading

# 01.07.2024 to today
now = datetime.today()
dates = [d for d in (now - timedelta(days=i) for i in range(365*9)) if d >= datetime(2024, 7, 1)]
dates.sort()

dates_loaded = []
for i in range(10):
    with open(f"elevators_{i}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        dates_loaded.extend(data.keys())

dates = [d for d in dates if d.strftime('%Y-%m-%d') not in dates_loaded]
print(f"Dates to load: {len(dates)}")
# exit()

dates_chunks = [dates[i::10] for i in range(10)]
regions = ["Сумська", "Вінницька", "Харківська", "Хмельницька", "Рівненська", "Миколаївська"]

def download_date(date, thread_i):
    print(f"Thread {thread_i}: Downloading data for {date.strftime('%Y-%m-%d')}")
    data_all = {}
    for region in regions:
        url = f"https://pricewidget-api.agroprosperis.com/api/v2/proxy/?query=price_grain/storages/?date={date.strftime('%Y-%m-%d')}%26region={region}"

        r = requests.get(url)
        data = r.json()["data"]

        if len(data) == 0:
            continue

        clean_data = {
            "date": data[0]["date"],
            "elevators": []
        }

        for elevator in data:
            try:
                el = {
                    "name": elevator["name"],
                    "address": elevator["address"],
                    "director": elevator["director"],
                    "phone": elevator["directorPhone"],
                    "traders": elevator["traders"],
                    "crops": []
                }
            except:
                el = {
                    "name": elevator["name"],
                    "address": elevator["address"],
                    "crops": []
                }
            for crop in elevator["crops"]:
                if crop["price"] is not None:
                    el["crops"].append({
                        "name": crop["name"],
                        "price": crop["price"],
                        "terminal": crop["terminal"]
                    })
            clean_data["elevators"].append(el)
        
        data_all[region] = clean_data

    with open(f"elevators_{thread_i}.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)
    
    existing_data[date.strftime('%Y-%m-%d')] = data_all

    with open(f"elevators_{thread_i}.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    
threads = []
for i, chunk in enumerate(dates_chunks):
    t = threading.Thread(target=lambda c, idx: [download_date(d, idx) for d in c], args=(chunk, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()