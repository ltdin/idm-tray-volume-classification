from ultralytics import YOLO
import cv2
import os

model = YOLO("../runs/train/tray_detector/weights/best.pt")

input_dir = "../rack_detect/Rack-Detection-Tray-Counting--1/test/images"
output_dir = "outputs/inference"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.lower().endswith((".jpg", ".png")):
        img_path = os.path.join(input_dir, filename)
        results = model(img_path)
        annotated = results[0].plot() 
        out_path = os.path.join(output_dir, filename)
        cv2.imwrite(out_path, annotated)
