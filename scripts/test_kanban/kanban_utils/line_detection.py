import cv2
import numpy as np

def detect_lines(mask, min_line_length=50, max_line_gap=300, canny_threshold1=50, canny_threshold2=150):
    """
    Find lines in the mask using Hough Transform and merge nearby parallel lines.
    """
    # Step 1: Find edges using Canny
    edges = cv2.Canny(mask, canny_threshold1, canny_threshold2, apertureSize=3)

    # Step 2: Apply Probabilistic Hough Line Transform
    raw_lines = cv2.HoughLinesP(
        mask,
        rho=1,
        theta=np.pi/180,
        threshold=50,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap
    )

    if raw_lines is None:
        return None

    # Step 3: Convert line format to more usable structure [(x1, y1, x2, y2), ...]
    lines = [tuple(line[0]) for line in raw_lines]

    # Step 4: Merge similar lines based on distance and angle
    merged_lines = []
    used = [False] * len(lines)
    angle_threshold = 10  
    distance_threshold = 0 

    def line_angle(line):
        x1, y1, x2, y2 = line
        return np.degrees(np.arctan2(y2 - y1, x2 - x1))

    def line_center(line):
        x1, y1, x2, y2 = line
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    for i in range(len(lines)):
        if used[i]:
            continue
        x1, y1, x2, y2 = lines[i]
        angle_i = line_angle(lines[i])
        cx_i, cy_i = line_center(lines[i])

        group = [lines[i]]
        used[i] = True

        for j in range(i + 1, len(lines)):
            if used[j]:
                continue
            angle_j = line_angle(lines[j])
            cx_j, cy_j = line_center(lines[j])
            angle_diff = abs(angle_i - angle_j)
            center_dist = np.hypot(cx_i - cx_j, cy_i - cy_j)

            if angle_diff < angle_threshold and center_dist < distance_threshold:
                group.append(lines[j])
                used[j] = True

        # Step 5: Average the group into one merged line
        xs = []
        ys = []
        for lx1, ly1, lx2, ly2 in group:
            xs.extend([lx1, lx2])
            ys.extend([ly1, ly2])
        x1_avg, x2_avg = int(min(xs)), int(max(xs))
        y1_avg = int(np.mean([y for x, y in zip(xs, ys) if x == x1_avg]))
        y2_avg = int(np.mean([y for x, y in zip(xs, ys) if x == x2_avg]))

        merged_lines.append([[x1_avg, y1_avg, x2_avg, y2_avg]])

    return merged_lines

def draw_lines(image, lines, color=(0,255,0), thickness=3):
    """
    Draw lines on the image.
    """
    img_copy = image.copy()
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(img_copy, (x1, y1), (x2, y2), color, thickness)
    return img_copy
