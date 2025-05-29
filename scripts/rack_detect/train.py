from ultralytics import YOLO

# Create a YOLO model instance 
model = YOLO("yolov8n.pt") 

# Train the model
model.train(
    data="../Rack-Detection-Tray-Counting--1/data.yaml", 
    epochs=50,
    imgsz=448,
    batch=8,
    patience=5,
    project="runs/train",
    name="tray_detector"
)
