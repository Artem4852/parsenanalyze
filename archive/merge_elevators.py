import json

elevators_merged = {}
for i in range(10):
    with open(f"elevators_{i}.json", "r", encoding="utf-8") as f:
        elevators_merged.update(json.load(f))

# remove dates that dont align
dates_to_remove = []
for date, data in elevators_merged.items():
    match_found = False
    for region, region_data in data.items():
        if region_data["date"] == date:
            match_found = True
            break
    if match_found: continue
    print(f"Date mismatch for {date} in region {region}: {region_data['date']}")
    dates_to_remove.append(date)

for date in dates_to_remove:
    if date in elevators_merged:
        del elevators_merged[date]

# sort by date
elevators_merged = dict(sorted(elevators_merged.items(), key=lambda x: x[0]))

with open("elevators_merged.json", "w", encoding="utf-8") as f:
    json.dump(elevators_merged, f, ensure_ascii=False, indent=4)