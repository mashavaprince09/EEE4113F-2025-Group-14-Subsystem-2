import tkinter as tk
from tkinter import filedialog
import os
import shutil
import glob
from ultralytics import YOLO

def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    return file_path

def train_model():
    # Load a pretrained YOLO11n model
    model = YOLO("YOLOv11/yolo11n.pt")

    # Train the model on the COCO8 dataset for 100 epochs
    train_results = model.train(
        data="YOLOv11/config.yaml",   # dataset config
        epochs=50,
        imgsz=768,
        device=0,
        batch=8,
        workers=4,
        # Hyperparameter overrides:
        lr0=0.01,                     # base learning rate
        lrf=0.2,                      # lr final = lr0 * lrf
        momentum=0.937,
        weight_decay=0.0005,                 # weight for classification loss on class0
        kobj=1.0,                   # weight for objectness loss
        scale=0.5,
        mosaic=1.0,
        #multi_scale=True
        cls=3.0,  # Increased from 2.0 for stronger class weighting
                # Enhanced augmentations
        hsv_h=0.02,  # Reduced from 0.03
        hsv_s=0.8,   # Reduced from 0.9
        hsv_v=0.5,   # Reduced from 0.7
        degrees=15.0, # Reduced from 25.0
        translate=0.1, # Reduced from 0.2
        shear=5.0,    # Reduced from 10.0
        perspective=0.0005, # Reduced from 0.001
        mixup=0.5,    # Reduced from 0.7
        copy_paste=0.2, # Reduced from 0.3
                # Training optimizations
        cos_lr=True,
        amp=True,        
    )

    # Find the latest training directory
    train_dirs = glob.glob("runs/detect/train*")
    train_dirs.sort(key=os.path.getmtime, reverse=True)  # Newest first

    if train_dirs:
        latest_train_dir = train_dirs[0]
        best_model_path = os.path.join(latest_train_dir, "weights", "best.pt")

        # Where to export the model
        export_path = "C:/Users/Prince/OneDrive - University of Cape Town/AYOS4/EEE4113F/Moulting Detection Subsystem/YOLOv11/moulting_stage_detector.pt"

        # Copy the model
        if os.path.exists(best_model_path):
            shutil.copy(best_model_path, export_path)
            print(f"Model exported from {best_model_path} to:\n{export_path}")
        else:
            print("No best.pt found in latest training folder.")
    else:
        print("No training folders found in runs/detect/")
    # Evaluate the model's performance on the validation set
    metrics = model.val()

    # Perform object detection on an image
    print("Training successfully complete with",50,"epochs")

if __name__ == '__main__':
    train_model()
    