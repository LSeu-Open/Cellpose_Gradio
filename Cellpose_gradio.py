import gradio as gr
import numpy as np
import os
from cellpose import models, utils
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime

# Your existing functions
def load_image(file_path: str) -> np.ndarray:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {file_path}")
    
    valid_extensions = ['.tif', '.tiff', '.png', '.jpg', '.jpeg']
    if os.path.splitext(file_path)[1].lower() not in valid_extensions:
        raise ValueError("Unsupported file format. Please use TIFF, PNG, or JPEG images.")
    
    try:
        image = plt.imread(file_path)
        if image is None:
            raise IOError("Failed to load image")
        return image
    except Exception as e:
        raise IOError(f"Error loading image: {str(e)}")

def segment_image(image: np.ndarray, model_type: str, channels: list, diameter: float = None, flow_threshold: float = None) -> np.ndarray:
    model = models.Cellpose(model_type=model_type)
    
    try:
        masks, _, _, _ = model.eval(image, channels=channels, diameter=diameter, flow_threshold=flow_threshold)
        return masks
    except Exception as e:
        raise RuntimeError(f"Segmentation failed: {str(e)}. Check your input image and parameters.")

def count_cells(masks: np.ndarray) -> int:
    return len(np.unique(masks)) - 1  # Subtract 1 to exclude the background (usually labeled as 0)

def display_results(image: np.ndarray, masks: np.ndarray, display_channel: str) -> plt.Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Display original image
    if display_channel == "RGB":
        ax1.imshow(image)
    elif display_channel == "Grayscale":
        ax1.imshow(image, cmap='gray')
    elif display_channel == "Inverted":
        ax1.imshow(np.invert(image), cmap='gray')
    elif isinstance(display_channel, int) and image.ndim == 3:
        ax1.imshow(image[:,:,display_channel])
    else:
        ax1.imshow(image)
    ax1.set_title('Original Image')
    ax1.axis('off')
    
    # Display segmentation masks
    ax2.imshow(masks, cmap='tab20b')
    ax2.set_title('Segmentation Masks')
    ax2.axis('off')
    
    plt.tight_layout()
    return fig

def save_masks(image, masks):
    if masks is not None:
        # Create a unique base filename using a formatted timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        base_filename = f"cellpose_output_{timestamp}"
        
        # Save masks as NPY
        # Create Outputs folder if it doesn't exist
        output_folder = "Outputs"
        os.makedirs(output_folder, exist_ok=True)

        # Save masks as NPY
        npy_filename = os.path.join(output_folder, f"{base_filename}_masks.npy")
        np.save(npy_filename, masks)
        npy_path = os.path.abspath(npy_filename)

        # Save masks as PNG
        png_filename = os.path.join(output_folder, f"{base_filename}_masks.png")
        plt.imshow(masks, cmap='tab20b')
        plt.axis('off')
        plt.savefig(png_filename, bbox_inches='tight', pad_inches=0)
        plt.close()
        png_path = os.path.abspath(png_filename)

        # Save outlines as PNG
        outlines_filename = os.path.join(output_folder, f"{base_filename}_outlines.png")
        overlay = image.copy()
        overlay = utils.masks_to_outlines(masks)
        Image.fromarray(overlay).save(outlines_filename)
        outlines_path = os.path.abspath(outlines_filename)

        return [npy_path, png_path, outlines_path]
    return None

# Gradio interface function
def process_image(image, model_type, diameter):
    # Convert grayscale to RGB if necessary
    if image.ndim == 2:
        image = np.stack((image,) * 3, axis=-1)
    
    masks = segment_image(image, model_type, channels=[0, 0], diameter=diameter)
    fig = display_results(image, masks, display_channel="RGB")
    return fig, masks

# Create Gradio interface
def display_input_image(image):
    if image is not None:
        return image
    return None

