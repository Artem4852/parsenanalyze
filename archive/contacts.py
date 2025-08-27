from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(open("contacts.html"), "html.parser")

# get first 18 elements with classes "Container clearfix grpelem wp-panel"
elements = soup.select(".Container.clearfix.grpelem")[:18]

print(len(elements))

contacts_data = []

for element in elements:
    group = {
        "id": element.get("id"),
        "people": []
    }
    for child in element.find_all(recursive=False):
        person = {
            "photo_id": child.select_one(".museBGSize").get("id") if child.select_one(".museBGSize") else None,
        }
        p_tags = child.find_all("p")
        print(p_tags)
        for i, tag in enumerate(p_tags):
            text = tag.get_text(strip=True)
            if len(text.split(" ")) == 2:
                person["name"] = text
            elif "@" in text:
                person["email"] = text
            elif "+" in text and "38" in text:
                person["phone"] = text
            elif "+" in text:
                person["phone_alt"] = text
            else:
                person["role"] = text
        group["people"].append(person)
    contacts_data.append(group)

with open("contacts_2.json", "w") as f:
    json.dump(contacts_data, f, indent=4)