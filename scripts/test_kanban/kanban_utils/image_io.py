import cv2

def read_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Can not find: {path}")
    return img

def show_image(title, img, max_width=1200):
    h, w = img.shape[:2]

    if w > max_width:
        scale = max_width / w
        new_size = (int(w * scale), int(h * scale))
        resized = cv2.resize(img, new_size)
    else:
        resized = img

    cv2.imshow(title, resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()