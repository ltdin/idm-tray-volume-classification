import os
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image, ImageDraw, ImageFont

# Load models 
yolo_model = YOLO("../runs/train/tray_detector/weights/best.pt") 
cnn_model = load_model("../../weights/volume_cnn_model.h5") 

# Input image 
image_path = "../../scripts/predict/input/Untitled design (1).png"
original = cv2.imread(image_path)
rgb_img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

# YOLOv8 detect
results = yolo_model.predict(image_path, imgsz=448, conf=0.4)[0]
boxes = results.boxes.xyxy.cpu().numpy()

# Prepare annotated image
annotated = Image.fromarray(rgb_img)
draw = ImageDraw.Draw(annotated)
font_path = "arial.ttf"  
font = ImageFont.truetype(font_path, size=100)  # Large readable font

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

        # Draw bounding box
        draw.rectangle([x1, y1, x2, y2], outline="blue", width=10)

        # Prepare label
        label = f"Rack: {pred:.2f}%"

        # Get label size
        text_bbox = draw.textbbox((x1, 0), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Position above bounding box
        padding = 20
        text_y = max(0, y1 - text_height - padding)
        text_bbox = draw.textbbox((x1, text_y), label, font=font)

        # Draw label background
        draw.rectangle(text_bbox, fill=(255, 255, 255))

        # Draw label text
        draw.text((x1, text_y), label, fill="blue", font=font)

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
annotated.save("../../scripts/predict/output/result.png")
print("[OK] Annotated image saved to output/result.png")

# Save CSV output
df = pd.DataFrame(volume_data)
df.to_csv("../../scripts/predict/output/predictions.csv", index=False)
print("[OK] Prediction CSV saved to output/predictions.csv")

print(f"Detected {len(boxes)} boxes.")
print(f"Saved {len(volume_data)} volume entries.")
