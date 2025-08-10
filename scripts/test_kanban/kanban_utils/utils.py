import cv2
import numpy as np

def combine_images(img_list, grid_shape=(2,2), size=(600,400)):
    """
    Combine a list of images into a single image arranged in a grid.
    """
    rows, cols = grid_shape
    small_images = []
    
    for img in img_list:
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        resized = cv2.resize(img, size)
        small_images.append(resized)
    
    # Combine images into rows
    rows_images = []
    for r in range(rows):
        row_imgs = small_images[r*cols:(r+1)*cols]
        row_combined = np.hstack(row_imgs)
        rows_images.append(row_combined)

    # Combine rows into final image
    final_image = np.vstack(rows_images)
    return final_image
