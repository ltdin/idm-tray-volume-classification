import os

# Chỉnh đường dẫn này về đúng thư mục dataset của bạn
BASE_DIR = r"C:\Users\ADMIN\Documents\Study\Capstone A\Model\data_preprocessed"

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")

def count_images_in_folder(folder_path):
    count = 0
    if not os.path.exists(folder_path):
        return 0
    for file in os.listdir(folder_path):
        if file.lower().endswith(VALID_EXTENSIONS):
            count += 1
    return count

def main():
    for subset in ["train", "valid", "test"]:
        folder = os.path.join(BASE_DIR, subset, "images")
        num_images = count_images_in_folder(folder)
        print(f"[{subset.upper()}] 📸 {num_images} images")

if __name__ == "__main__":
    main()
