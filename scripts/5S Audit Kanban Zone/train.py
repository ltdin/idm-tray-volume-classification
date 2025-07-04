from ultralytics import YOLO
model = YOLO("yolov8n-seg.pt")  # or yolov8s-seg.pt/yolov8m-seg.pt tùy tài nguyên
model.train(data="../5S Audit Kanban Zone/kanban_dataset/data.yaml", 
            epochs=100, 
            imgsz=640,
            batch=8,
            resume=False,
            verbose=True,
            project="../5S Audit Kanban Zone/results",
            name="yolov8_kanban_zone",)
