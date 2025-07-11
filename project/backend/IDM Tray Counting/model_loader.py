from database import versions_collection
from ultralytics import YOLO

def load_current_model():
    version = versions_collection.find_one({"is_current": True})
    if not version:
        raise RuntimeError("No active model version found.")

    model_path = version["files"]["best_pt"]
    from ultralytics import YOLO
    model = YOLO(model_path)
    return model
