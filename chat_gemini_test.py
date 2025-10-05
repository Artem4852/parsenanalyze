from google import genai
from google.genai.types import GenerateContentConfig
import os
import dotenv
import json
import random
import PIL.Image

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


def get_plate_and_date(image_path):
    image = PIL.Image.open(image_path)

    system_instructions = """
You are an expert at identifying license plates and timestamps from images. You must follow these instructions exactly:

In json format, output the number plate, the date, the time on the image, the bounding box of the truck and the plate.

Don't output anything else, as your output will be parsed by a program. Remember date should be in format `%d.%m.%y` and time should be in format `%H:%M:%S`. If you cannot confidently identify the plate, the truck, or the date or the time, for that specific parameter use `null`. Examples:
`{
    "plate": "CH1094HE",
    "date": "26.10.25",
    "time": "20:03:12",
    "truck_bbox": [x1, y1, x2, y2],
    "plate_bbox": [x1, y1, x2, y2]
}`
`{
    "plate": "null",
    "date": "null",
    "time": "null",
    "truck_bbox": "null",
    "plate_bbox": "null"
}`
"""

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[image],
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
    # print(parsed)
    output = {
        "plate": ''.join(filter(str.isalnum, parsed["plate"])).upper(),
        "date": parsed["date"],
        "time": parsed["time"],
        "truck_bbox": parsed["truck_bbox"],
        "plate_bbox": parsed["plate_bbox"],
        "truck_width": None,
        "plate_width": None,
    }

    if parsed["truck_bbox"] != "null" and parsed["truck_bbox"]:
        output["truck_width"] = parsed["truck_bbox"][2] - parsed["truck_bbox"][0]
    if parsed["plate_bbox"] != "null" and parsed["plate_bbox"]:
        output["plate_width"] = parsed["plate_bbox"][2] - parsed["plate_bbox"][0]
    
    if output["plate"] == "NULL" or len(output["plate"]) != 8 or output["plate_bbox"] == "null" or not output["plate_bbox"] or output["plate_width"] < 80:
    # if parsed["plate"] == "null" or parsed["plate_bbox"] == "null" or output["plate_width"] < 150:
        output["skipped"] = True
    else:
        output["skipped"] = False

    return output

if __name__ == "__main__":
    start = 3380
    num = 10
    only_skipped = True
    for i in range(start, start + num):
        output = get_plate_and_date(f"images/{i}.jpg")

        print(f"Image {i}:")
        if only_skipped:
            print(f"Skipped: {output['skipped']}")
            if output["skipped"]:
                if output["plate"] == "NULL":
                    print("Reason - Plate is null")
                elif len(output["plate"]) != 8:
                    print("Reason - Plate is not 8 characters")
                elif output["plate_width"] < 80:
                    print("Reason - Plate width is less than 80px")
                elif output["plate_bbox"] == "null" or not output["plate_bbox"]:
                    print("Reason - Plate bbox is null")
            print()
            continue
        print(output)
        print(f"Plate: {output['plate']}")
        print(f"Date: {output['date']}")
        print(f"Time: {output['time']}")

        if output['truck_width']:
            print(f"Truck width: {output['truck_width']}px")
        if output['plate_width']:
            print(f"Plate width: {output['plate_width']}px")

        if output["plate_width"] and output["truck_width"]:
            print(f"Plate width / Truck width: {output['plate_width'] / output['truck_width']:.2%}")
        
        print()