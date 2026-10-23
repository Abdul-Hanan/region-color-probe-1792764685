# region-color-probe

Identifies the most frequent exact BGR color within a programmatically defined image region.

## Description

This project loads a synthetic image, defines a rectangular region of interest (ROI) via hardcoded coordinates (simulating a user's click-and-drag), and then calculates the single most frequent exact BGR color within that region. The process is entirely headless; all visual outputs are saved as image files to an `output/` directory, rather than displayed in a GUI.

## Requirements

Ensure you have Python 3.7+ installed.

## Installation

1. Clone this repository (or copy `main.py` and the other files).
2. Navigate to the project directory.
3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the project:

```bash
python main.py
```

The script will:
1. Generate a sample image and save it as `output/original_sample_image.png`.
2. Define a rectangular ROI (currently hardcoded within `main.py`).
3. Draw the defined ROI on a copy of the original image and save it as `output/output_image_with_roi.png`.
4. Identify the most frequent exact BGR color within that ROI.
5. Print the dominant BGR color to the console.
6. Create a 100x100 pixel swatch of the dominant color and save it as `output/dominant_color_swatch.png`.

All operations are performed without opening any graphical windows, making it suitable for headless server environments.