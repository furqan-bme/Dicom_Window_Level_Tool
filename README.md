

-----

# Interactive DICOM Window/Level Viewer with Histogram

Welcome to my interactive DICOM viewer\! This project is a focused tool designed to help medical imaging enthusiasts,like myself, easily explore individual DICOM images. Beyond just displaying the image, it provides dynamic control over **Window Center (WC)** and **Window Width (WW)**, along with a real-time **histogram** that visually illustrates how these settings impact the displayed intensity range.

I built this as part of my journey in biomedical engineering, specifically to deepen my understanding of DICOM data visualization and the critical role of windowing in medical image analysis. It leverages `pydicom` for robust DICOM parsing and `Matplotlib` for powerful, interactive plotting.

![](WindowLevel.gif)

-----

## Features

  * **Single DICOM Image Loading:** Load and display any valid single-frame DICOM file.
  * **Automatic Rescaling:** Automatically applies `Rescale Slope` and `Rescale Intercept` to convert raw pixel values into meaningful units like Hounsfield Units (HU) for CT scans.
  * **DICOM Window/Level Prioritization:** Initializes window and level settings using values specified within the DICOM tags themselves, providing a clinically relevant starting point. Falls back to sensible defaults if not present.
  * **Interactive Window/Level Sliders:** Dynamically adjust the Window Center and Window Width to enhance the visualization of different tissue types and anatomical structures.
  * **Live Pixel Value Histogram:** Visualizes the distribution of pixel values in the image.
  * **Dynamic Window Rectangle on Histogram:** A red rectangle on the histogram graphically represents the currently applied window and level range, offering immediate feedback on how your adjustments map to the data's intensity distribution.

-----

## Requirements

To run this viewer, you'll need the following Python libraries:

  * `pydicom`
  * `matplotlib`
  * `numpy`

You can install them easily using pip:

```bash
pip install pydicom matplotlib numpy
```

-----

## Getting Started

### 1\. Download the Script

Save the provided code as a Python file (e.g., `dicom_viewer_single.py`).

### 2\. Place Your DICOM File

Ensure you have a DICOM image file ready. Place it in the same directory as the script, or update the `dicom_file_path` variable within the `main()` function to point to its location:

```python
# --- 1. Load DICOM File ---
dicom_file_path = 'path/to/your/dicom/image'  # <--- Update this to your DICOM file path!
```

### 3\. Run the Viewer

Open your terminal or command prompt, navigate to the directory where you saved the script, and execute it:

```bash
python dicom_viewer_single.py
```

-----

## Usage

Once the script runs, a Matplotlib window will appear, split into two main sections:

1.  **DICOM Image (Left Panel):** This displays your medical image. Its appearance will change dynamically as you interact with the sliders.
2.  **Pixel Value Histogram (Right Panel):** This graph shows the distribution of all pixel values in your image.
      * A **red translucent rectangle** on the histogram highlights the range of pixel values currently visible based on your Window Center and Window Width settings. Values outside this rectangle are clipped to black (min) or white (max).

Below the plots, you'll find two interactive sliders:

  * **Window Center:** Move this slider to shift the center of your visible intensity range. This brightens or darkens the image.
  * **Window Width:** Adjust this slider to expand or compress the visible intensity range. A smaller width increases contrast, while a larger width decreases it.

Experiment with these sliders\! You'll quickly see how crucial they are for revealing different anatomical details, whether you're looking for bone structures, soft tissues, or specific pathologies. The histogram will provide instant visual feedback on how your choices affect the data.

-----

## Technical Details

  * **Window/Level Calculation:** The `apply_window_level` function implements the standard formula for windowing, clipping values outside the `[WC - WW/2, WC + WW/2]` range and then normalizing them to `[0, 1]` for display.
  * **Histogram Visualization:** The histogram helps users understand the underlying pixel value distribution, which is key to effectively using window/level. The dynamic rectangle visually connects the slider controls to the data's characteristics.
  * **Error Handling:** Basic error handling for `FileNotFoundError` is included to make initial setup smoother.

-----

## Future Enhancements (Ideas\!)

While this is a complete functional viewer, here are a few ideas for potential future enhancements if you wish to expand upon it:

  * **Zoom/Pan Functionality:** Add interactive zoom and pan for closer inspection.
  * **Overlay Information:** Display relevant DICOM tag information (Patient Name, Modality, etc.) directly on the image or in a separate info panel.
  * **Multiple File Support:** Extend to load and switch between multiple single DICOM images.
  * **Annotation Tools:** Basic tools for drawing lines or points on the image.

-----

## Contribution

If you have any suggestions or find areas for improvement, I'm always open to feedback\! This project is a learning exercise, and collaboration makes it even better.