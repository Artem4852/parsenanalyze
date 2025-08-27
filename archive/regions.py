from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(open("contacts.html"), "html.parser")

# get first 18 elements with classes "Container clearfix grpelem wp-panel"
elements = soup.select(".Thumb.popup_element.clearfix")[:18]

print(len(elements))

region_data = {}

for element in elements:
    # get aria-controls parameter and text content
    print(element.get("aria-controls"), element.get_text(strip=True))
    region_data[element.get("aria-controls")] = element.get_text(strip=True)

print(region_data)

with open("contacts_2.json", "r") as f:
    contacts_data = json.load(f)

for i, group in enumerate(contacts_data):
    if group["id"] in region_data:
        contacts_data[i]["region"] = region_data[group["id"]]
    else:
        contacts_data[i]["region"] = None

with open("contacts_2_with_regions.json", "w") as f:
    json.dump(contacts_data, f, indent=4)