import cv2
import numpy as np

def create_blue_mask(image, lower_hsv=[100, 150, 50], upper_hsv=[120, 255, 240]):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array(lower_hsv)
    upper = np.array(upper_hsv)
    
    mask = cv2.inRange(hsv, lower, upper)

    # Morphological cleaning
    kernel = np.ones((3,3), np.uint8)
    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN, kernel)

    return mask_clean