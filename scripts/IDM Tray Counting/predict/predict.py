import os
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load models 
yolo_model = YOLO("../rack_detect/results/train/weights/best.pt") 
cnn_model = load_model("../../weights/volume_mobilenetv2_model.h5") 

# Input image 
image_path = "../../scripts/predict/input/z6656192617646_fc2e21de125013e5935519720e3a112d.jpg"
original = cv2.imread(image_path)
rgb_img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

# YOLOv8 detect
results = yolo_model.predict(image_path, imgsz=448, conf=0.4)[0]
boxes = results.boxes.xyxy.cpu().numpy()

volume_data = []

for i, box in enumerate(boxes):
    x1, y1, x2, y2 = map(int, box)

    try:
        crop = rgb_img[y1:y2, x1:x2]
        if crop.size == 0:
            print(f"[ERROR] Box {i+1} crop is empty. Skipping.")
            continue

        resized = cv2.resize(crop, (224, 224))
        norm_img = resized / 255.0
        input_img = np.expand_dims(norm_img, axis=0)

        pred = cnn_model.predict(input_img)[0][0] * 100
        pred = np.clip(pred, 0, 100)

        # Draw bounding box and label using cv2
        label = f"Rack: {pred:.2f}%"
        color = (255, 0, 0)  # Blue in BGR

        cv2.rectangle(original, (x1, y1), (x2, y2), color, 4)
        text_y = max(30, y1 - 10)
        cv2.putText(original, label, (x1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        # Save prediction data
        volume_data.append({
            "rack_id": f"rack_{i+1}",
            "bbox": [x1, y1, x2, y2],
            "volume": round(pred, 2)
        })

    except Exception as e:
        print(f"[ERROR] Error processing box {i+1}: {e}")
        continue

# Save annotated image
os.makedirs("output", exist_ok=True)
cv2.imwrite("../../scripts/predict/output/result.png", original)
print("[OK] Annotated image saved to output/result.png")

# Save CSV output
df = pd.DataFrame(volume_data)
df.to_csv("../../scripts/predict/output/predictions.csv", index=False)
print("[OK] Prediction CSV saved to output/predictions.csv")

print(f"Detected {len(boxes)} boxes.")
print(f"Saved {len(volume_data)} volume entries.")
