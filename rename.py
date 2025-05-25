import os
from pathlib import Path

def rename_images(folder_path, prefix="image_"):
    """
    Rename all images in a folder with sequential numbering.
    
    Args:
        folder_path (str): Path to the folder containing images
        prefix (str): Prefix for the new filenames (default: "image_")
    """
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'}
    
    # Get all image files in the folder
    image_files = [
        f for f in os.listdir(folder_path) 
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    # Sort files to maintain some order
    image_files.sort()
    
    # Rename files with sequential numbering
    for i, filename in enumerate(image_files, start=1):
        old_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()
        new_name = f"{prefix}{i:03d}{ext}"  # 3-digit zero-padded number
        new_path = os.path.join(folder_path, new_name)
        
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

if __name__ == "__main__":
    # Example usage
    folder_path = input("Enter the path to your images folder: ")
    prefix = input("Enter prefix for filenames (default 'image_'): ") or "image_"
    
    if os.path.exists(folder_path):
        rename_images(folder_path, prefix)
        print("Renaming complete!")
    else:
        print("Error: Folder path does not exist")