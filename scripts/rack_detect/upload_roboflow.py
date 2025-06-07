import os
from roboflow import Roboflow

# Step 1: Input API key
API_KEY = "d1oW7OTNqLiVqRb1zN4c"  

# Step 2: Workspace and project infomation
WORKSPACE = "l-thnh-vinh-j9hig"
PROJECT = "rack-detection-tray-counting-2"

# Step 3: Connect to Roboflow
rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT)

# Step 4: Address the dataset directory
DATASET_DIR = "../../../Dataset/30_05"

# Step 5: List all folders in the dataset directory
for volume_folder in sorted(os.listdir(DATASET_DIR)):
    folder_path = os.path.join(DATASET_DIR, volume_folder)
    if not os.path.isdir(folder_path):
        continue

    print(f"\n[OK] Uploading from folder: {folder_path} (Volume {volume_folder}%)")

    for file in os.listdir(folder_path):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(folder_path, file)
            try:
                upload_result = project.upload(img_path, batch_name=f"Volume {volume_folder}%")
                print(f"[OK] Uploaded: {file}")
            except Exception as e:
                print(f"[ERROR] Failed: {file} ({e})")
