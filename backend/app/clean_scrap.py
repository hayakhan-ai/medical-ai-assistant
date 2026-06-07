import requests
import json
import os

URL = "https://meditour-production-9a75e265b52a.herokuapp.com/user/treatmentsByCategory"

os.makedirs("datasets", exist_ok=True)

response = requests.get(URL)
response.raise_for_status()

api_response = response.json()

# Save raw dataset
with open("datasets/raw_dataset.json", "w", encoding="utf-8") as f:
    json.dump(api_response, f, indent=2, ensure_ascii=False)

print("raw_dataset.json saved")

cleaned = []

# ACTUAL DATA
data = api_response.get("data", [])

for category in data:

    category_name = category.get("categoryName", "").strip().lower()

    treatments = category.get("treatments", [])

    for treatment in treatments:

        cleaned.append({
            "category": category_name,
            "treatment": treatment.get("subCategory", "").strip().lower(),
            "description": treatment.get("description", "").strip(),
            "speciality": category_name
        })

# Remove duplicates
seen = set()
unique_cleaned = []

for item in cleaned:

    key = (
        item["category"],
        item["treatment"]
    )

    if key not in seen:
        seen.add(key)
        unique_cleaned.append(item)

# Save cleaned dataset
with open("datasets/cleaned_dataset.json", "w", encoding="utf-8") as f:
    json.dump(unique_cleaned, f, indent=2, ensure_ascii=False)

print(f"cleaned_dataset.json saved with {len(unique_cleaned)} records")