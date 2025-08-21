import os
import cv2
import glob
import numpy as np
from ultralytics import YOLO
from kanban_utils.image_io import read_image
from kanban_utils.preprocessing import enhance_clahe
from kanban_utils.segmentation import create_blue_mask
from kanban_utils.line_detection import detect_lines


# Path
INPUT_DIRS = [
    r"../OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/just straight line/",
    r"../OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/rectangular angle/",
    r"../OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/rectangular straight/",
]

# Model YOLO wheels
MODEL_PATH = r"../wheels_seg3/wheels_seg3/weights/best.pt"
IMG_SIZE   = 1280
CONF       = 0.5

# Export path
OUTPUT_DIR = "pred_inout_results_batch"

# Line
FOCUS_BOTTOM_ONLY   = True
LINE_DRAW_THICKNESS = 3 
DILATE_KERNEL       = 3   

# BBox
BOX_THICKNESS  = 3
FONT           = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE     = 0.7
TEXT_THICKNESS = 2
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}



def make_line_mask_from_lines(lines, shape_hw, thickness=6, dilate_k=3):
    H, W = shape_hw
    m = np.zeros((H, W), dtype=np.uint8)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(m, (int(x1), int(y1)), (int(x2), int(y2)), 255, thickness=thickness)
    if dilate_k and dilate_k > 1:
        kernel = np.ones((dilate_k, dilate_k), np.uint8)
        m = cv2.dilate(m, kernel, iterations=1)
    return m

def bbox_overlaps_mask(bbox_xyxy, mask):
    x1, y1, x2, y2 = bbox_xyxy
    H, W = mask.shape
    xi1 = max(0, int(np.floor(x1)))
    yi1 = max(0, int(np.floor(y1)))
    xi2 = min(W, int(np.ceil(x2)))
    yi2 = min(H, int(np.ceil(y2)))
    if xi1 >= xi2 or yi1 >= yi2:
        return False
    crop = mask[yi1:yi2, xi1:xi2]
    return np.any(crop > 0)

def process_image(model, image_path, out_dir):
    # Read + enhance
    image = read_image(image_path)
    image_enh = enhance_clahe(image)

    # Blue mask -> detect lines
    mask = create_blue_mask(image_enh)
    if FOCUS_BOTTOM_ONLY:
        h, w = mask.shape
        mask[:h // 2, :] = 0

    lines = detect_lines(mask)
    line_mask = make_line_mask_from_lines(
        lines, shape_hw=mask.shape,
        thickness=LINE_DRAW_THICKNESS,
        dilate_k=DILATE_KERNEL
    )

    # YOLO detect wheels (bbox)
    results = model.predict(
        source=image_path,
        imgsz=IMG_SIZE,
        conf=CONF,
        save=False,
        verbose=False,
        show_labels=False,
        show_conf=False,
        show_boxes=True
    )

    # Draw in/out boxes
    vis = image.copy()
    in_count, out_count = 0, 0

    for r in results:
        if r.boxes is None or len(r.boxes) == 0:
            continue
        for box in r.boxes.xyxy.cpu().numpy():
            x1, y1, x2, y2 = box.tolist()
            is_out = bbox_overlaps_mask((x1, y1, x2, y2), line_mask)
            color  = (0, 0, 255) if is_out else (0, 200, 0)
            label  = "OUT" if is_out else "IN"
            if is_out: out_count += 1
            else:      in_count  += 1

            cv2.rectangle(vis, (int(x1), int(y1)), (int(x2), int(y2)), color, BOX_THICKNESS)
            cv2.putText(vis, label, (int(x1), int(y1) - 6), FONT, FONT_SCALE, color, TEXT_THICKNESS, cv2.LINE_AA)

    # Save
    base = os.path.splitext(os.path.basename(image_path))[0]
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, f"{base}_line_mask.jpg"), line_mask)
    cv2.imwrite(os.path.join(out_dir, f"{base}_inout.jpg"), vis)

    print(f"[OK] {os.path.basename(image_path)} -> IN:{in_count} OUT:{out_count}")

def collect_images_from_dirs(dirs):
    paths = []
    for d in dirs:
        for p in glob.glob(os.path.join(d, "*")):
            ext = os.path.splitext(p)[1].lower()
            if ext in IMG_EXTS and os.path.isfile(p):
                paths.append(p)
    return sorted(paths)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    image_paths = collect_images_from_dirs(INPUT_DIRS)
    if not image_paths:
        print("No images found. Please check INPUT_DIRS.")
        return

    # Load YOLO
    model = YOLO(MODEL_PATH)

    print(f"Found {len(image_paths)} images. Processing...")
    for img_path in image_paths:
        try:
            process_image(model, img_path, OUTPUT_DIR)
        except Exception as e:
            print(f"[ERROR] {img_path}: {e}")
            
    print(f"Done. Saved results to: {os.path.abspath(OUTPUT_DIR)}")
if __name__ == "__main__":
    main()