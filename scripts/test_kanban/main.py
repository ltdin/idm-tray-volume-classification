from kanban_utils.image_io import read_image, show_image
from kanban_utils.preprocessing import enhance_clahe
from kanban_utils.segmentation import create_blue_mask
from kanban_utils.contour_selection import find_largest_contour_polygon, draw_polygon
from kanban_utils.utils import combine_images
from kanban_utils.line_detection import detect_lines, draw_lines

def main():
    path = "../../DSC01307.jpg"
    focus_bottom_only = True  # Toggle this to limit mask to bottom half only

    # Read image
    image = read_image(path)

    # Apply CLAHE
    image_enhanced = enhance_clahe(image)

    # Create blue tape mask
    mask = create_blue_mask(image_enhanced)

    if focus_bottom_only:
        # Zero out the top half of the mask
        h, w = mask.shape
        mask[:h // 2, :] = 0

    # Find contour polygon
    polygon, approx_pts = find_largest_contour_polygon(mask)

    if polygon is not None:
        image_with_poly = draw_polygon(image_enhanced, polygon)
    else:
        image_with_poly = image_enhanced.copy()

    # Find lines using Hough Transform
    lines = detect_lines(mask)
    image_with_lines = draw_lines(image_enhanced, lines)

    # Combine all 4 images to view at once
    combined = combine_images(
        [image, image_enhanced, mask, image_with_lines],
        grid_shape=(2,2),
        size=(600, 400)
    )

    show_image("All Steps", combined)

if __name__ == "__main__":
    main()
