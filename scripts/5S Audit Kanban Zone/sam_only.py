import torch
import cv2
import numpy as np
import glob
import os
from segment_anything import sam_model_registry, SamPredictor

sam_checkpoint = "../5S Audit Kanban Zone/model/sam_vit_b_01ec64.pth"
model_type = "vit_b"

image_dir = "../5S Audit Kanban Zone/kanban_dataset/test/images/"
masked_dir = "../5S Audit Kanban Zone/results/masked/"

os.makedirs(masked_dir, exist_ok=True)

input_box = np.array([100, 150, 500, 600])

scale = 1.2

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to("cuda" if torch.cuda.is_available() else "cpu")
predictor = SamPredictor(sam)

image_paths = glob.glob(os.path.join(image_dir, "*.jpg"))
print(f"[OK] Found {len(image_paths)} images.")

for image_path in image_paths:
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, _ = image.shape
    
    box_w = input_box[2] - input_box[0]
    box_h = input_box[3] - input_box[1]
    new_w = box_w * scale
    new_h = box_h * scale

    center_x = (input_box[0] + input_box[2]) / 2
    center_y = (input_box[1] + input_box[3]) / 2

    new_x_min = max(0, center_x - new_w / 2)
    new_y_min = max(0, center_y - new_h / 2)
    new_x_max = min(w, center_x + new_w / 2)
    new_y_max = min(h, center_y + new_h / 2)

    new_box = np.array([
        new_x_min,
        new_y_min,
        new_x_max,
        new_y_max
    ], dtype=np.float32)

    higher_y = max(0, center_y - new_h * 0.3)

    point_coords = np.array([
        [center_x, center_y],
        [center_x, higher_y]
    ])
    point_labels = np.array([1, 1])

    print(f"Using box: {new_box} for image {image_path}")
    print(f"Point prompts: {point_coords}")

    predictor.set_image(image_rgb)

    masks, scores, logits = predictor.predict(
        box=new_box,
        point_coords=point_coords,
        point_labels=point_labels,
        multimask_output=True
    )
    
    best_mask = None
    max_area = 0
    for m in masks:
        area = np.sum(m)
        if area > max_area:
            max_area = area
            best_mask = m

    if best_mask is None:
        print("[WARN] No mask found.")
        continue

    masked_img = image.copy()
    masked_img[~best_mask] = 0

    file_stem = os.path.splitext(os.path.basename(image_path))[0]
    save_path = os.path.join(masked_dir, f"{file_stem}_masked.png")
    cv2.imwrite(save_path, masked_img)

    print(f"[OK] Masked image saved: {save_path}")

print("[OK] All done!")
