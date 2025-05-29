import cv2
import os

INPUT_DIR = "C:\Users\ADMIN\Documents\Study\Capstone A\Model\data"
OUTPUT_DIR = "C:\Users\ADMIN\Documents\Study\Capstone A\Model\data_preprocessed"
IMAGE_SIZE = (448, 448)
VALID_EXTENSIONS = (".png")

if not os.path.exists(INPUT_DIR):
    raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for folder in os.listdir(INPUT_DIR):
    input_folder = os.path.join(INPUT_DIR, folder)
    output_folder = os.path.join(OUTPUT_DIR, folder)

    if not os.path.isdir(input_folder):
        print(f"[WARN] Skip {input_folder} (not a directory)")
        continue

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(VALID_EXTENSIONS):
            print(f"[SKIP] Skip invalid file: {filename}")
            continue

        img_path = os.path.join(input_folder, filename)
        try:
            image = cv2.imread(img_path)
            if image is None:
                print(f"[ERROR] Can not read this image: {img_path}")
                continue

            resized = cv2.resize(image, IMAGE_SIZE)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            out_path = os.path.join(output_folder, filename)
            cv2.imwrite(out_path, gray)
            print(f"[OK] Preprocessed: {img_path} → {out_path}")

        except Exception as e:
            print(f"[ERROR] Error when preprocessing {img_path}: {e}")

print("[OK] Preprocessing done.")
