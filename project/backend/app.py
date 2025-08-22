from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from OCR import extract_rack_id_from_image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "upload"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/ocr-check", methods=["POST"])
def ocr_check():
    if "image" not in request.files or "expected_id" not in request.form:
        return jsonify({"error": "Image and expected_id are required"}), 400

    file = request.files["image"]
    expected_id = request.form["expected_id"]

    filename = f"{uuid.uuid4().hex}.jpg"
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(upload_path)

    extracted_id = extract_rack_id_from_image(upload_path)
    match = extracted_id is not None and expected_id.strip() in extracted_id

    return jsonify({
        "match": match,
        "expected_id": expected_id,
        "extracted_text": extracted_id
    })

if __name__ == "__main__":
    app.run(debug=True)

