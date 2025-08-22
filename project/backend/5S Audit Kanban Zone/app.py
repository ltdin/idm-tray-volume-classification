from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, uuid, logging
from pathlib import Path
from predict_core import process_kanban_batch 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_DIR = os.getenv("KANBAN_UPLOAD_DIR", "upload")
OUTPUT_DIR = os.getenv("KANBAN_OUTPUT_DIR", "output")
BASE_URL   = os.getenv("KANBAN_BASE_URL", "http://localhost:5002")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route("/predict", methods=["POST"])
def predict_kanban():
    if "images" not in request.files:
        return jsonify({"error": "No images uploaded"}), 400
    files = request.files.getlist("images")
    if not files:
        return jsonify({"error": "Empty images list"}), 400
    try:
        resp = process_kanban_batch(
            files=files,
            base_url=BASE_URL.rstrip("/"),
            upload_dir=UPLOAD_DIR,
            output_dir=OUTPUT_DIR
        )
        return jsonify(resp), 200
    except Exception as e:
        logger.exception("predict-kanban failed")
        return jsonify({"error": str(e)}), 500

@app.route("/output/<path:filename>", methods=["GET"])
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
