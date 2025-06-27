# Step 1: Crop rack from YOLOv8 predictions and save for CNN training
import os
import cv2
import numpy as np
from ultralytics import YOLO
import albumentations as A
from tqdm import tqdm

# --- CONFIG ---
YOLO_MODEL_PATH = "../rack_detect/results/train/weights/best.pt"
INPUT_DIR = "../volume_trays/volume_dataset/"
OUTPUT_BASE_DIR = "../volume_trays/dataset_preprocessed"
IMAGE_SIZE = (224, 224)
AUGMENT_TIMES = 3

# Albumentations augmentation
augment = A.Compose([
    A.RandomBrightnessContrast(p=0.5),
    A.Rotate(limit=10, p=0.5),
    A.ShiftScaleRotate(shift_limit_x=0.05, shift_limit_y=0.0, scale_limit=0.0, rotate_limit=0, p=0.3),
    A.Resize(IMAGE_SIZE[1], IMAGE_SIZE[0])
])

yolo_model = YOLO(YOLO_MODEL_PATH)

volume_folders = [f for f in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, f))]

for volume_folder in tqdm(volume_folders, desc="Processing volume folders"):
    input_volume_path = os.path.join(INPUT_DIR, volume_folder)

    try:
        volume_label = float(volume_folder.split('_')[-1])
    except ValueError:
        print(f"[SKIP] Invalid volume folder name: {volume_folder}")
        continue

    output_volume_path = os.path.join(OUTPUT_BASE_DIR, volume_folder)
    os.makedirs(output_volume_path, exist_ok=True)

    image_files = [f for f in os.listdir(input_volume_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for fname in tqdm(image_files, desc=f"{volume_folder}", leave=False):
        image_path = os.path.join(input_volume_path, fname)
        image = cv2.imread(image_path)
        if image is None:
            print(f"[SKIP] Failed to read image: {image_path}")
            continue

        results = yolo_model.predict(image_path, imgsz=448, conf=0.4)[0]
        boxes = results.boxes.xyxy.cpu().numpy()

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            crop = image[y1:y2, x1:x2]
            if crop.size == 0:
                print(f"[WARN] Empty crop for {fname} box {i+1}. Skipped.")
                continue

            for j in range(AUGMENT_TIMES):
                try:
                    augmented = augment(image=crop)
                    aug_img = augmented["image"]
                    save_name = f"{os.path.splitext(fname)[0]}_rack{i+1}_aug{j+1}.jpg"
                    save_path = os.path.join(output_volume_path, save_name)
                    cv2.imwrite(save_path, aug_img)
                    print(f"[OK] Saved: {save_path}")
                except Exception as e:
                    print(f"[ERROR] Augmenting rack {i+1} in {fname}: {e}")

print("[OK] All racks cropped and saved by volume.")
