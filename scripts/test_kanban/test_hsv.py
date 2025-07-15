import cv2
import numpy as np
from kanban_utils.image_io import read_image

def print_hsv_value(img, scale=0.3):
    """
    Click chuột vào ảnh để in ra giá trị HSV tại pixel.
    Scale ảnh nhỏ lại nếu quá to.
    """
    # Resize ảnh
    h, w = img.shape[:2]
    new_size = (int(w * scale), int(h * scale))
    img_resized = cv2.resize(img, new_size)

    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Scale to original coordinate
            orig_x = int(x / scale)
            orig_y = int(y / scale)
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            pixel = hsv[orig_y, orig_x]
            print(f"HSV tại pixel gốc ({orig_x},{orig_y}) = {pixel}")

    cv2.imshow("Click để lấy HSV", img_resized)
    cv2.setMouseCallback("Click để lấy HSV", callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    path = "../../DSC01285.jpg"
    image = read_image(path)
    print_hsv_value(image, scale=0.3)
