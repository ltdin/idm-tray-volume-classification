from kanban_utils.image_io import read_image, show_image
from kanban_utils.preprocessing import enhance_clahe
from kanban_utils.segmentation import create_blue_mask
from kanban_utils.contour_selection import find_largest_contour_polygon, draw_polygon
from kanban_utils.utils import combine_images
from kanban_utils.line_detection import detect_lines, draw_lines

def main():
    path = "../../DSC01294.jpg"

    # STEP 1 - Đọc ảnh gốc
    image = read_image(path)

    # STEP 2 - Cân bằng sáng CLAHE
    image_enhanced = enhance_clahe(image)

    # STEP 3 - Tạo mask tape xanh
    mask = create_blue_mask(image_enhanced)

    # STEP 4 - Tìm contour polygon
    polygon, approx_pts = find_largest_contour_polygon(mask)

    if polygon is not None:
        image_with_poly = draw_polygon(image_enhanced, polygon)
    else:
        image_with_poly = image_enhanced.copy()

    # STEP 5 - Tìm các lines bằng Hough Transform
    lines = detect_lines(mask)
    image_with_lines = draw_lines(image_enhanced, lines)

    # Combine all 4 images để xem cùng lúc
    combined = combine_images(
        [image, image_enhanced, mask, image_with_lines],
        grid_shape=(2,2),
        size=(600, 400)
    )

    show_image("All Steps", combined)

if __name__ == "__main__":
    main()
