import os
import random
from pathlib import Path
folder_path = "Database Testing/Uploads"


# Ensure the folder exists
folder = Path(folder_path)
if not folder.exists():
    raise FileNotFoundError(f"Folder '{folder_path}' does not exist")

# Supported image extensions (modify as needed)
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

# Loop through all files in the folder
for file in folder.iterdir():
    if file.suffix.lower() in image_extensions and file.is_file():
        # Generate a random number (adjust range as needed)
        random_number = random.randint(1, 150)
        
        # Create new filename with original extension
        new_filename = f"{random_number}{file.suffix}"
        new_path = file.with_name(new_filename)

        # Ensure the new filename doesn't already exist
        while new_path.exists():
            random_number = random.randint(1, 150)
            new_filename = f"{random_number}{file.suffix}"
            new_path = file.with_name(new_filename)

        # Rename the file
        os.rename(file, new_path)
        print(f"Renamed: {file.name} -> {new_filename}")