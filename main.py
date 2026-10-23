import numpy as np
import cv2
import os

def generate_sample_image(width=400, height=300):
    """
    Generates a synthetic image with distinct color regions for testing.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Background color (Dark Grey)
    img[:] = [30, 30, 30]

    # Large Blue square
    cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), -1) # BGR: Blue

    # Medium Red square
    cv2.rectangle(img, (220, 100), (350, 250), (0, 0, 255), -1) # BGR: Red

    # Vertical Yellow stripe
    cv2.rectangle(img, (100, 20), (150, 280), (0, 255, 255), -1) # BGR: Yellow

    # Scattered Green pixels (less dominant)
    for _ in range(500):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        img[y, x] = [0, 255, 0] # BGR: Green

    return img

def main():
    print("Starting region-color-probe...")

    # Define output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output files will be saved in: {os.path.abspath(output_dir)}")

    # 1. Generate a synthetic image
    image = generate_sample_image()
    original_image_path = os.path.join(output_dir, "original_sample_image.png")
    cv2.imwrite(original_image_path, image)
    print(f"Generated sample image: {original_image_path}")

    # 2. Define a rectangular Region of Interest (ROI)
    # These coordinates simulate a user clicking and dragging.
    # Format: (x_top_left, y_top_left, x_bottom_right, y_bottom_right)
    # This specific ROI should have Blue as the dominant color.
    roi_x1, roi_y1 = 80, 40
    roi_x2, roi_y2 = 180, 220
    print(f"Defined ROI: Top-left ({roi_x1}, {roi_y1}), Bottom-right ({roi_x2}, {roi_y2})")

    # Ensure ROI is within image bounds
    h, w, _ = image.shape
    roi_x1 = max(0, roi_x1)
    roi_y1 = max(0, roi_y1)
    roi_x2 = min(w, roi_x2)
    roi_y2 = min(h, roi_y2)

    # Validate ROI dimensions
    if roi_x1 >= roi_x2 or roi_y1 >= roi_y2:
        print(f"Warning: Invalid or empty ROI selected: ({roi_x1},{roi_y1}) to ({roi_x2},{roi_y2}). Exiting.")
        return

    # Create a copy of the image to draw the ROI on
    image_with_roi = image.copy()
    # Draw the rectangle on the image (Green border, 2 pixels thick)
    cv2.rectangle(image_with_roi, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
    output_with_roi_path = os.path.join(output_dir, "output_image_with_roi.png")
    cv2.imwrite(output_with_roi_path, image_with_roi)
    print(f"Saved image with ROI marked: {output_with_roi_path}")

    # 3. Extract pixels within the ROI
    roi_pixels_img = image[roi_y1:roi_y2, roi_x1:roi_x2]

    # Reshape the ROI image to a 1D array of pixels, where each pixel is a [B, G, R] array
    # Check if the ROI is empty after cropping
    if roi_pixels_img.size == 0:
        print("Error: Extracted ROI is empty. Cannot determine dominant color.")
        return

    reshaped_pixels = roi_pixels_img.reshape(-1, 3) # -1 infers the number of rows (pixels)

    # 4. Identify the single most frequent exact BGR color
    # np.unique with axis=0 treats each row (BGR triplet) as a unique item
    unique_colors, counts = np.unique(reshaped_pixels, axis=0, return_counts=True)

    if len(unique_colors) == 0:
        print("No unique colors found in the ROI. This should not happen for a non-empty ROI.")
        return

    # Find the index corresponding to the highest count
    max_count_idx = np.argmax(counts)
    dominant_bgr_color = unique_colors[max_count_idx]

    print(f"\nDominant BGR color in the ROI: {dominant_bgr_color} (B={dominant_bgr_color[0]}, G={dominant_bgr_color[1]}, R={dominant_bgr_color[2]})")

    # 5. Create and save a color swatch for the dominant color
    swatch_size = 100
    color_swatch = np.full((swatch_size, swatch_size, 3), dominant_bgr_color, dtype=np.uint8)
    output_swatch_path = os.path.join(output_dir, "dominant_color_swatch.png")
    cv2.imwrite(output_swatch_path, color_swatch)
    print(f"Saved dominant color swatch: {output_swatch_path}")

    print("\nRegion-color-probe finished successfully.")

if __name__ == "__main__":
    main()