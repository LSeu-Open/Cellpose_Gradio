import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models, utils
from PIL import Image
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os
import io
import jsonschema

########################################################
# 1. Data and validation functions
########################################################

def load_image(file_path: str) -> tuple[np.ndarray | None, str | None]:
    """
    Load an image file and return it as a numpy array.

    This function attempts to load an image from the specified file path,
    checking for file existence and supported file formats. It returns
    the image as a numpy array if successful, or None with an error message
    if unsuccessful.

    Args:
        file_path (str): The path to the image file to be loaded.

    Returns:
        tuple[np.ndarray | None, str | None]: A tuple containing:
            - The loaded image as a numpy array, or None if loading failed.
            - An error message string if an exception occurred, or None if successful.
    """
    valid_extensions = ['.tif', '.tiff', '.png', '.jpg', '.jpeg']
    
    try:
        # check if the file exists
        if not os.path.exists(file_path):
            gr.Error(f"Image file not found: {file_path}")
            return None, f"Image file not found: {file_path}"
        
        # check if the file extension is supported
        if os.path.splitext(file_path)[1].lower() not in valid_extensions:
            gr.Error("Unsupported file format. Please use TIFF, PNG, or JPEG images.")
            return None, "Unsupported file format. Please use TIFF, PNG, or JPEG images."
        
        # check if the image can be loaded
        image = plt.imread(file_path)
        if image is None:
            gr.Error("Failed to load image")
            return None, "Failed to load image"
        
        return image, None
    except Exception as e:
        gr.Error(str(e))
        return None, str(e)

# Define the set of valid colormaps
VALID_COLORMAPS = {'tab20', 'tab20b', 'tab20c', 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'hsv', 'twilight', 'gray'}

def validate_cmap(cmap):
    """
    Validate the colormap input.
    
    Args:
        cmap (str): The colormap string to validate.
    Returns:
        str: The validated colormap string.
    Raises:
        ValueError: If the colormap is not in the set of valid colormaps.
    """
    if cmap not in VALID_COLORMAPS:
        raise ValueError(f"Invalid colormap. Must be one of: {', '.join(VALID_COLORMAPS)}")
    return cmap

VALID_DISPLAY_CHANNELS = ["RGB", "Grayscale", "Red", "Green", "Blue"]

def validate_display_channel(display_channel):
    """
    Validate the display channel input.

    Args:
        display_channel (str): The display channel string to validate.

    Returns:
        str: The validated display channel string.

    Raises:
        ValueError: If the display channel is not in the set of valid display channels.
    """
    if display_channel not in VALID_DISPLAY_CHANNELS:
        raise ValueError(f"Invalid display channel. Must be one of: {', '.join(VALID_DISPLAY_CHANNELS)}")
    return display_channel

########################################################
# 2. Core processing functions
########################################################

def segment_image(image: np.ndarray, model_type: str, channels: list, diameter: float = None, flow_threshold: float = None) -> np.ndarray:
    """
    Segment cells in an image using the Cellpose model.

    This function applies the Cellpose segmentation algorithm to the input image
    using the specified model type and parameters. It returns a mask array where
    each cell is uniquely labeled.

    Args:
        image (np.ndarray): The input image to be segmented.
        model_type (str): The type of Cellpose model to use (e.g., 'cyto', 'nuclei').
        channels (list): List specifying the channels to use for segmentation.
        diameter (float, optional): The expected diameter of cells in pixels. Defaults to None.
        flow_threshold (float, optional): The flow threshold for cell detection. Defaults to None.

    Returns:
        np.ndarray: A 2D array of the same size as the input image, where each cell
                    is labeled with a unique integer. Background is labeled as 0.

    Raises:
        RuntimeError: If segmentation fails due to invalid input or parameters.
    """
    # load the model
    model = models.Cellpose(model_type=model_type)
    
    try:
        # run the model
        masks, _, _, _ = model.eval(image, channels=channels, diameter=diameter, flow_threshold=flow_threshold)
        
        # return the masks
        return masks
    
    # if the segmentation fails, raise an error
    except Exception as e:
        raise gr.Error(f"Segmentation failed: {str(e)}. Check your input image and parameters.")

