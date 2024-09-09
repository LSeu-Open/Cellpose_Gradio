# Cellpose-Gradio

The **Cellpose-Gradio App** is a modern, user-friendly interface build on the popular **Cellpose library**, making its powerful cell segmentation capabilities accessible to non-experts. By wrapping the complexity of Cellpose within a streamlined **Gradio app**, users without extensive programming knowledge can easily :

* upload images.
* select from pre-trained models.
* adjust parameters to achieve high-quality cell segmentation results in just a few clicks.

> [!NOTE]
> This app is designed for simple, single-image segmentation tasks, using the core features of Cellpose. For more control or model training, we recommend using the official **Cellpose GUI**, which provides additional functionality and customization options.

> [!IMPORTANT]
> For **simplicity and ease of use**, this Gradio-based app **omits GPU acceleration**, instead relying on CPU for all cell segmentation tasks.
>
> If you plan on **running many images**, you may benefit from installing the **official Cellpose GUI with GPU support**.

## Requirements

**Before proceeding with the installation process, please ensure that Python is installed on your system.**

If Python is not already installed, please download and install it from the [official Python website](https://www.python.org/downloads/) for your operating system.

Once Python is installed, you can proceed with the next steps in the installation process.

<br>

## Automated Installation and Running (Recommended)

### For Windows (Initial Setup)

#### 1. Download or clone this repository

To Download the Repository :  

* Click on the `<> Code` button at the top of the repository page.
* Select either "Download ZIP" or "Download tar.gz" from the dropdown menu.
* Extract the downloaded file to your desired location.

to Clone the Repository : 

* Click on the `<> Code` button at the top of the repository page.
* Copy the repository URL.
* Open your terminal or command prompt.
* Run the following command to clone the repository:
  
```
git clone https://github.com/LSeu-Open/Cellpose_Gradio.git
```


#### 2. Double-click on the `setup_and_run.bat` file to run the setup script.
#### 3. Follow the on-screen prompts.

The script will perform the following actions:

* **Check for Python Installation**: Verify if Python is installed on your system.
* **Create a New Environment**: Set up a new virtual environment to isolate dependencies.
* **Install Dependencies**: Install all necessary packages and libraries required for the project. This process may take some time, depending on your computer's specifications.
* **Launch the Cellpose Gradio App**: Start the Cellpose application using Gradio

#### 4. Open the app

Open your web browser and navigate to the URL displayed in the terminal (usually http://127.0.0.1:7860). Alternatively, you can simply Ctrl+click on the URL in the terminal.

### For Linux/macOS (Initial Setup)

#### 1. Download or clone this repository.
#### 2. Open a terminal in the repository directory.
#### 3. Make the setup script executable:

   ```bash
   chmod +x setup_and_run.sh
   ```

#### 4. Run the setup script:

   ```bash
   ./setup_and_run.sh
   ```

#### 5. Follow the on-screen prompts. The script will:

The script will perform the following actions:

* **Check for Python Installation**: Verify if Python is installed on your system.
* **Create a New Environment**: Set up a new virtual environment to isolate dependencies.
* **Install Dependencies**: Install all necessary packages and libraries required for the project. This process may take some time, depending on your computer's specifications.
* **Launch the Cellpose Gradio App**: Start the Cellpose application using Gradio

#### 6. Open the app

Open your web browser and navigate to the URL displayed in the terminal (usually http://127.0.0.1:7860). Alternatively, you can simply Ctrl+click on the URL in the terminal.

### Running the App After Initial Setup

After the initial setup, you can use the following scripts to run the app:

* On Windows: Double-click `run_app.bat`
* On Linux/macOS: Run `./run_app.sh` in the terminal

These scripts will activate the environment and **launch the Cellpose Gradio app without repeating the setup process.**

<br>

## Manual Installation and Running

### Using venv

1. Clone this repository:

   ```bash
   git clone https://github.com/LSeu-Open/Cellpose_Gradio.git
   cd Cellpose-Gradio
   ```

2. Create a virtual environment:

   ```bash
   python -m venv cellpose-gradio-env
   ```

3. Activate the virtual environment:

   * On Windows:

   ```bash
     cellpose-gradio-env\Scripts\activate
   ```

   * On macOS and Linux:

   ```bash
     source cellpose-gradio-env/bin/activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the app:

   ```bash
   python Cellpose_gradio.py
   ```

6. Open your web browser and go to the URL displayed in the terminal (usually `http://127.0.0.1:7860`).

### Using Conda

> [!NOTE]
> we will assume that you have already installed Conda. If not, please install Conda from [here](https://docs.anaconda.com/free/miniconda/miniconda-install/).

1. Open Anaconda Prompt (on Windows) or Terminal (on macOS/Linux).

2. Clone this repository:

   ```bash
   git clone https://github.com/LSeu-Open/Cellpose_Gradio.git
   cd Cellpose-Gradio
   ```

3. Create a conda environment from the `environment.yml` file:

   ```bash
   conda env create -f environment.yml
   ```

4. Activate the environment:

   ```bash
   conda activate cellpose-gradio
   ```

5. Run the app:

   ```bash
   python Cellpose_gradio.py
   ```

6. Open your web browser and go to the URL displayed in the Anaconda Prompt/Terminal (usually `http://127.0.0.1:7860`).

### Using uv

1. Clone this repository:

   ```bash
   git clone https://github.com/LSeu-Open/Cellpose_Gradio.git
   cd Cellpose-Gradio
   ```

2. Install uv if you haven't already:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

4. Activate the virtual environment:

   * On Windows:

   ```bash
   .venv\Scripts\activate
   ```

   * On macOS and Linux:

   ```bash
   source .venv/bin/activate
   ```

5. Run the app:

   ```bash
   python Cellpose_gradio.py
   ```

6. Open your web browser and go to the URL displayed in the terminal (usually `http://127.0.0.1:7860`).

<br>

## Acknowledgments

This project uses the following open-source libraries:

* [Cellpose](https://github.com/mouseland/cellpose), licensed under the [BSD 3-Clause License](https://github.com/mouseland/cellpose/blob/master/LICENSE)
* [Gradio](https://github.com/gradio-app/gradio), licensed under the [Apache License 2.0](https://github.com/gradio-app/gradio/blob/main/LICENSE)

Please see the [LICENSE](LICENSE) file for full license texts.

* This application is based on the **[Cellpose library](https://github.com/mouseland/cellpose)**. If you find it useful in your research, please cite the original paper:

**If you use Cellpose 1, 2 or 3, please cite the Cellpose 1.0 [paper](https://www.nature.com/articles/s41592-020-01018-x.epdf?sharing_token=yrCA1mB-y9TR8-RC8w_CPdRgN0jAjWel9jnR3ZoTv0Ms-A3TbUG5N7s_6d3I7lMImMDE6cyl-17ubiknffX50r-dX1un0XSIQ2PGYWsCV1du16fIaipcHNxste8FMByEL75Ek_S2_UEVkSk7lCFllWEVogGWJwmQkBC9uKq9UEA%3D)**:
Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021). Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106.

**If you use the new image restoration models or cyto3, please also cite the Cellpose3 [paper](https://www.biorxiv.org/content/10.1101/2024.02.10.579780v1)**:
Stringer, C. & Pachitariu, M. (2024). Cellpose3: one-click image restoration for improved segmentation. bioRxiv.
