import cv2
import easyocr
import re

reader = easyocr.Reader(['en'])

def resize_to_2mp(img):
    original_height, original_width = img.shape[:2]
    target_pixels = 2_000_000
    aspect_ratio = original_width / original_height
    new_height = int((target_pixels / aspect_ratio) ** 0.5)
    new_width = int(aspect_ratio * new_height)
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_img

def extract_rack_id_from_image(image_path):
    try:
        img = cv2.imread(image_path)
        resized_img = resize_to_2mp(img)
        results = reader.readtext(resized_img)

        for detection in results:
            text = detection[1]
            digits = re.findall(r'\d', text)
            if len(digits) >= 5:
                return text.strip()
        return None
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return None
