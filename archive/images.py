import cssutils
import json

sheet = cssutils.parseFile("map-distr.css")

def get_image_url(photo_id):
    target_id = f"#{photo_id}"
    matching_rules = []

    # Iterate over rules
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            for selector in rule.selectorList:
                if target_id in selector.selectorText:
                    matching_rules.append(rule.style.cssText)

    # get background url
    for style in matching_rules:
        styles = style.split(";")
        for s in styles:
            if "background" in s:
                bg_value = s.split(":")[1].strip()
                if "url(" in bg_value:
                    url_part = bg_value.split("url(")[1].split(")")[0]
                    image_url = url_part.strip('"').strip("'").replace("../", "https://agroprosperis.com/")
                    return image_url
    return None

with open("contacts_2_with_regions.json", "r") as f:
    contacts_data = json.load(f)

for group_n, group in enumerate(contacts_data):
    for person_n, person in enumerate(group["people"]):
        photo_id = person["photo_id"]
        image_url = get_image_url(photo_id)
        contacts_data[group_n]["people"][person_n]["image"] = image_url

with open("contacts_2_with_regions_and_images.json", "w") as f:
    json.dump(contacts_data, f, ensure_ascii=False, indent=2)