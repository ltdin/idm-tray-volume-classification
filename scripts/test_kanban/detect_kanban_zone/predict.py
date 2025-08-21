from ultralytics import YOLO
from pathlib import Path

MODEL_PATH = "../kanban_zone_seg/kanban_zone_seg/weights/best.pt"
SOURCE = "../OneDrive_2025-08-17/kanban image for logic test ( 3 cases)/rectangular angle/DSC01120.jpg"  
IMGSZ = 640
CONF = 0.5

def main():
    model = YOLO(MODEL_PATH)

    results = model.predict(
        source=SOURCE,
        imgsz=IMGSZ,
        conf=CONF,   
        save=True,          
        save_txt=False,      
        save_conf=False,   
        project="runs/kanban",  
        name="predict",          
        exist_ok=True           
    )

    # Save file
    out_dir = Path(results[0].save_dir) 
    print(f"Predicted images saved to: {out_dir.resolve()}")

if __name__ == "__main__":
    main()
