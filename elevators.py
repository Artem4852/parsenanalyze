import requests
import json
from datetime import datetime

date = datetime(2025, 8, 26)
regions = ["Сумська", "Вінницька", "Харківська", "Хмельницька", "Рівненська", "Миколаївська"]

data_all = {}
for region in regions:
    url = f"https://pricewidget-api.agroprosperis.com/api/v2/proxy/?query=price_grain/storages/?date={date.strftime('%Y-%m-%d')}%26region={region}"

    r = requests.get(url)
    data = r.json()["data"]

    print(f"Region: {region}, Elevators: {len(data)}")

    if len(data) == 0:
        continue

    clean_data = {
        "date": data[0]["date"],
        "elevators": []
    }

    for elevator in data:
        el = {
            "name": elevator["name"],
            "address": elevator["address"],
            "director": elevator["director"],
            "phone": elevator["directorPhone"],
            "traders": elevator["traders"],
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

with open("elevators.json", "w", encoding="utf-8") as f:
    json.dump(data_all, f, ensure_ascii=False, indent=4)