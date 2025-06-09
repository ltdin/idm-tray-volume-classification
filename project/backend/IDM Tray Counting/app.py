from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from predict_core import run_prediction

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "upload"
OUTPUT_FOLDER = "output"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/predict", methods=["POST"])
def predict():
    if "images" not in request.files:
        return jsonify({"error": "No images uploaded"}), 400

    files = request.files.getlist("images")
    results = []

    for file in files:
        filename = f"{uuid.uuid4().hex}.jpg"
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)

        result = run_prediction(upload_path)
        result["filename"] = filename
        print(result)  
        results.append(result)  

    return jsonify({"results": results})

@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
    

