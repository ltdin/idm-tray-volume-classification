from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np
import os
from typing import List, Tuple

# CONFIG 
KANBAN_MODEL = r"../test_kanban/kanban_zone_seg/kanban_zone_seg/weights/best.pt"
WHEEL_MODEL  = r"../test_kanban/wheels_seg3/wheels_seg3/weights/best.pt"

# Upload 3 folders image for testing
INPUT_DIRS = [
    r"../test_kanban/OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/just straight line/",
    r"../test_kanban/OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/rectangular angle//",
    r"../test_kanban/OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/rectangular straight//",
]

# Get output directory
OUTPUT_DIR = Path("runs/kanban/predict")
IMGSZ = 640
CONF  = 0.7

# BGR color
COLOR_IN   = (255,  0,  0) 
COLOR_OUT  = (  0,  0,255)  
COLOR_ZONE = (200,255,200)  

def list_images(dirs: List[str]) -> List[Path]:
    exts = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")
    files = []
    for d in dirs:
        p = Path(d)
        if not p.exists():
            print(f"[WARN] Folder not found: {p}")
            continue
        for f in p.rglob("*"):
            if f.suffix.lower() in exts:
                files.append(f)
    files.sort()
    return files

def largest_polygon_xy(masks_xy: List[np.ndarray]) -> np.ndarray:
    """Select the largest polygon by area from masks.xy (list of Nx2 arrays)."""
    if not masks_xy:
        return None
    areas = []
    for poly in masks_xy:
        if poly is None or len(poly) < 3:
            areas.append(0.0)
        else:
            areas.append(cv2.contourArea(poly.astype(np.float32)))
    idx = int(np.argmax(areas))
    return masks_xy[idx] if areas[idx] > 0 else None

def rasterize_polygon(poly_xy: np.ndarray, shape_hw: Tuple[int,int]) -> np.ndarray:
    """Create a binary mask (0/1) from the polygon pixel points."""
    H, W = shape_hw
    m = np.zeros((H, W), dtype=np.uint8)
    if poly_xy is not None and len(poly_xy) >= 3:
        cv2.fillPoly(m, [poly_xy.astype(np.int32)], 1)
    return m

def rasterize_wheel(result, idx: int, shape_hw: Tuple[int,int]) -> Tuple[np.ndarray, Tuple[int,int,int,int]]:
    """
    Return (mask_binary_0_1, bbox_xyxy_int) of 1 wheel.
    """
    H, W = shape_hw
    # BBox
    box = result.boxes.xyxy.cpu().numpy()[idx].astype(int)
    x1, y1, x2, y2 = box.tolist()

    # If segmentation masks are available
    wheel_mask = np.zeros((H, W), dtype=np.uint8)
    if result.masks is not None and result.masks.xy is not None and len(result.masks.xy) > idx:
        poly = result.masks.xy[idx]
        if poly is not None and len(poly) >= 3:
            cv2.fillPoly(wheel_mask, [poly.astype(np.int32)], 1)
        else:
            wheel_mask[y1:y2, x1:x2] = 1
    else:
        wheel_mask[y1:y2, x1:x2] = 1

    return wheel_mask, (x1, y1, x2, y2)

def decide_in_out(zone_mask: np.ndarray, wheel_mask: np.ndarray) -> str:
    if zone_mask is None or zone_mask.max() == 0:
        return "OUT" 
    outside = (wheel_mask == 1) & (zone_mask == 0)
    return "OUT" if np.any(outside) else "IN"

def draw_polygon(img, poly_xy: np.ndarray, color=COLOR_ZONE, thickness=2):
    if poly_xy is not None and len(poly_xy) >= 2:
        cv2.polylines(img, [poly_xy.astype(np.int32)], isClosed=True, color=color, thickness=thickness)

def process_image(img_path: Path, zone_model: YOLO, wheel_model: YOLO, out_dir: Path):
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"[SKIP] Cannot read image: {img_path}")
        return

    H, W = img.shape[:2]
    # Predict zone
    zres = zone_model.predict(source=img, imgsz=IMGSZ, conf=CONF, verbose=False)[0]
    zone_poly = None
    if zres.masks is not None and zres.masks.xy:
        zone_poly = largest_polygon_xy(zres.masks.xy)
    zone_mask = rasterize_polygon(zone_poly, (H, W))

    # Predict wheels
    wres = wheel_model.predict(source=img, imgsz=IMGSZ, conf=CONF, verbose=False)[0]
    n_wheels = len(wres.boxes.xyxy) if wres.boxes is not None else 0

    # Draw zone polygon
    draw_polygon(img, zone_poly, COLOR_ZONE, thickness=2)

    # Check each wheel
    print(f"\n[IMAGE] {img_path.name}  |  Wheels: {n_wheels}")
    for i in range(n_wheels):
        wheel_mask, (x1, y1, x2, y2) = rasterize_wheel(wres, i, (H, W))
        status = decide_in_out(zone_mask, wheel_mask)
        color  = COLOR_IN if status == "IN" else COLOR_OUT

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 12)
        cv2.putText(img, status, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 4, cv2.LINE_AA)

        print(f"  - Wheel #{i+1}: {status}")

    # Save out
    out_dir.mkdir(parents=True, exist_ok=True)
    save_path = out_dir / img_path.name
    cv2.imwrite(str(save_path), img)
    print(f"[SAVED] {save_path}")

def main():
    # Model reloaded
    zone_model  = YOLO(KANBAN_MODEL)
    wheel_model = YOLO(WHEEL_MODEL)

    all_imgs = list_images(INPUT_DIRS)
    if not all_imgs:
        print("[ERROR] No images found in INPUT_DIRS.")
        return

    print(f"[INFO] Found {len(all_imgs)} images. Saving all results to: {OUTPUT_DIR.resolve()}")
    for img_path in all_imgs:
        try:
            process_image(img_path, zone_model, wheel_model, OUTPUT_DIR)
        except Exception as e:
            print(f"[ERROR] {img_path.name}: {e}")

if __name__ == "__main__":
    main()