def display_results(image: np.ndarray, masks: np.ndarray, display_channel: str, cmap: str = 'tab20b') -> plt.Figure:
    """
    Display the original image and segmentation masks side by side.

    This function creates a figure with three subplots: one for the original image,
    one for the segmentation masks and one for the outlines. The original image can be displayed
    in different modes (RGB, Grayscale, or individual color channels) based on
    the display_channel parameter.

    Args:
        image (np.ndarray): The original input image.
        masks (np.ndarray): The segmentation masks generated by Cellpose.
        display_channel (str): The channel to display for the original image.
            Can be "RGB", "Grayscale", "Red", "Green", or "Blue".
        cmap (str): The colormap to use for displaying the segmentation masks.

    Returns:
        plt.Figure: A matplotlib Figure object containing the three subplots.

    Note:
        The function uses different colormaps for the original image (grayscale
        for single-channel displays) and the segmentation masks (user-specified).
    """
    # create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))
    
    # Display original image
    if display_channel == "RGB":
        ax1.imshow(image)
    elif display_channel == "Grayscale":
        ax1.imshow(np.mean(image, axis=2), cmap='gray')
    elif display_channel in ["Red", "Green", "Blue"]:
        channel_index = {"Red": 0, "Green": 1, "Blue": 2}[display_channel]
        ax1.imshow(image[:,:,channel_index], cmap='gray')
    else:
        ax1.imshow(image)
    ax1.set_title('Original Image')
    ax1.axis('off')
    
    # Display segmentation masks
    ax2.imshow(masks, cmap=cmap)
    ax2.set_title('Segmentation Masks')
    ax2.axis('off')
    ax2.set_facecolor('black')
    
    # display masks outlines
    outlines = utils.masks_to_outlines(masks)
    ax3.imshow(outlines, cmap='gray')
    ax3.set_title('Outlines')
    ax3.axis('off')
    ax3.set_facecolor('black')

    plt.tight_layout()
    return fig

def count_cells(masks: np.ndarray) -> int:
    """
    Count the number of unique cells in a segmentation mask.

    This function takes a 2D numpy array of segmentation masks where each cell
    is labeled with a unique integer, and counts the number of distinct cells.
    It assumes that the background is labeled as 0.

    Args:
        masks (np.ndarray): A 2D numpy array containing segmentation masks.

    Returns:
        int: The number of unique cells in the mask.

    Note:
        This function subtracts 1 from the count to exclude the background,
        which is typically labeled as 0 in the mask.
    """
    return len(np.unique(masks)) - 1

