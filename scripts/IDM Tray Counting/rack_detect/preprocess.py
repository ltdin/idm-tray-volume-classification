import os
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm


IMAGE_SIZE = (448, 448)
INPUT_DIR = r"C:\Users\ADMIN\Documents\Study\Capstone A\Model\roboflow_dataset"
OUTPUT_DIR = r"C:\Users\ADMIN\Documents\Study\Capstone A\Model\data_preprocessed"
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")

# Augmentation Pipeline 
transform = A.Compose([
    A.RandomBrightnessContrast(p=0.3),
    A.Rotate(limit=15, p=0.4),
    A.Resize(IMAGE_SIZE[1], IMAGE_SIZE[0]),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

def load_labels(label_path):
    labels = []
    with open(label_path, 'r') as file:
        for line in file:
            items = line.strip().split()
            if len(items) == 5:
                labels.append((int(items[0]), float(items[1]), float(items[2]), float(items[3]), float(items[4])))
    return labels

def save_labels(label_path, labels):
    with open(label_path, 'w') as file:
        for cls, x, y, w, h in labels:
            file.write(f"{cls} {x} {y} {w} {h}\n")

def count_labels(all_labels):
    counter = Counter()
    for label_list in all_labels:
        for label in label_list:
            counter[label[0]] += 1
    return counter

# Main
all_class_labels = []

for subset in ["train", "valid", "test"]:
    image_dir = os.path.join(INPUT_DIR, subset, "images")
    label_dir = os.path.join(INPUT_DIR, subset, "labels")
    out_image_dir = os.path.join(OUTPUT_DIR, subset, "images")
    out_label_dir = os.path.join(OUTPUT_DIR, subset, "labels")
    os.makedirs(out_image_dir, exist_ok=True)
    os.makedirs(out_label_dir, exist_ok=True)

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(VALID_EXTENSIONS)]
    for fname in tqdm(image_files, desc=f"Augmenting {subset}", unit="img"):
        if not fname.lower().endswith(VALID_EXTENSIONS):
            continue

        image_path = os.path.join(image_dir, fname)
        label_path = os.path.join(label_dir, os.path.splitext(fname)[0] + ".txt")
        if not os.path.exists(label_path):
            continue

        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        labels = load_labels(label_path)
        all_class_labels.append(labels)

        bboxes = [box[1:] for box in labels]
        class_labels = [box[0] for box in labels]

        # Apply augmentation
        transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
        aug_img = transformed['image']
        aug_bboxes = transformed['bboxes']
        aug_classes = transformed['class_labels']

        # Save image
        aug_fname = os.path.splitext(fname)[0] + "_aug.jpg"
        out_img_path = os.path.join(out_image_dir, aug_fname)
        cv2.imwrite(out_img_path, aug_img)
        
        # Save labels
        aug_label_path = os.path.join(out_label_dir, os.path.splitext(fname)[0] + "_aug.txt")
        save_labels(aug_label_path, list(zip(aug_classes, *zip(*aug_bboxes))) if aug_bboxes else [])

print("[OK] Augmentation & copy done.")

# Check balance
label_counts = count_labels(all_class_labels)

print("\n[OK] Class distribution across dataset:")
for cls, count in label_counts.items():
    print(f"Class {cls}: {count} objects")

# Optional: visualize
plt.bar(label_counts.keys(), label_counts.values())
plt.xlabel("Class ID")
plt.ylabel("Count")
plt.title("Label Distribution in Original Dataset")
plt.show()
