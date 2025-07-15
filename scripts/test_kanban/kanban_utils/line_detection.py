import cv2
import numpy as np

def detect_lines(mask, min_line_length=50, max_line_gap=300, canny_threshold1=50, canny_threshold2=150):
    """
    Tìm các lines trên mask bằng HoughLinesP
    """
    # Tìm edges
    edges = cv2.Canny(mask, canny_threshold1, canny_threshold2, apertureSize=3)

    # Hough Transform
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=50,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap
    )

    return lines

def draw_lines(image, lines, color=(0,255,0), thickness=3):
    """
    Vẽ các lines lên ảnh
    """
    img_copy = image.copy()
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(img_copy, (x1, y1), (x2, y2), color, thickness)
    return img_copy
