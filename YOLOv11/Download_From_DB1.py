import base64
import os
from supabase import create_client, Client

# --- Supabase Config ---
SUPABASE_URL = "https://urwadaqpwgtltaimtwfu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVyd2FkYXFwd2d0bHRhaW10d2Z1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NTc3NzcsImV4cCI6MjA2MzQzMzc3N30.fzvcF5GoC5g__J4aQOAXblMgbuxZYqIseQmE1G95GEg"
TABLE_NAME = "Penguin_Images"
OUTPUT_FOLDER = "Database Testing\\Downloads copy"

def download_all_images(output_folder=OUTPUT_FOLDER):
    image_count = 0
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    try:
        print("Fetching all records from Supabase...")
        response = supabase.table(TABLE_NAME).select("*").execute()
        records = response.data

        if not records:
            print("No records found in the table.")
            return

        os.makedirs(output_folder, exist_ok=True)

        for record in records:
            image_name = record["ImageName"]
            image_base64 = record["ImageBase64"]
            output_path = os.path.join(output_folder, image_name)

            # Save image
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(image_base64))
            print(f"Saved '{image_name}' to '{OUTPUT_FOLDER}'")
            image_count += 1

            # Delete image record from database
            try:
                delete_response = supabase.table(TABLE_NAME).delete().eq("ImageName", image_name).execute()
                #print(delete_response)
                #if delete_response[0]['ImageName'] == image_name:
                print(f"Deleted record for '{image_name}' from the database.")
                #else:
                    #print(f"No record deleted for '{image_name}'.")

            except Exception as delete_error:
                print(f"Error deleting record for '{image_name}':", delete_error)

        print("All images processed and deleted successfully.")
        return image_count

    except Exception as e:
        print("Error retrieving or deleting images:", e)

# --- Run ---
def main():
    print("All images in DB1 are being downloaded to", OUTPUT_FOLDER)
    print("Number of images downloaded:", download_all_images())
    print("---------------------------------------------------------------------")
