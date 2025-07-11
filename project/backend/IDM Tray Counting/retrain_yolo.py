import os
import shutil
import datetime
import json
from ultralytics import YOLO
import glob
from database import versions_collection

def get_current_model_path():

    version_doc = versions_collection.find_one({"is_current": True})
    if not version_doc:
        raise RuntimeError("[ERROR] No current YOLO model found in MongoDB.")

    files = version_doc.get("files", {})
    best_pt_path = files.get("best_pt")

    if not best_pt_path or not os.path.exists(best_pt_path):
        raise RuntimeError(f"[ERROR] best.pt file not found at path: {best_pt_path}")

    print(f"[INFO] Using current YOLO model for retraining: {best_pt_path}")
    return best_pt_path


def retrain_yolo_model(note=""):
    print("Starting YOLO retraining...")

    model_path = get_current_model_path()

    yaml_path = "../../../scripts/IDM Tray Counting/data_preprocessed/data.yaml"
    project_path = "../../../scripts/IDM Tray Counting/rack_detect/results"
    os.makedirs(project_path, exist_ok=True)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"[ERROR] Model not found: {model_path}")

    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"[ERROR] data.yaml not found: {yaml_path}")

    model = YOLO(model_path)

    # Train
    results = model.train(
        data=yaml_path,
        epochs=1,
        imgsz=448,
        batch=8,
        resume=False,
        verbose=True,
        project=project_path
    )

    pattern = os.path.join(project_path, "*", "weights", "best.pt")
    candidates = glob.glob(pattern)

    if not candidates:
        print("[WARN] No best.pt found in YOLO training result.")
        return None, None

    # Pick latest modified
    best_weight_path = max(candidates, key=os.path.getmtime)
    latest_exp_dir = os.path.dirname(os.path.dirname(best_weight_path))
    print(f"[OK] Found best.pt at {best_weight_path}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    version_name = f"version_{timestamp}"
    version_dir = os.path.join("../models", version_name)
    os.makedirs(version_dir, exist_ok=True)
    new_best_pt = os.path.join(version_dir, "best.pt")
    shutil.copy(best_weight_path, new_best_pt)

    # Validate best.pt to extract metrics
    print("[INFO] Running validation on best.pt...")
    model_new = YOLO(new_best_pt)
    val_results = model_new.val(data=yaml_path)

    metrics = {
        "mAP50": float(val_results.box.map50),
        "mAP50-95": float(val_results.box.map),
        "precision": float(val_results.box.mp),
        "recall": float(val_results.box.mr)
    }
    print(f"[OK] YOLO metrics: {metrics}")

    # Save metrics JSON
    metrics_path = os.path.join(version_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[OK] Saved metrics.json to {metrics_path}")

    # Copy plots if exist
    plots = [
        "results.png",
        "confusion_matrix.png",
        "P_curve.png",
        "R_curve.png",
        "PR_curve.png",
        "F1_curve.png"
    ]

    files = {
        "best_pt": new_best_pt,
        "metrics_json": metrics_path,
    }

    for plot_name in plots:
        src = os.path.join(latest_exp_dir, plot_name)
        if os.path.exists(src):
            dst = os.path.join(version_dir, plot_name)
            shutil.copy(src, dst)
            files[plot_name.replace(".png", "")] = dst
            print(f"[OK] Copied plot: {plot_name}")

    # Save version info to MongoDB
    save_version_to_mongo(version_name, metrics, files, note)

    # Clean YOLO exp folder
    shutil.rmtree(latest_exp_dir, ignore_errors=True)
    print(f"[OK] Cleaned YOLO results folder: {latest_exp_dir}")

    print("[OK] YOLO retraining completed.")
    return version_name, version_dir


def save_version_to_mongo(version_name, metrics, files, note):
    """
    Save YOLO version info to MongoDB.
    """
    versions_collection.update_many({}, {"$set": {"is_current": False}})

    doc = {
        "version_name": version_name,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "metrics": metrics,
        "files": files,
        "note": note,
        "is_current": True
    }

    versions_collection.insert_one(doc)
    print(f"[OK] Saved YOLO version {version_name} to MongoDB.")
