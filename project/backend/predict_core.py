import os
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import uuid

# Load models once
yolo_model = YOLO("models/best.pt")
cnn_model = load_model("models/volume_mobilenetv2_model.h5")

def run_prediction(image_path, prefix="rack", start_index=1):
    original = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    results = yolo_model.predict(image_path, imgsz=448, conf=0.4)[0]
    boxes = results.boxes.xyxy.cpu().numpy()

    volume_data = []
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        try:
            crop = rgb_img[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            resized = cv2.resize(crop, (224, 224))
            norm_img = resized / 255.0
            input_img = np.expand_dims(norm_img, axis=0)

            pred = cnn_model.predict(input_img)[0][0] * 100
            pred = np.clip(pred, 0, 100)

            quantity = round(1161 * pred / 100)

            label = f"Rack: {pred:.2f}%"
            cv2.rectangle(original, (x1, y1), (x2, y2), (255, 0, 0), 4)
            text_y = max(30, y1 - 10)
            cv2.putText(original, label, (x1, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

            volume_data.append({
                "rack_id": f"{prefix} No.{start_index + i}",
                "bbox": [x1, y1, x2, y2],
                "volume": round(float(pred), 2),
                "quantity": quantity
            })

        except Exception as e:
            print(f"[ERROR] Error with box {i+1}: {e}")
            continue

    # Save annotated image
    save_name = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join("output", save_name)
    cv2.imwrite(output_path, original)

    return {
        "racks": volume_data,
        "annotated_path": f"http://localhost:5000/output/{save_name}"
    }
