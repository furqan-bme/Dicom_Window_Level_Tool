import pydicom
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.widgets as widgets
from matplotlib.patches import Rectangle

def apply_window_level(image_data, window_center, window_width):
    """
    Applies window and level to DICOM pixel data for display.

    Args:
        image_data (np.array): The raw pixel array (e.g., in Hounsfield Units for CT).
        window_center (float): The window center value.
        window_width (float): The window width value.

    Returns:
        np.array: The processed image data normalized to a 0-1 range,
                  suitable for display.
    """
    min_val = window_center - window_width / 2
    max_val = window_center + window_width / 2

    # Clip pixel values to the defined window range
    display_image = np.clip(image_data, min_val, max_val)

    # Normalize the clipped values to a 0-1 range for proper visualization
    # Avoid division by zero if window_width is 0
    if window_width == 0:
        display_image = np.zeros_like(display_image)
    else:
        display_image = (display_image - min_val) / (max_val - min_val)

    return display_image

def main():
    """
    Main function to load a DICOM file, apply window/level, and display it
    with an interactive viewer including a histogram and sliders.
    """
    # --- 1. Load DICOM File ---
    dicom_file_path = 'path/to/your/dicom/image'  # Specify the path to your DICOM file
    try:
        ds = pydicom.dcmread(dicom_file_path)
        print(f"Successfully loaded DICOM file: {dicom_file_path}")
    except FileNotFoundError:
        print(f"Error: DICOM file not found at {dicom_file_path}")
        return
    except Exception as e:
        print(f"Error loading DICOM file: {e}")
        return

    # --- 2. Extract Pixel Data and Apply Rescaling (if present) ---
    pixel_array = ds.pixel_array

    # Check for and apply Rescale Slope and Intercept. These are crucial
    # for converting raw pixel values to meaningful units like Hounsfield Units (HU)
    # in CT scans.
    if 'RescaleIntercept' in ds and 'RescaleSlope' in ds:
        rescale_intercept = ds.RescaleIntercept
        rescale_slope = ds.RescaleSlope
        pixel_array = pixel_array * rescale_slope + rescale_intercept
        print(f"Applied Rescale Slope ({rescale_slope}) and Rescale Intercept ({rescale_intercept}). "
              "Pixel values are now likely in Hounsfield Units (HU).")
    else:
        print("No Rescale Slope or Intercept found. Using raw pixel values.")

    # --- 3. Determine Initial Window/Level Settings ---
    # Prioritize DICOM-specified Window Center and Window Width values.
    # These often provide clinically relevant views of the image data.
    # Handle MultiValue DICOM tags by taking the first value.
    if 'WindowCenter' in ds and 'WindowWidth' in ds:
        initial_window_center = ds.WindowCenter[0] if isinstance(ds.WindowCenter, pydicom.multival.MultiValue) else ds.WindowCenter
        initial_window_width = ds.WindowWidth[0] if isinstance(ds.WindowWidth, pydicom.multival.MultiValue) else ds.WindowWidth
        print(f"Using DICOM-specified Window Center: {initial_window_center:.0f}, Window Width: {initial_window_width:.0f}")
    else:
        # Provide sensible default values if DICOM tags are missing.
        # These defaults are typical for a general CT abdomen window.
        initial_window_center = 40.0
        initial_window_width = 400.0
        print(f"DICOM WindowCenter/Width not found. Using default values: "
              f"Center={initial_window_center:.0f}, Width={initial_window_width:.0f}")

    # Initialize current window/level values
    current_window_center = initial_window_center
    current_window_width = initial_window_width

    # --- 4. Setup Matplotlib Plot ---
    # Create a figure and a set of subplots.
    # One subplot for the DICOM image and another for its histogram.
    figure_name = "DICOM Interactive Viewer"
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), num=figure_name)
    ax_image = axes[0]
    ax_hist = axes[1]

    # Adjust the bottom margin to allocate space for the interactive sliders.
    # This prevents sliders from overlapping with the plots.
    fig.subplots_adjust(bottom=0.25)

    # Display the initial DICOM image with the determined window/level settings.
    im = ax_image.imshow(apply_window_level(pixel_array, current_window_center, current_window_width), cmap='gray')
    ax_image.set_title(f"DICOM Image\nWC: {current_window_center:.0f}, WW: {current_window_width:.0f}")
    ax_image.axis('off')  # Hide axes ticks and labels for a cleaner image display.

    # Plot the histogram of pixel values.
    n_bins = 256  # Number of bins for the histogram
    hist_values, bin_edges = np.histogram(pixel_array.flatten(), bins=n_bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    ax_hist.plot(bin_centers, hist_values, color='blue', linewidth=1.5)
    ax_hist.set_title("Pixel Value Histogram")
    ax_hist.set_xlabel("Pixel Value (HU if applicable)")
    ax_hist.set_ylabel("Frequency")
    ax_hist.grid(True, linestyle='--', alpha=0.7)
    ax_hist.set_facecolor('#f5f5f5') # Light grey background for the histogram

    # Add a visual indicator (rectangle) on the histogram to show the current
    # window and level range.
    window_rect = Rectangle((current_window_center - current_window_width / 2, 0),
                            current_window_width, ax_hist.get_ylim()[1],
                            facecolor='red', alpha=0.3, edgecolor='red', linewidth=1, linestyle='--')
    ax_hist.add_patch(window_rect)

    # --- 5. Create Interactive Sliders ---
    # Define the color for the slider backgrounds.
    axcolor = '#f0f0f0'  # A light grey for a professional look

    # Define positions for the window center and window width sliders.
    # The format is [left, bottom, width, height] as fractions of the figure width/height.
    # These coordinates are relative to the figure, not the subplots.
    ax_wc = plt.axes([0.15, 0.12, 0.65, 0.03], facecolor=axcolor) # Window Center slider position
    ax_ww = plt.axes([0.15, 0.07, 0.65, 0.03], facecolor=axcolor) # Window Width slider position

    # Determine the range for the sliders based on the actual pixel value range
    # to provide a meaningful and explorable range.
    min_pixel_val = pixel_array.min()
    max_pixel_val = pixel_array.max()

    # Create the Window Center slider.
    # The slider range is extended beyond min/max pixel values to allow for
    # exploration of different tissue types.
    wc_slider = widgets.Slider(ax_wc, 'Window Center',
                               min_pixel_val - (max_pixel_val - min_pixel_val) * 0.5,
                               max_pixel_val + (max_pixel_val - min_pixel_val) * 0.5,
                               valinit=initial_window_center, valfmt="%0.0f")

    # Create the Window Width slider.
    # The minimum width is set to 1 to prevent division by zero in apply_window_level.
    ww_slider = widgets.Slider(ax_ww, 'Window Width',
                               1,  # Minimum width to avoid division by zero
                               (max_pixel_val - min_pixel_val) * 2, # Max width can be larger than data range
                               valinit=initial_window_width, valfmt="%0.0f")

    # --- 6. Define Update Function for Sliders ---
    def update(val):
        """
        This function is called whenever a slider's value is changed.
        It updates the displayed image and the histogram's window rectangle.
        """
        # Retrieve the current values from the sliders.
        new_window_center = wc_slider.val
        new_window_width = ww_slider.val

        # Update the image data with the new window/level settings.
        im.set_data(apply_window_level(pixel_array, new_window_center, new_window_width))
        # Update the image title to reflect the current window/level.
        ax_image.set_title(f"DICOM Image\nWC: {new_window_center:.0f}, WW: {new_window_width:.0f}")

        # Update the position and width of the rectangle on the histogram
        # to match the new window/level.
        window_rect.set_x(new_window_center - new_window_width / 2)
        window_rect.set_width(new_window_width)

        # Redraw the canvas to reflect the changes.
        fig.canvas.draw_idle()

    # Register the update function to be called when slider values change.
    wc_slider.on_changed(update)
    ww_slider.on_changed(update)

    # --- 7. Display the Plot ---
    plt.show()

if __name__ == "__main__":
    main()