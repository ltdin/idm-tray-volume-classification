import torch
import cv2
import numpy as np
import glob
import os
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor
from shapely.geometry import Polygon, box

# Load YOLOv8-seg model
yolo_model = YOLO("../5S Audit Kanban Zone/results/yolov8_kanban_zone/weights/best.pt")

# Load SAM
sam_checkpoint = "../5S Audit Kanban Zone/model/sam_vit_b_01ec64.pth"
model_type = "vit_b"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to("cuda" if torch.cuda.is_available() else "cpu")
predictor = SamPredictor(sam)

# Folder setup
image_dir = "../5S Audit Kanban Zone/kanban_dataset/test/images/"
boxed_dir = "../5S Audit Kanban Zone/results/boxed/"
masked_dir = "../5S Audit Kanban Zone/results/masked/"
os.makedirs(boxed_dir, exist_ok=True)
os.makedirs(masked_dir, exist_ok=True)

image_paths = glob.glob(os.path.join(image_dir, "*.jpg"))
print(f"🔍 Found {len(image_paths)} images.")

for image_path in image_paths:
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictor.set_image(image_rgb)

    results = yolo_model.predict(image_path, save=False, verbose=False)
    zone_poly = None
    for r in results:
        if r.masks is None:
            continue
        for seg in r.masks.xy:
            zone_poly = Polygon(seg)
            zone_pts = np.array(seg, dtype=np.int32)
            cv2.polylines(image, [zone_pts], isClosed=True, color=(0, 255, 255), thickness=2)
            break
        if zone_poly:
            break

    if zone_poly is None:
        print(f"⚠ No kanban zone found in {image_path}")
        continue

    x_min, y_min, x_max, y_max = zone_poly.bounds
    input_box = np.array([x_min, y_min, x_max, y_max])

    masks, scores, logits = predictor.predict(box=input_box, multimask_output=False)
    mask = masks[0]
    masked_img = image.copy()
    masked_img[~mask] = 0

    file_stem = os.path.splitext(os.path.basename(image_path))[0]
    cv2.imwrite(os.path.join(masked_dir, f"{file_stem}_masked.png"), masked_img)

    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 3000:
            x, y, w, h = cv2.boundingRect(cnt)
            obj_box = box(x, y, x + w, y + h)
            inter_area = zone_poly.intersection(obj_box).area
            obj_area = obj_box.area
            ratio = inter_area / obj_area
            if ratio > 0.5:
                color = (0, 255, 0)
                label = f"IN {ratio:.2f}"
            else:
                color = (0, 0, 255)
                label = f"OUT {ratio:.2f}"
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imwrite(os.path.join(boxed_dir, f"{file_stem}_boxed.png"), image)

print("✅ All done!")