def save_masks(image, masks):
    """
    Save the segmentation masks in various formats.

    This function saves the segmentation masks as NPY, PNG, and outline PNG files.
    It creates a unique filename for each output based on the current timestamp.

    Args:
        image (np.ndarray): The original input image.
        masks (np.ndarray): The segmentation masks generated by Cellpose.

    Returns:
        list: A list of absolute file paths for the saved masks (NPY, PNG, and outline PNG),
              or None if no masks were provided.

    Note:
        - The function creates an 'Outputs' folder if it doesn't exist.
        - The NPY file contains the raw mask data.
        - The PNG file shows the masks with a viridis colormap.
        - The outline PNG file shows the outlines of the masks overlaid on the original image.
    """
    if masks is not None:
        # Create a unique base filename using a formatted timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        base_filename = f"cellpose_{timestamp}"
        
        # Create Outputs folder if it doesn't exist
        output_folder = "Outputs"
        os.makedirs(output_folder, exist_ok=True)

        # Save masks as NPY
        npy_filename = os.path.join(output_folder, f"masks_{base_filename}.npy")
        np.save(npy_filename, masks)
        npy_path = os.path.abspath(npy_filename)

        # Save masks as PNG
        png_filename = os.path.join(output_folder, f"masks_{base_filename}.png")
        plt.figure(figsize=(10, 10))
        plt.imshow(masks, cmap='tab20b')
        plt.axis('off')
        plt.savefig(png_filename, bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()
        png_path = os.path.abspath(png_filename)

        # Save outlines as PNG
        outlines_filename = os.path.join(output_folder, f"outlines_{base_filename}.png")
        overlay = image.copy()
        overlay = utils.masks_to_outlines(masks)
        Image.fromarray(overlay).save(outlines_filename)
        outlines_path = os.path.abspath(outlines_filename)
        
        return [npy_path, png_path, outlines_path]
    return None

########################################################
# 3. Gradio-Display functions
########################################################

def process_and_display(image, model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2, cmap, progress=gr.Progress()):
    """
    Process an input image using Cellpose for cell segmentation and display the results.

    This function performs the following steps:
    1. Checks if an image is provided and converts it to the appropriate format.
    2. Applies Cellpose segmentation using the specified parameters.
    3. Generates a figure displaying the segmentation results.
    4. Counts the number of cells in the segmented image.
    5. Saves the segmentation masks to files.
    6. Saves a high-quality version of the plot as a PNG file.
    7. Saves the plot as an SVG file.

    Args:
        image (numpy.ndarray): Input image for segmentation.
        model_type (str): Type of Cellpose model to use ('cyto3', 'cyto2', or 'nuclei').
        diameter (int): Approximate diameter of cells in pixels.
        flow_threshold (float): Flow threshold for Cellpose segmentation.
        display_channel (str): Channel to display in the output figure.
        seg_channel1 (int): First channel to use for segmentation.
        seg_channel2 (int): Second channel to use for segmentation.
        cmap (str): Colormap to use for displaying the segmentation masks.
        progress (gr.Progress): Gradio progress indicator.

    Returns:
        tuple: Contains the following elements:
            - fig (matplotlib.figure.Figure): Figure object with segmentation results.
            - mask_files (list): Paths to saved mask files and high-quality plot.
            - cell_count (int): Number of cells detected.
            - settings_summary (str): Summary of the settings used for segmentation.
            - gr.update: Gradio update object to hide/show error alerts.
    """
    try:
        if image is not None:
            # Convert grayscale to RGB if necessary
            if image.ndim == 2:
                image = np.stack((image,) * 3, axis=-1)
            elif image.ndim == 3 and image.shape[2] == 4:  # RGBA image
                image = image[:, :, :3]  # Remove alpha channel
            
            # Ensure image is uint8
            image = (image * 255).astype(np.uint8) if image.dtype == np.float64 else image.astype(np.uint8)

            # validate the colormap
            cmap = validate_cmap(cmap)
            
            # validate the display channel
            display_channel = validate_display_channel(display_channel)
            
            # Set channels for segmentation
            progress(0.1, desc="Segmentation starting...")
            channels = [seg_channel1, seg_channel2]
            
            # Segment the image
            progress(0.25, desc="Segmentation in progress...")
            masks = segment_image(image, model_type, channels=channels, diameter=diameter, flow_threshold=flow_threshold)
            progress(0.75, desc="Segmentation complete. Generating results...")
            
            # Display the results
            fig = display_results(image, masks, display_channel=display_channel, cmap=cmap)
            cell_count = count_cells(masks)
            mask_files = save_masks(image, masks)
            
            # Save the figure as a high-quality PNG
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            buf.seek(0)

            # Save the plot to a file.png
            plot_filename = os.path.join("Outputs", f"Result_figure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            with open(plot_filename, 'wb') as f:
                f.write(buf.getvalue())
            
            # Add the PNG plot to mask_files
            mask_files.append(plot_filename)

            # Save the figure as an SVG
            svg_buf = io.BytesIO()
            fig.savefig(svg_buf, format='svg', bbox_inches='tight')
            svg_buf.seek(0)

            # Save the plot as an SVG
            svg_filename = os.path.join("Outputs", f"Result_figure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.svg")
            with open(svg_filename, 'wb') as f:
                f.write(svg_buf.getvalue())

            # Add the SVG plot to mask_files
            mask_files.append(svg_filename)
            
            progress(1.0, desc="Process complete!")
            settings_summary = f"Model: {model_type}, Diameter: {diameter}, Flow Threshold: {flow_threshold}, Display: {display_channel}, Seg Ch1: {seg_channel1}, Seg Ch2: {seg_channel2}, Colormap: {cmap}"
            return fig, mask_files, cell_count, settings_summary, gr.update(visible=False)
        
        # if no image is provided, show an error message
        gr.Error("No image provided.")
        return None, None, None, None, gr.update(visible=True)
    
    # if an error occurs, show an error message
    except Exception as e:
        gr.Error(str(e))
        return None, None, None, None, gr.update(visible=True)

def update_channel_visibility(channel_config):
    """
    Update the visibility of segmentation channels based on the selected configuration.

    This function takes a channel configuration string and returns visibility updates
    for two segmentation channels. If the configuration is "own channels", both channels
    are made visible. Otherwise, both channels are hidden.

    Args:
        channel_config (str): The channel configuration string. Expected values are "own channels" or other.

    Returns:
        tuple: A tuple containing two gr.update objects to set the visibility of the segmentation channels.
    """

    # if the channel configuration is "own channels", make both channels visible
    if channel_config == "own channels":
        return gr.update(visible=True), gr.update(visible=True)
    
    # otherwise, make both channels invisible
    else:
        return gr.update(visible=False), gr.update(visible=False)

########################################################
# 4. Profile functions
########################################################

def save_settings(profile_name, model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2, cmap):
    """
    Save the current settings to a JSON file with a specific profile name and refresh the profile list.
    """
    # Create a dictionary with the provided settings
    settings = {
        "model_type": model_type,
        "diameter": diameter,
        "flow_threshold": flow_threshold,
        "display_channel": display_channel,
        "seg_channel1": seg_channel1,
        "seg_channel2": seg_channel2,
        "cmap": cmap
    }
    
    # Create a 'profiles' directory if it doesn't exist
    profiles_dir = "profiles"
    os.makedirs(profiles_dir, exist_ok=True)
    
    # Ensure the profile name is safe to use as a filename
    safe_profile_name = secure_filename(profile_name)
    if not safe_profile_name:
        raise gr.Error("Invalid profile name")
    
    # Construct the full path
    full_path = os.path.join(profiles_dir, f"{safe_profile_name}.json")
    
    # Save the settings to a JSON file named after the profile
    with open(full_path, "w") as f:
        json.dump(settings, f)
    
    gr.Info(f"Settings saved successfully as profile: {profile_name}")
    
    # Return the updated list of profiles
    return gr.update(choices=list_profiles(), value=safe_profile_name)

def list_profiles():
    """
    List all available profiles in the 'profiles' directory.
    """
    # get the base path
    base_path = "profiles"
    
    # if the base path does not exist, return an empty list
    if not os.path.exists(base_path):
        return []
    
    # get the list of files in the base path
    return [f.split('.')[0] for f in os.listdir(base_path) if f.endswith('.json')]

# Define the JSON schema for validation
settings_schema = {
    "type": "object",
    "properties": {
        "model_type": {"type": "string", "enum": ["cyto3", "cyto2", "cyto", "nuclei"]},
        "diameter": {"type": "number", "minimum": 1, "maximum": 100},
        "flow_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "display_channel": {"type": "string", "enum": ["RGB", "Grayscale", "Red", "Green", "Blue"]},
        "seg_channel1": {"type": "integer", "minimum": 0, "maximum": 3},
        "seg_channel2": {"type": "integer", "minimum": 0, "maximum": 3},
        "cmap": {"type": "string"}
    },
    "required": ["model_type", "diameter", "flow_threshold", "display_channel", "seg_channel1", "seg_channel2", "cmap"]
}

def load_settings(profile_name):
    """
    Load settings from a specific profile JSON file with validation.
    """
    file_path = f"profiles/{profile_name}.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                settings = json.load(f)
                
                # Validate the loaded JSON against our schema
                jsonschema.validate(instance=settings, schema=settings_schema)
                
                # Additional custom validation if needed
                if settings["cmap"] not in ['tab20', 'tab20b', 'tab20c', 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'hsv', 'twilight', 'gray']:
                    raise ValueError("Invalid colormap")
                
                gr.Info(f"Settings loaded successfully from profile: {profile_name}")
                return (settings["model_type"], settings["diameter"], settings["flow_threshold"], 
                        settings["display_channel"], settings["seg_channel1"], settings["seg_channel2"], 
                        settings["cmap"])
            except json.JSONDecodeError:
                gr.Warning(f"Invalid JSON in profile: {profile_name}")
            except jsonschema.exceptions.ValidationError as ve:
                gr.Warning(f"Invalid settings in profile: {profile_name}. Error: {ve}")
            except ValueError as ve:
                gr.Warning(f"Invalid settings in profile: {profile_name}. Error: {ve}")
    else:
        gr.Warning(f"Profile '{profile_name}' not found.")
    
    return [gr.update()] * 7

########################################################
# 5. UI setup
########################################################

# Custom CSS styles for the Gradio interface
custom_css = """
.gradio-container {
    max-width: 1200px !important;
    font-family: Arial, sans-serif;
    font-size: 14px;
}
.output-image, .input-image {
    height: 600px !important;
}
.center {
    text-align: center;
}
.app-header {
    font-family: Arial, sans-serif;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    background-color: #f9fafb;
    border-bottom: 1px solid #ffcc99;
}
.app-header h1 {
    font-size: 28px;
    color: #ff6600;
    margin-bottom: 10px;
}
.app-header p {
    font-size: 16px;
    color: #f5830b;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}
.app-footer {
    font-family: Arial, sans-serif;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    background-color: #f9fafb;
    border-top: 1px solid #ffcc99;
    margin-top: 30px;
}
.app-footer p {
    font-size: 16px;
    color: #f5830b;
    max-width: 800px;
    margin: 10px auto;
    text-align: center;
}
.custom-component {
    font-weight: bold;
}
.custom-component:hover {
    background-color: #fdedd6;
    color: white;
}
.custom-button {
    color: #f5830b !important;
    border-color: #ff9933 !important;
    background-color: white !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}
.custom-button:hover {
    color: white !important;
    background-color: #ff9933 !important;
}
.custom-button:active {
    color: white !important;
    background-color: #5ce65c !important;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}
.custom-dropdown {
    font-weight: bold;
    font-size: 10px;
}
.custom-dropdown:hover {
    background-color: #fdedd6;
    color: white;
}
.custom-slider {
    font-weight: bold;
    font-size: 10px;
}
.custom-slider:hover {
    background-color: #fdedd6;
    color: white;
}
.custom-settings-summary {
    font-weight: bold;
    font-size: 10px;
}
.custom-settings-summary textarea {
    font-weight: bold !important;
    font-size: 10px !important;
}
.custom-settings-summary:hover {
    background-color: #fdedd6;
    color: white;
}
"""

# set a custom theme for the app
custom_theme = gr.themes.Soft(primary_hue="orange", secondary_hue="orange", font=["Arial", "sans-serif"])

########################################################
# 6. Gradio interface
########################################################

with gr.Blocks(css=custom_css, theme=custom_theme) as iface:
    
    # Title and description
    with gr.Row(elem_classes=["app-header"]):
        gr.Markdown("# Cellpose Gradio")
        gr.Markdown("A user-friendly interface for cell segmentation powered by Cellpose and built with Gradio.")
        gr.Markdown("This application provides a user-friendly interface for cell segmentation tasks. <br> For more advanced functionalities, users may prefer the comprehensive Cellpose GUI.")
        gr.Markdown("Please refer to the **[Cellpose documentation](https://cellpose.readthedocs.io/en/latest/)** for more information on specific parameters.")
    
    # Input image
    with gr.Row():
        input_image = gr.Image(label="Input Image - Supported formats include TIFF, PNG, and JPEG. - TIFF images preview is not supported.", type="numpy", height=400, width=400, visible=True)

    # Save and load settings
    with gr.Row():
        with gr.Column(scale=1):
            profile_name = gr.Textbox(label="Save Profile", placeholder="Enter profile name", info="Name your profile to **save the current settings**.", elem_classes=["custom-component"])
            save_btn = gr.Button("Save Profile", scale=1, size="sm", elem_classes=["custom-button"])
        with gr.Column(scale=1):
            profiles = list_profiles()
            default_value = profiles[0] if profiles else None
            load_profile = gr.Dropdown(label="Load Profile", choices=profiles, scale=1, info="Select a profile to **load its settings**.", value=default_value, allow_custom_value=True, elem_classes=["custom-dropdown"])
            load_btn = gr.Button("Load Profile", scale=1, size="sm", elem_classes=["custom-button"])    
    
    # Model type, diameter, flow threshold
    with gr.Row():
        model_type = gr.Dropdown(
            choices=['cyto3', 'cyto2', 'cyto', 'nuclei'],
            label="Segmentation model",
            value='cyto3', scale=1, 
            info="**Choose the model used for segmentation.** <br> ***cyto<cyto2<cyto3***: generalist models for cells (channel 1 is cells color and channel 2 is nuclei color). <br> ***nuclei***: specialized for nucleus segmentation (channel 1 is nuclei color and set channel 2 to 0).",
            elem_classes=["custom-dropdown"]
        )
        diameter = gr.Slider(
            minimum=1, maximum=100, 
            step=1,label="Diameter", 
            value=30, scale=1, 
            info="**Set the expected diameter of cells in pixels.** <br> When the diameter is set smaller than the true size then cellpose may over-split cells. If the diameter is set too big then cellpose may over-merge cells.", 
            elem_classes=["custom-slider"]
        )
        flow_threshold = gr.Slider(
            minimum=0.0, maximum=1.0, step=0.01,
            label="Flow Threshold", 
            value=0.4, scale=1, 
            info="**Adjust the flow threshold.** <br> Increase it if cellpose is not returning as many ROIs as you’d expect. Decrease it if cellpose is returning too many ill-shaped ROIs.", 
            elem_classes=["custom-slider"]
        )
    

    # Display channel, segmentation channels, and color palette
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Group():
                display_channel = gr.Dropdown(
                choices=list(VALID_DISPLAY_CHANNELS),
                label="Display Mode",
                    value="RGB",
                    info="Select the channel used to display the original image **in the segmentation result**.",
                    elem_classes=["custom-dropdown"]
                )
                cmap = gr.Dropdown(
                choices=list(VALID_COLORMAPS),
                label="Masks Color Palette",
                value='tab20b',
                info="Select the color palette used to **color cells in the segmentation result.**",
                elem_classes=["custom-dropdown"]
            )
        with gr.Column(scale=2):
            with gr.Group():
                seg_channel1 = gr.Dropdown(
                    choices=[0, 1, 2, 3],
                    label="Segmentation Channel 1",
                    value=0,
                    info="**0=grayscale, 1=red, 2=green, 3=blue**",
                    elem_classes=["custom-dropdown"]
                )
                seg_channel2 = gr.Dropdown(
                    choices=[0, 1, 2, 3],
                    label="Segmentation Channel 2",
                    value=0,
                    info="**0=None (will set to zero), 1=red, 2=green, 3=blue**",
                    elem_classes=["custom-dropdown"]
                )
    
    process_btn = gr.Button("Run Segmentation", scale=2, elem_classes=["custom-button"])
    progress_output = gr.Textbox(label="Progress", interactive=False, visible=True)
    
    # Output components (initially hidden)
    with gr.Row(visible=False) as output_row:
        output_plot = gr.Plot(label="Segmentation Results")
        
    with gr.Row(visible=False) as results_row:
        with gr.Column(scale=1):
            cell_count_output = gr.Number(label="Number of cells detected", elem_classes=["custom-component"])
            settings_output = gr.Textbox(label="Settings Summary", elem_classes=["custom-settings-summary"])
        with gr.Column(scale=2):
            output_files = gr.File(label="Download Results", file_count="multiple", scale=1, height=500, elem_classes=["custom-component"])

    #### function and buttons logic to make the app work

    # Update the process_and_display_wrapper function
    def process_and_display_wrapper(*args):
        results = process_and_display(*args)
        return [gr.update(visible=True), gr.update(visible=True)] + list(results)

    # Run segmentation button
    process_btn.click(
        fn=process_and_display_wrapper,
        inputs=[input_image, model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2, cmap],
        outputs=[output_row, results_row, output_plot, output_files, cell_count_output, settings_output, progress_output],
    )

    # Save settings button
    save_btn.click(
        save_settings,
        inputs=[profile_name, model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2, cmap],
        outputs=[load_profile]  # Update the load_profile dropdown
    )

    # Load settings button
    load_btn.click(
        load_settings,
        inputs=[load_profile],
        outputs=[model_type, diameter, flow_threshold, display_channel, seg_channel1, seg_channel2, cmap]
    )

    # Footer
    with gr.Row(elem_classes=["app-footer"]):
        gr.Markdown("This application utilizes Cellpose, a tool designed for cell segmentation in microscopy images. <br> For additional information, please refer to the [Cellpose Github repository](https://github.com/Cellpose/Cellpose).")
        gr.Markdown("If you use this application for your research, please consider citing the [original Cellpose 1.0 paper](https://www.nature.com/articles/s41592-020-01018-x) and the [Cellpose3 paper](https://www.biorxiv.org/content/10.1101/2024.02.10.579780v1).")
        gr.Markdown("For any issues or feedback regarding this application, please submit an issue on the [Cellpose-gradio Github repository](https://github.com/LSeu-Open/cellpose-gradio).")

########################################################
# 6. Launch the interface
########################################################

if __name__ == "__main__":
    iface.launch()