def process_and_display(image, model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2):
    if image is not None:
        # Convert grayscale to RGB if necessary
        if image.ndim == 2:
            image = np.stack((image,) * 3, axis=-1)
        elif image.ndim == 3 and image.shape[2] == 4:  # RGBA image
            image = image[:, :, :3]  # Remove alpha channel
        
        # Ensure image is uint8
        image = (image * 255).astype(np.uint8) if image.dtype == np.float64 else image.astype(np.uint8)
        
        # Set channels for segmentation
        channels = [seg_channel1, seg_channel2]
        
        masks = segment_image(image, model_type, channels=channels, diameter=diameter, flow_threshold=flow_threshold)
        fig = display_results(image, masks, display_channel=display_channel)
        cell_count = count_cells(masks)
        mask_files = save_masks(image, masks)
        
        return fig, mask_files, cell_count
    return None, None, None

def update_channel_visibility(channel_config):
    if channel_config == "own channels":
        return gr.update(visible=True), gr.update(visible=True)
    else:
        return gr.update(visible=False), gr.update(visible=False)

# Custom CSS to increase font size and overall UI size
custom_css = """
body, .gradio-container {
    font-size: 18px;
}
.gradio-container {
    max-width: 1200px !important;
}
.output-image, .input-image {
    height: 600px !important;
}
"""

with gr.Blocks(css=custom_css) as iface:
    gr.Markdown("# Cellpose Segmentation", elem_classes=["center"])
    gr.Markdown("Upload an image to segment using Cellpose. Choose the model type, channel configuration, and specify the parameters. The output will be a PNG image of the segmentation masks, a NPY file of the masks, and a PNG image of the outlines.")
    gr.Markdown("This app is designed to simplify the process of segmenting single images using the Cellpose models. For more complex needs, please use the Cellpose GUI.")
    
    with gr.Row():
        input_image = gr.Image(label="Input Image", type="numpy", height=150, width=150)
        
    with gr.Row():
        model_type = gr.Dropdown(choices=['cyto3', 'cyto2', 'nuclei'], label="Choose segmentation model", value='cyto3', scale=1, info="cyto models are trained on two-channel images")
        diameter = gr.Slider(minimum=1, maximum=100, step=1, label="Diameter", value=30, scale=1, info="When the input diameters are undersized, CellPose may split cells unnecessarily; when oversized, it may merge overlapping objects.")
        flow_threshold = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label="Flow Threshold", value=0.4, scale=1, info="Increase it if CellPose returns fewer ROIs than expected or if they are well-defined shapes; decrease it if it returns more poorly defined ROIs.")
    
    with gr.Row():
        display_channel = gr.Dropdown(choices=["RGB", "Grayscale", "Inverted"], label="Display Channel", value="RGB", scale=1)
        seg_channel1 = gr.Dropdown(choices=[0, 1, 2, 3], label="Segmentation Channel 1", value=0, visible=True, info="0=grayscale, 1=red, 2=green, 3=blue", scale=1)
        seg_channel2 = gr.Dropdown(choices=[0, 1, 2, 3], label="Segmentation Channel 2", value=0, visible=True, info="0=None (will set to zero), 1=red, 2=green, 3=blue", scale=1)
    
    output_plot = gr.Plot(label="Segmentation Results")
    
    with gr.Row():
        cell_count_output = gr.Number(label="Cell Count", scale=1)
        output_files = gr.File(label="Download Results (date is in the filename formatted as YYYY-MM-DD_HH-MM)", file_count="multiple", scale=1)
    
    process_btn = gr.Button("Process", scale=2)
    
    process_btn.click(
        fn=process_and_display,
        inputs=[input_image, model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2],
        outputs=[output_plot, output_files, cell_count_output]
    )

    gr.Markdown("This app is based on Cellpose, a software for cell segmentation in microscopy images. For more information, see the [Cellpose Github repository](https://github.com/Cellpose/Cellpose).")
    gr.Markdown("If you find this app useful, please cite the [Cellpose3 paper](https://www.biorxiv.org/content/10.1101/2024.02.10.579780v1).")
    gr.Markdown("If you have any issues or feedback, please open an issue on the [Github Cellpose-gradio repository](https://github.com/LSeu-Open/cellpose-gradio).")

# Launch the interface
if __name__ == "__main__":
    iface.launch()
