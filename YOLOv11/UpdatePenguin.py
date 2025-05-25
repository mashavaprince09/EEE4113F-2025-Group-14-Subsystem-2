import os
import random
import requests

import os
from ultralytics import YOLO
from pathlib import Path

FOLDER_PATH = "Database Testing/Downloads copy"
BASE_URL = "https://penguinanalytics.onrender.com"

SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
MODEL_PATH = "YOLOv11/moulting_stage_detector.pt"

# --- Load YOLO model ---
model = YOLO(MODEL_PATH)

def detect_moulting_stage(image_filename):
    if not image_filename.lower().endswith(SUPPORTED_EXTENSIONS):
        raise ValueError("Unsupported file type.")

    image_path = os.path.join(FOLDER_PATH, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    print(f"Processing: {image_filename}")
    results = model(image_path)

    if results[0].boxes.cls.numel() > 0:
        stage = results[0].names[results[0].boxes.cls[0].item()]
    else:
        stage = "No stage detected"

    if stage == "Penguin_Not_Moulting":
        return "done"
    else:
        return "moulting"


def main():
    # Step 1: Fetch all penguins and map name -> id
    get_url = f"https://penguinanalytics.onrender.com/penguins?sort_by=name"
    headers = {        "Content-Type": "application/json",
            "accept": "application/json"}

    try:
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()
        penguins = response.json()
        name_to_id = {penguin["name"]: penguin["id"] for penguin in penguins}
    except Exception as e:
        print("Failed to fetch penguins:", e)
        name_to_id = {}

    # Step 2: Loop through files and upload for matching penguins
    for filename in os.listdir(FOLDER_PATH):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            rfid_tag = filename.split(".")[0]
            penguin_name = f"P{rfid_tag}"

            if penguin_name not in name_to_id:
                print(f"Skipping {filename}: No penguin with name '{penguin_name}'")
                continue

            penguin_id = name_to_id[penguin_name]
            upload_url = f"{BASE_URL}/penguins/{penguin_id}/upload-image-log"

            data = {
                "stage": detect_moulting_stage(filename),
                "mass": round(random.uniform(1, 4), 2),
            }

            with open(os.path.join(FOLDER_PATH, filename), "rb") as image_file:
                files = {"image": image_file}
                response = requests.post(upload_url, data=data, files=files)
                print(f"Uploaded image for {penguin_name} → Status: {response.status_code}")
                print("  →", response.text)
        
            os.remove(os.path.join(FOLDER_PATH, filename))
            #print("\n")
            print(f"{filename} will now be deleted from the local directory and DB1")
            

        except Exception as e:
            print(f"Error with file {filename}:", e)
    print("---------------------------------------------------------------------")        