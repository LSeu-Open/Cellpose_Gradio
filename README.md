
# Cellpose-Gradio

The Cellpose-Gradio App is a modern looking **user-friendly interface** ported from the popular Cellpose library, making its powerful cell segmentation capabilities **accessible to non-experts**. 

By wrapping the complexity of Cellpose within **a Gradio app**, users without extensive programming knowledge can easily upload images, select from pre-trained models, and adjust parameters to achieve high-quality cell segmentation results in just a few clicks.

Please note that **this app is designed for simple, single-image segmentation tasks**, using the core features of Cellpose. For more control or model training, we recommend using the official Cellpose GUI, which provides additional functionality and customization options.

> [!NOTE]
> For simplicity and ease of use, this Gradio-based app **omits GPU acceleration**, instead relying on CPU for all cell segmentation tasks.
>
> If you plan on **running many images**, you may benefit from installing the **official Cellpose GUI with GPU support**.

## Acknowledgments

* This project uses **[Gradio](https://www.gradio.app/)**, an open-source library for building machine learning web apps.

* This application is based on the **[Cellpose library](https://github.com/mouseland/cellpose)**. If you find it useful in your research, please cite the original paper:

**If you use Cellpose 1, 2 or 3, please cite the Cellpose 1.0 [paper](https://www.nature.com/articles/s41592-020-01018-x.epdf?sharing_token=yrCA1mB-y9TR8-RC8w_CPdRgN0jAjWel9jnR3ZoTv0Ms-A3TbUG5N7s_6d3I7lMImMDE6cyl-17ubiknffX50r-dX1un0XSIQ2PGYWsCV1du16fIaipcHNxste8FMByEL75Ek_S2_UEVkSk7lCFllWEVogGWJwmQkBC9uKq9UEA%3D)**:
Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021). Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106.

**If you use the new image restoration models or cyto3, please also cite the Cellpose3 [paper](https://www.biorxiv.org/content/10.1101/2024.02.10.579780v1)**:
Stringer, C. & Pachitariu, M. (2024). Cellpose3: one-click image restoration for improved segmentation. bioRxiv.

## Running the App

### Using Conda

1. Clone this repository:
   ```
   git clone https://github.com/your-username/cellpose-segmentation-app.git
   cd cellpose-segmentation-app
   ```

2. Create a conda environment from the `environment.yml` file:
   ```
   conda env create -f environment.yml
   ```

3. Activate the environment:
   ```
   conda activate cellpose-gradio
   ```

4. Run the app:
   ```
   python Cellpose_gradio.py
   ```

5. Open your web browser and go to the URL displayed in the terminal (usually `http://127.0.0.1:7860`).
