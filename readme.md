# EEE4113F-2025-Group-14-Project

# Penguin Moulting Stage Detection System  

## Overview  

This system automates the detection of penguin moulting stages using **YOLOv11** for object detection. It processes penguin images through a **multi-stage pipeline**, including database operations, penguin record management, and moulting stage classification.  

---

## System Components  

### **1. Main Pipeline (`Automated_Penguin_Moulting_Stage_Detection.py`)**  
- **Coordinates the entire workflow** by executing all components in sequence:  
  1. **Uploads images** to **DB1 (Supabase)**  
  2. **Downloads images** from DB1  
  3. **Creates penguin records** in **DB2 (Analytics DB)**  
  4. **Updates penguin records** with moulting status  

### **2. Database Operations**  
- **`Upload_To_DB1.py`**  
  - Uploads images from a local folder (`Database Testing/Uploads`) to **Supabase**  
  - Handles duplicates by updating existing records  
- **`Download_From_DB1.py`**  
  - Downloads images from **Supabase**  
  - **Deletes records** after download to prevent reprocessing  

### **3. Penguin Record Management**  
- **`CreatePenguin.py`**  
  - Creates new penguin records in **DB2** (if they don’t exist)  
  - Uses RFID tags from filenames to generate penguin IDs  
- **`UpdatePenguin.py`**  
  - Uses **YOLOv11** to detect moulting status (`moulting` or `done`)  
  - Updates penguin records with **moulting stage + random mass**  
  - **Deletes processed images** locally  

### **4. Machine Learning Model**  
- **`yolov11_detector_trainer.py`**  
  - **Trains a YOLOv11 model** for moulting detection  
  - Exports the best model to `YOLOv11/moulting_stage_detector.pt`  
- **`config.yaml`**  
  - Configuration for **dataset paths, classes, augmentation, and training**  

---

## Installation  

### **Prerequisites**  
- Python 3.8+  
- Supabase & Render.com API access  

### **Setup**  
1. **Clone the repository**  
   ```sh
   git clone <repo-url>
   cd penguin-moulting-detection
   ```  

2. **Install dependencies**  
   ```sh
   pip install ultralytics supabase requests
   ```  

3. **Configure database credentials** in:  
   - `Upload_To_DB1.py` (Supabase URL & Key)  
   - `Download_From_DB1.py` (Supabase URL & Key)  

4. **Place images** in:  
   - `Database Testing/Uploads/` (for processing)  

---

## Usage  

### **1. Training the Model**  
```sh
python yolov11_detector_trainer.py
```  
- Trains for **50 epochs**  
- Exports best model to `YOLOv11/moulting_stage_detector.pt`  

### **2. Running the Full Pipeline**  
```sh
python Automated_Penguin_Moulting_Stage_Detection.py
```  
- Automatically processes new images and updates penguin records.  

### **3. Manual Execution (Optional)**  
Run individual scripts in order:  
1. `Upload_To_DB1.py`  
2. `Download_From_DB1.py`  
3. `CreatePenguin.py`  
4. `UpdatePenguin.py`  

---

## Configuration  

### **File Structure**  
```
📂 Database Testing/  
├── 📂 Uploads/          # Input images
└── 📂 Downloads copy/   # Processed images (auto-deleted)
📂 YOLOv11/  
├── config.yaml          # YOLO training config  
└── moulting_stage_detector.pt  # Trained model  
```  

### **Key Configurations (`config.yaml`)**  
- **Classes:** `["Moulting_Penguin", "Penguin_Not_Moulting"]`  
- **Augmentations:**  
  - Rotation, scaling, motion blur  
  - Color adjustments for better moulting detection  
- **Loss weights:**  
  - Higher focus on **class prediction** (`cls: 0.8`)  

---

## Workflow  

1. **Upload** images to **Supabase (DB1)**  
2. **Download & process** images locally  
3. **Create/update** penguin records in **DB2**  
4. **Detect moulting stage** using YOLOv11  
5. **Update penguin status** (`moulting` or `done`)  
6. **Delete processed images** (cleanup)  

---

## Notes  

- **DB1 (Supabase):** Temporary storage for raw images  
- **DB2 (Render.com):** Permanent penguin records with moulting status  
- **Random mass values** are generated for demo purposes  
- **Images are auto-deleted** after processing  

---
