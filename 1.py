import json

with open("data.json", "r") as f:   
    data = json.load(f)

new_data = {}
for entry in data:
    key = list(entry.keys())[0]
    new_data[key] = entry[key]

with open("data_by_date.json", "w") as f:
    json.dump(new_data, f, indent=4)