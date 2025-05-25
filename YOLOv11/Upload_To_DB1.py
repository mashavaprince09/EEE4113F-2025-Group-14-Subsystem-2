import base64
import os
from supabase import create_client, Client
from datetime import datetime
import random
from datetime import timedelta


# --- Supabase Config ---
SUPABASE_URL = "https://urwadaqpwgtltaimtwfu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVyd2FkYXFwd2d0bHRhaW10d2Z1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NTc3NzcsImV4cCI6MjA2MzQzMzc3N30.fzvcF5GoC5g__J4aQOAXblMgbuxZYqIseQmE1G95GEg"
TABLE_NAME = "Penguin_Images"
FOLDER_PATH = "Database Testing/Uploads"
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def parse_filename(image_name):
    """Extract PenguinID from filename and generate LastSeen"""
    # Get filename without extension
    filename_without_ext = os.path.splitext(image_name)[0]
    # Add 'P' prefix to create PenguinID
    penguin_id = f"P{filename_without_ext}"
    
    return penguin_id

def upload_image_to_supabase(image_path):
    image_name = os.path.basename(image_path)
    print(f"Processing: {image_name}")

    try:
        image_base64 = convert_image_to_base64(image_path)
        penguin_id = parse_filename(image_name)

        data = {
            "PenguinID": penguin_id,
            "ImageName": image_name,
            "ImageBase64": image_base64
        }

        # Check if PenguinID already exists
        existing = supabase.table(TABLE_NAME).select("PenguinID").eq("PenguinID", penguin_id).execute()

        if existing.data:
            # Update existing record
            print("A Penguin ID matching this RFID tag has been found in the table")
            
            r = supabase.table(TABLE_NAME).update(data).eq("PenguinID", penguin_id).execute()
            print("The corresponding Penguin ID for RFID: ",image_name,"is",penguin_id)
            print(f"Updated {penguin_id} → Status: 200")
            print(f"PenguinID: {penguin_id}")
            print(f"ImageName: {image_name}")
            print(f"ImageBase64 Preview: {data['ImageBase64'][:70]}...")  # Show first 30 chars

        else:
            # Insert new record
            r = supabase.table(TABLE_NAME).insert(data).execute()
            print(f"Inserted {penguin_id} → Status: 200")
            print(f"PenguinID: {penguin_id}")
            print(f"ImageName: {image_name}")
            print(f"ImageBase64 Preview: {data['ImageBase64'][:70]}...")  # Show first 30 chars

    except Exception as e:
        print(f"Failed to process {image_name}: {e}")

def upload_all_images_in_folder(folder_path):
    image_count = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            image_path = os.path.join(folder_path, filename)
            upload_image_to_supabase(image_path)
            image_count += 1
    return image_count

def main():
    print("All images in",FOLDER_PATH,"are being uploaded to DB1...")
    print("Number of images uploaded:", upload_all_images_in_folder(FOLDER_PATH))
    print("---------------------------------------------------------------------")