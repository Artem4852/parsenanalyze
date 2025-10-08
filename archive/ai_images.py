from google import genai
from google.genai.types import GenerateContentConfig
import os
import dotenv
import json
import random
import PIL.Image

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

system_instructions = """
You are an AI assistant that helps to extract price information from tables. What we are interested in is to get all commodities being bought as well as the price one is willing to pay. You will get image with a table as an input. You MUST output the result in JSON format as shown in the example below. Don't mention Kernel anywhere. Apart from price info you also have to output terms of the deals and locations, which are in the top left of the table. If any of these two pieces of info is unavailable - write null. Don't leave out any data and output an accurate JSON as it will be processed further automaticaly by another application. Date must be in the format "YYYY-MM-DD", nothing else.

```json
"2022-10-03": {
    "date": "2022-10-03",
    "info": [
      {
        "terms": "DAP",
        "location": "TBT",
        "commodities": {
          "October": {
            "Wheat 2": 210,
            "Wheat 3": 208,
            "Wheat 4": 190,
            "Corn": 190
          },
          "November": {
            "Wheat 2": 212,
            "Wheat 3": 210,
            "Wheat 4": 192,
            "Corn": 192
          },
      },
      {
        "terms": "DAP",
        "location": "Reni",
        "commodities": {
          "October": {
            "Wheat 2": 220,
            "Wheat 3": 220,
          },
          "November": {
            "Wheat 2": 225,
            "Wheat 3": 225,
          }
        }
      }
    ]
  },
```
"""

def get_prices(image_path: str) -> dict:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[PIL.Image.open(image_path)],
        config=GenerateContentConfig(
            system_instruction=system_instructions,
            # max_output_tokens=100,
            temperature=0.1,
            top_p=0.8,
            top_k=40
        )
    )

    data = response.text
    if "```json" in data:
        data = data.split("```json")[1].split("```")[0]
    parsed = json.loads(data)

    # print(response)
    return parsed

def get_ids() -> list:
    with open("kernel.json", "r") as f:
        existing_data = json.load(f)
    
    ids = []
    for _, v in existing_data.items():
        ids.append(v["id"])
    return ids

def append_data(new_data: dict) -> None:
    with open("kernel.json", "r") as f:
        existing_data = json.load(f)
    
    existing_data[list(new_data.keys())[0]+"+"] = new_data[list(new_data.keys())[0]]

    with open("kernel.json", "w") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
  images = os.listdir("images")
  images.sort(key=lambda x: int(x.split(".")[0]))
  ids = get_ids()
  images = [i for i in images if i.split(".")[0] not in ids]
  print(len(images))
  for image_path in images:
    try:
      print(f"Processing {image_path}...")
      prices = get_prices(os.path.join("images", image_path))
      prices[list(prices.keys())[0]]["id"] = image_path.split(".")[0]
      append_data(prices)
    except Exception as e:
      print(f"Error processing {image_path}: {e}")

  # image_path = "images/1001.jpg"
  # prices = get_prices(image_path)
  # print(json.dumps(prices, indent=2, ensure_ascii=False))