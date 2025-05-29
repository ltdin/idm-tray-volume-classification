from roboflow import Roboflow

rf = Roboflow(api_key="d1oW7OTNqLiVqRb1zN4c")
project = rf.workspace("l-thnh-vinh-j9hig").project("rack-detection-tray-counting")
version = project.version(1)
dataset = version.download("yolov8")
