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
You are an AI assistant that helps to extract price information from text blocks. What we are interested in is to get all commodities each company is buying as well as the price they are willing to pay. You will get text block as an input. You MUST output the result in JSON format as shown in the example below. Don't mention Kernel unless it is in the name of specific company/institution. For example, if company is "Бандурський ОЕЗ", don't write anything like "Kernel | Бандурський ОЕЗ" or "Kernel Бандурський ОЕЗ"

```json
"2017-09-04": {
    "date": "2017-09-04",
    "organizations": {
      "Транс-Сервіс ТОВ": [
        {
          "name": "Соя",
          "price": 10400,
          "priceUsd": 0
        },
        {
          "name": "Пшениця 2 клас",
          "price": 5000,
          "priceUsd": 165
        },
        {
          "name": "Пшениця 3 клас",
          "price": 4650,
          "priceUsd": 155
        }
      ],
      "Весело-Кутський КХП ВАТ (порт)": [
        {
          "name": "Ячмінь 3 клас",
          "price": 4500,
          "priceUsd": 145
        },
        {
          "name": "Пшениця 2 клас",
          "price": 4950,
          "priceUsd": 163
        },
        {
          "name": "Пшениця 3 клас",
          "price": 4600,
          "priceUsd": 153
        },
        {
          "name": "Пшениця 5 клас",
          "price": 4400,
          "priceUsd": 146
        },
        {
          "name": "Пшениця 6 клас",
          "price": 4350,
          "priceUsd": 144
        }
      ],
      "Тіс-Зерно ТОВ": [
        {
          "name": "Ячмінь 3 клас",
          "price": 4850,
          "priceUsd": 158
        },
        {
          "name": "Пшениця 2 клас",
          "price": 5000,
          "priceUsd": 165
        },
        {
          "name": "Пшениця 3 клас",
          "price": 4650,
          "priceUsd": 155
        },
        {
          "name": "Пшениця 6 клас",
          "price": 4440,
          "priceUsd": 148
        },
        {
          "name": "Ріпак 1 клас",
          "price": 12800,
          "priceUsd": 420
        }
      ],
      "МСП Ніка-Тера ТОВ": [
        {
          "name": "Пшениця 3 клас",
          "price": 4675,
          "priceUsd": 156
        }
      ]
    }
  },
```
"""

def get_prices(text_block: str) -> dict:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[text_block],
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

    print(response)
    return parsed


if __name__ == "__main__":
  text_block = """
🔰 KERNEL | Цінова політика
Станом на 02.10.2025

🛳️ ТБТ (Чорноморськ):
• Пшениця 2/3/4 кл — 10 200 / 10 200 / 9 600 грн/т 
• Ячмінь — 10 000 грн/т
• Кукурудза - 9400 грн/т

🌻 Соняшник (у перерахунку на 48 олійність)

🏭 Бандурський ОЕЗ —  
26 700 грн/т
🏭 УЧІ — 27 000 грн/т
🏭 Старокостянтинівський ОЕЗ — 26 000 грн/т
🏭 Кропивницький ОЕЗ — 
26 600 грн/т
💰Премія / Дисконт: +350 / -400 грн/т

🌻Соняшник високоолеїновий (у перерахунку на 48 олійність)

🏭Придніпровський ОЕЗ - 
31 200 грн/т
💰Премія / Дисконт: +350 / -400 грн/т

🌱Соя 
(Білок не менше 37%, олійність не менше 21%)

 🏭Старокостянтинівський ОЕЗ —  16 500 грн/т

💬 Всі пропозиції розглядаємо індивідуально 

Менеджер із закупівель
👨🏼‍💻 Синьківський Андрій
Телефони для зв’язку:
📞 +38 (050) 401 56 57
📞 +38 (098) 580 78 79
"""
  prices = get_prices(text_block)
  print(json.dumps(prices, indent=2, ensure_ascii=False))