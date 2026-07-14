import json
import requests
from datetime import date

# rice stock inventory (monthly total stocks inventory by sector)
url = 'https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2E/CS/0032E4ECNV0.px'

curr_year = date.today().year
years = [str(i) for i in range(2000, curr_year + 1)]

# 2. Define your query payload
payload = {
    "query": [
        {
            "code": "Sector",
            "selection": {"filter": "item", "values": ["0", "1", "2", "3"]},
        },  # Rice total, commercial, household, and nfa stocks
        {
            "code": "Year",
            "selection": {"filter": "item", "values": years},
        },  # Years
        {
            "code": "Month",
            "selection": {
                "filter": "item",
                "values": ["0", "1", "2", "3", "4", "5", "6", "7", 
                           "8", "9", "10", "11"],
            },
        },  # Jan - Dec
    ],
    "response": {"format": "json"},
}

headers = {"Content-Type": "application/json"}

print("[Sending request to API]")

try:
    # 3. Make the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        response.encoding = "utf-8-sig"

        data = response.json()

        # 4. Save the data to a local JSON file
        output_filename = "stocks_inventory_data.json"

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[Successfully retrieved data. Saved locally as: '{output_filename}']")

    else:
        print(f"API Error {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while connecting to the API: {e}")
