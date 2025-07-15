import cv2
import numpy as np

def find_largest_contour_polygon(mask, epsilon_ratio=0.02):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    # Get highest area contour
    c = max(contours, key=cv2.contourArea)

    # Approximate to polygon
    epsilon = epsilon_ratio * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    
    approx_pts = approx.reshape(-1, 2)
    
    return approx, approx_pts

def draw_polygon(image, polygon, color=(0,255,0), thickness=3):
    img_copy = image.copy()
    cv2.drawContours(img_copy, [polygon], -1, color, thickness)
    return img_copy
