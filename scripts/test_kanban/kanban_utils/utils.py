import cv2
import numpy as np

def combine_images(img_list, grid_shape=(2,2), size=(600,400)):
    """
    Ghép nhiều ảnh thành 1 ảnh lớn.
    - img_list: list các ảnh (BGR hoặc Gray)
    - grid_shape: (rows, cols)
    - size: kích thước từng ảnh con
    """
    rows, cols = grid_shape
    small_images = []
    
    for img in img_list:
        # Chuyển gray thành BGR nếu cần
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        resized = cv2.resize(img, size)
        small_images.append(resized)
    
    # Ghép theo từng hàng
    rows_images = []
    for r in range(rows):
        row_imgs = small_images[r*cols:(r+1)*cols]
        row_combined = np.hstack(row_imgs)
        rows_images.append(row_combined)
    
    # Ghép các hàng thành ảnh cuối
    final_image = np.vstack(rows_images)
    return final_image
