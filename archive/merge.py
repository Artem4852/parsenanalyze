import json

for i in range(10):
    with open(f"prices_{i}.json", "r") as f:
        data = json.load(f)
    
    with open("prices.json", "r") as f:
        existing_data = json.load(f)
    
    for date, price_data in data.items():
        existing_data[date] = price_data
    
    with open("prices.json", "w") as f:
        json.dump(existing_data, f, indent=4)