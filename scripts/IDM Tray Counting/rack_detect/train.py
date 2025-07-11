from ultralytics import YOLO

# Create a YOLO model instance 
model = YOLO("yolov8n.pt") 

# Train the model
model.train(
    data="../data_preprocessed/data.yaml", 
    epochs=100,
    imgsz=448,
    batch=8,
    # patience=7,
    project="../rack_detect/results",
    resume=False,
    verbose=True,
)
