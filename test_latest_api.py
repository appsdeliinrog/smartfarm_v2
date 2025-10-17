import requests
import json

# Test the latest prices API
response = requests.get('http://127.0.0.1:8000/api/price-observations/latest/')
data = response.json()

print(f"Total results: {len(data)}")
print("\nCommodities returned:")
commodities = set()
for item in data:
    commodities.add(item['commodity_name'])

for commodity in sorted(commodities):
    count = len([item for item in data if item['commodity_name'] == commodity])
    print(f"- {commodity}: {count} entries")

print(f"\nUnique commodities: {len(commodities)}")
print("Sample entries:")
for i, item in enumerate(data[:5]):
    print(f"{i+1}. {item['commodity_name']} at {item['market_name']} - {item['price']} TZS/kg on {item['observed_date']}")
