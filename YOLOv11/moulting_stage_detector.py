import os
from ultralytics import YOLO
from pathlib import Path

# --- CONFIG ---
IMAGE_FOLDER = "Database Testing/Downloads copy"
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
MODEL_PATH = "YOLOv11/moulting_stage_detector.pt"

# --- Load YOLO model ---
model = YOLO(MODEL_PATH)

def detect_moulting_stage(image_filename):
    if not image_filename.lower().endswith(SUPPORTED_EXTENSIONS):
        raise ValueError("Unsupported file type.")

    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    print(f"Processing: {image_filename}")
    results = model(image_path)
    results[0].show()
    if results[0].boxes.cls.numel() > 0:
        stage = results[0].names[results[0].boxes.cls[0].item()]
    else:
        stage = "No stage detected"

    return stage

if __name__ == "__main__":
    print(detect_moulting_stage("17.jpg"))
# Example usage:
# stage = detect_moulting_stage("87-2016-11-10-T09-27-46.jpeg")
# print("Detected moulting stage:", stage)
