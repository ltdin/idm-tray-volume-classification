from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from retrain_yolo import retrain_yolo_model
from retrain_cnn import retrain_cnn_model
from model_loader import load_current_model
from database import versions_collection
import pandas as pd
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER_IMAGES = './uploads/yolo_images'
UPLOAD_FOLDER_LABELS = './uploads/yolo_labels'

os.makedirs(UPLOAD_FOLDER_IMAGES, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_LABELS, exist_ok=True)

@app.route("/api/training/upload", methods=["POST"])
def upload_training_data():
    note = request.form.get("note", "")

    if "yolo_images" not in request.files or "yolo_labels" not in request.files:
        return jsonify({"error": "[ERROR] Missing files"}), 400

    volume_label = request.form.get("volume", None)
    if volume_label is None:
        return jsonify({"error": "[ERROR] Missing volume label"}), 400

    volume_label = int(volume_label)

    image_files = request.files.getlist("yolo_images")
    label_files = request.files.getlist("yolo_labels")

    if len(image_files) != len(label_files):
        return jsonify({
            "error": f"[ERROR] Number of images ({len(image_files)}) and labels ({len(label_files)}) do not match."
        }), 400

    image_names = set(os.path.splitext(f.filename)[0] for f in image_files)
    label_names = set(os.path.splitext(f.filename)[0] for f in label_files)

    missing_labels = image_names - label_names
    if missing_labels:
        return jsonify({
            "error": f"[ERROR] Missing label files for images: {', '.join(missing_labels)}"
        }), 400

    for file in image_files:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER_IMAGES, filename))

    for file in label_files:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER_LABELS, filename))

    DATASET_TRAIN_IMAGES = "../../../scripts/IDM Tray Counting/data_preprocessed/train/images"
    DATASET_TRAIN_LABELS = "../../../scripts/IDM Tray Counting/data_preprocessed/train/labels"

    os.makedirs(DATASET_TRAIN_IMAGES, exist_ok=True)
    os.makedirs(DATASET_TRAIN_LABELS, exist_ok=True)

    for file in image_files:
        src = os.path.join(UPLOAD_FOLDER_IMAGES, file.filename)
        dst = os.path.join(DATASET_TRAIN_IMAGES, file.filename)
        shutil.copy(src, dst)

    for file in label_files:
        src = os.path.join(UPLOAD_FOLDER_LABELS, file.filename)
        dst = os.path.join(DATASET_TRAIN_LABELS, file.filename)
        shutil.copy(src, dst)

    print("[OK] YOLO data merged.")

    VOLUME_DATASET_DIR = "../../../scripts/IDM Tray Counting/volume_trays/dataset_preprocessed"
    CSV_PATH = "../../../scripts/IDM Tray Counting/volume_trays/csv/volume_labels.csv"

    os.makedirs(VOLUME_DATASET_DIR, exist_ok=True)

    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = pd.DataFrame(columns=["filename", "label"])

    new_rows = []
    for f in image_files:
        unique_name = f"{uuid.uuid4().hex}_{f.filename}"
        src = os.path.join(UPLOAD_FOLDER_IMAGES, f.filename)
        dst = os.path.join(VOLUME_DATASET_DIR, unique_name)
        shutil.copy(src, dst)

        new_rows.append({
            "filename": unique_name,
            "label": volume_label
        })

    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

    print(f"[OK] Volume data merged with label {volume_label}%.")

    return jsonify({
        "message": "[OK] Uploaded YOLO + Volume data successfully.",
        "note": note
    }), 200

@app.route("/api/training/retrain", methods=["POST"])
def retrain_models():
    version_name, version_dir = retrain_yolo_model()
    if version_name:
        retrain_cnn_model(version_name, version_dir)
        return jsonify({"message": f"[OK] Retrain finished for {version_name}"}), 200
    else:
        return jsonify({"error": "[ERROR] YOLO retrain failed"}), 500

@app.route("/api/model/versions", methods=["GET"])
def list_versions():
    versions = list(versions_collection.find({}, {"_id": 0}))
    return jsonify(versions)

@app.route("/api/model/use-version", methods=["POST"])
def use_version():
    req = request.get_json()
    version_name = req.get("version_name")

    version = versions_collection.find_one({"version_name": version_name})
    if not version:
        return jsonify({"error": "Version not found"}), 404

    versions_collection.update_many({}, {"$set": {"is_current": False}})
    versions_collection.update_one(
        {"version_name": version_name},
        {"$set": {"is_current": True}}
    )

    return jsonify({"message": f"Switched to {version_name}"}), 200

@app.route("/api/model/delete-version", methods=["POST"])
def delete_version():
    req = request.get_json()
    version_name = req.get("version_name")
    versions_collection.delete_one({"version_name": version_name})
    return jsonify({"message": f"Deleted {version_name}"}), 200

@app.route("/models/<path:filename>")
def serve_models(filename):
    return send_from_directory('../models', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
