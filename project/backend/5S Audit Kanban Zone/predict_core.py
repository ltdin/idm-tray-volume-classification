import os
import uuid
from pathlib import Path
from typing import List, Tuple, Dict, Any
import cv2
import numpy as np
from ultralytics import YOLO
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

KANBAN_MODEL = r"../../../scripts/5S Audit Kanban Zone/kanban_zone_seg/kanban_zone_seg/weights/best.pt"
WHEEL_MODEL  = r"../../../scripts/5S Audit Kanban Zone/wheels_seg3/weights/best.pt"

UPLOAD_DIR   = Path("upload_kanban")
OUTPUT_DIR   = Path("output")
IMGSZ        = 640
CONF         = 0.7

# BGR colors
COLOR_IN     = (255,   0,   0)   
COLOR_OUT    = (  0,   0, 255)   

_zone_model = None
_wheel_model = None

def _get_models() -> Tuple[YOLO, YOLO]:
    global _zone_model, _wheel_model
    if _zone_model is None:
        _zone_model = YOLO(KANBAN_MODEL)
    if _wheel_model is None:
        _wheel_model = YOLO(WHEEL_MODEL)
    return _zone_model, _wheel_model

def _largest_polygon_xy(masks_xy: List[np.ndarray]) -> np.ndarray:
    if not masks_xy:
        return None
    best_idx, best_area = -1, 0.0
    for i, poly in enumerate(masks_xy):
        if poly is None or len(poly) < 3:
            continue
        area = cv2.contourArea(poly.astype(np.float32))
        if area > best_area:
            best_area, best_idx = area, i
    return masks_xy[best_idx] if best_idx >= 0 else None


def _rasterize_polygon(poly_xy: np.ndarray, shape_hw: Tuple[int, int]) -> np.ndarray:

    H, W = shape_hw
    m = np.zeros((H, W), dtype=np.uint8)
    if poly_xy is not None and len(poly_xy) >= 3:
        cv2.fillPoly(m, [poly_xy.astype(np.int32)], 1)
    return m


def _wheel_mask_and_bbox(result, idx: int, shape_hw: Tuple[int, int]) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    H, W = shape_hw
    box = result.boxes.xyxy.cpu().numpy()[idx].astype(int)
    x1, y1, x2, y2 = box.tolist()

    wheel_mask = np.zeros((H, W), dtype=np.uint8)
    # Prefer segmentation if available; else fallback to bbox
    if result.masks is not None and result.masks.xy is not None and len(result.masks.xy) > idx:
        poly = result.masks.xy[idx]
        if poly is not None and len(poly) >= 3:
            cv2.fillPoly(wheel_mask, [poly.astype(np.int32)], 1)
        else:
            wheel_mask[y1:y2, x1:x2] = 1
    else:
        wheel_mask[y1:y2, x1:x2] = 1

    return wheel_mask, (x1, y1, x2, y2)


def _in_or_out(zone_mask: np.ndarray, wheel_mask: np.ndarray) -> str:
    """Wheel is OUT if any wheel pixel lies outside zone."""
    if zone_mask is None or zone_mask.max() == 0:
        return "OUT"  
    outside = (wheel_mask == 1) & (zone_mask == 0)
    return "OUT" if np.any(outside) else "IN"

def process_kanban_batch(files, base_url, upload_dir="upload", output_dir="output") -> Dict[str, Any]:
    # Prepare IO folders
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Persist uploads
    saved_items: List[Tuple[str, Path]] = [] 
    for f in files:
        orig = f.filename or "unnamed.jpg"
        safe = secure_filename(orig)
        saved = UPLOAD_DIR / f"{uuid.uuid4().hex}_{safe}"
        f.save(str(saved))
        saved_items.append((orig, saved))

    # Sort by original filename 
    saved_items.sort(key=lambda x: x[0].lower())

    zone_model, wheel_model = _get_models()
    results: List[Dict[str, Any]] = []

    for order_idx, (orig_name, saved_path) in enumerate(saved_items, start=1):
        img = cv2.imread(str(saved_path))
        if img is None:
            results.append({
                "order": order_idx,
                "filename": orig_name,
                "status": "WARN",          
                "num_wheels": 0,
                "in": 0,
                "out": 0,
                "wheels": [],
                "annotated_path": ""
            })
            continue

        H, W = img.shape[:2]

        # Predict Kanban zone (seg)
        zres = zone_model.predict(source=img, imgsz=IMGSZ, conf=CONF, verbose=False)[0]
        zone_poly = None
        if zres.masks is not None and zres.masks.xy:
            zone_poly = _largest_polygon_xy(zres.masks.xy)
        zone_mask = _rasterize_polygon(zone_poly, (H, W))

        # Predict wheels
        wres = wheel_model.predict(source=img, imgsz=IMGSZ, conf=CONF, verbose=False)[0]
        n_wheels = int(len(wres.boxes.xyxy)) if wres.boxes is not None else 0

        wheels_json = []
        all_in = True
        in_count = 0
        out_count = 0  
        
        for i in range(n_wheels):
            wmask, (x1, y1, x2, y2) = _wheel_mask_and_bbox(wres, i, (H, W))
            wstatus = _in_or_out(zone_mask, wmask)
            color = COLOR_IN if wstatus == "IN" else COLOR_OUT
            all_in = all_in and (wstatus == "IN")

            if wstatus == "IN":
                in_count += 1
            else:
                out_count += 1 

            # draw
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 6)
            cv2.putText(
                img, wstatus, (x1, max(30, y1 - 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, color, 3, cv2.LINE_AA
            )

            wheels_json.append({
                "index": i + 1,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "status": wstatus
            })

        # Image-level status
        image_status = "SAFE" if (zone_mask is not None and zone_mask.max() == 1 and all_in) else "WARN"

        # Save annotated
        out_name = f"{uuid.uuid4().hex}_kanban.png"
        out_path = OUTPUT_DIR / out_name
        cv2.imwrite(str(out_path), img)

        # Build URL
        base = base_url.rstrip("/") + "/"
        annotated_url = f"{base}output/{out_name}"

        results.append({
            "order": order_idx,
            "filename": orig_name,
            "status": image_status,
            "num_wheels": n_wheels,
            "in":  in_count,
            "out": out_count,
            "wheels": wheels_json,
            "annotated_path": annotated_url
        })

    return {"results": results}

