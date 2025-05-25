import os
import random
import requests

# API endpoints
base_url = "https://penguinanalytics.onrender.com"
create_url = f"{base_url}/penguins/"
get_url = f"https://penguinanalytics.onrender.com/penguins?sort_by=name"  # assuming this returns a list of penguins

FOLDER_PATH = "Database Testing/Downloads copy"

def createPenguin():
    # Headers for JSON requests
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    # Step 1: Get existing penguin names
    try:
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()
        existing_penguins = response.json()
        existing_names = {penguin["name"] for penguin in existing_penguins}
    except Exception as e:
        print("Failed to fetch existing penguins:", e)
        existing_names = set()  # fallback to allow script to run

    # Step 2: Process image files
    for filename in os.listdir(FOLDER_PATH):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            rfid_tag = filename.split(".")[0]
            name = f"P{rfid_tag}"

            if name in existing_names:
                print(f"Skipped: Penguin with name '{name}' already exists in DB2 so no need to create a new record")
                continue

            payload = {
                "rfid_tag": rfid_tag,
                "name": name,
                "mass": round(random.uniform(1, 3.5), 2),
                "status": "not started"
            }

            # Create penguin
            response = requests.post(create_url, json=payload, headers=headers)
            print(f"Creating a new record with Name: {name} from {filename} in DB2")
            print("  → Status:", response.status_code)
            print("  → Response:", response.text)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

def main():
    createPenguin()
    print("---------------------------------------------------------------------") 