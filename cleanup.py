import json

month_short = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
    "jan": "January",
    "feb": "February",
    "mar": "March",
    "apr": "April",
    "may": "May",
    "jun": "June",
    "jul": "July",
    "aug": "August",
    "sep": "September",
    "oct": "October",
    "nov": "November",
    "dec": "December"
}

month_num = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

with open('kernel_raw.json', 'r') as f:
    data = json.load(f)

clean_data = {}

for k, v in data.items():
    clean_piece = {
        'date': v['date'],
        'id': v['id'],
        'info': []
    }
    print(v['id'])
    for info in v['info']:
        info_piece = {
            'terms': info['terms'],
            'location': info['location'],
            'commodities': {}
        }
        for month_g, commodity in info['commodities'].items():
            for month in month_g.split('/'):
                if "sh" in month.lower():
                    month = month.split(" ")[-1]
                month = month_short.get(month, month)
                if "till" in month.lower():
                    month = month_num[month.split(" ")[-1].split(".")[-1]]

                clean_commodity = {}
                for el, price in commodity.items():
                    if price:
                        if isinstance(price, int):
                            clean_commodity[el.capitalize()] = price
                            continue
                        if price.lower() == "stop":
                            continue
                        price = int(price.split('/')[0].split("(", )[0].replace("*", "").strip())
                        clean_commodity[el.capitalize()] = price
                if clean_commodity == {}:
                    continue
                info_piece['commodities'][month] = clean_commodity
        if info_piece['commodities'] == {}:
            continue
        clean_piece['info'].append(info_piece)
    clean_data[k] = clean_piece

with open('clean_kernel.json', 'w') as f:
    json.dump(clean_data, f, indent=2)