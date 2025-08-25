import json

with open('prices_clean.json', 'r') as file:
    data = json.load(file)

clean_data = {}

for key, value in data.items():
    if key != value["date"]:
        continue
    clean_data[key] = {
        "date": value["date"],
        "organizations": {}
    }
    for org_name, org in value["organizations"].items():
        organization = []
        for grain in org:
            if grain["price"] == 0 and grain["priceUsd"] == 0:
                continue
            if grain["price"] == 1 or grain["priceUsd"] == 1:
                continue
            if grain["name"] in [g["name"] for g in organization]:
                continue
            organization.append(grain)
        if organization:
            clean_data[key]["organizations"][org_name] = organization

with open('prices_clean.json', 'w') as file:
    json.dump(clean_data, file, indent=4)