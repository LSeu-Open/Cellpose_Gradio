# Cellpose-Gradio-Colorblind-ready

In response to non-experts' struggles with Cellpose's complex process, I created this app to provide a more accessible solution.

The ***Cellpose-Gradio App*** is a modern, user-friendly interface built on the popular **Cellpose library**, making its powerful cell segmentation capabilities available to users without extensive technical expertise. 

This app is designed for straightforward, **single-image segmentation tasks**, utilizing the core features of Cellpose. Additionally, **it can serves as an educational tool to help users understand how to manage segmentation parameters effectively.** 

For more advanced control over segmentation, including **human-in-the-loop training** or accessing the **image restoration features of the 3.0 version**, please use the **official Cellpose GUI**.

By encapsulating the complexity of Cellpose within an intuitive **Gradio app**, users can easily:

* upload images.
* select from pre-trained models.
* adjust parameters to achieve **high-quality cell segmentation results in just a few clicks**.
* **Save results** to multiple file formats:
  - ***Segmentation masks*** in either .png or .npy format.
  - ***Outlines of segmentation masks*** as .png files.
  - ***Resulting figures*** displayed within the app as .png or .svg files.

<br>

> [!IMPORTANT]
> This app now has a **colorblind-ready version.**
> 
> If you are concerned about this, ***we welcome your feedback on our color choices. Please consider contacting us or opening an issue.***
>
> To **access the colorblind version**, please go to the **[release list](https://github.com/LSeu-Open/Cellpose_Gradio/releases) and select the colorblind version of the latest release.**

<br>

## Table of Contents


* [Requirements](#requirements)
* [Automated Installation and Running (Recommended)](#automated-installation-and-running-recommended)
    - [Windows (Initial Setup)](#windows-initial-setup)
    - [Linux and macOS (Initial Setup)](#linux-and-macos-initial-setup)
    - [Run the App After the Initial Setup](#run-the-app-after-the-initial-setup)    
* [Manual Installation and Running](#manual-installation-and-running)
    - [Using venv](#using-venv)
    - [Using Conda](#using-conda)
    - [Using uv](#using-uv)  
* [Acknowledgments](#acknowledgments)


## Requirements

**Before proceeding with the installation process, please ensure that Python is installed on your system.**

If Python is not already installed, please download and install it from the [official Python website](https://www.python.org/downloads/) for your operating system.

Once Python is installed, you can proceed with the next steps in the installation process.

> [!IMPORTANT]
> For **simplicity and ease of use**, this Gradio-based app **omits GPU acceleration**, instead relying on CPU for all cell segmentation tasks.
>
> If you plan to **run multiple images or process very large images**, you may benefit from installing the **official Cellpose GUI with GPU support**.

<br>

## Automated Installation and Running (Recommended)

### Windows (Initial Setup)

> [!NOTE]
> First-time users, please follow these steps.
>
> After setting it up the first time, simply run `run_app.bat` script to launch the app.

#### 1. Download or clone this repository

To Download the Repository :  

* Click on the `<> Code` button at the top of the repository page.
* Select either "Download ZIP" or "Download tar.gz" from the dropdown menu.
* Extract the downloaded file to your desired location.

to Clone the Repository : 

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

Open your web browser and navigate to the URL displayed in the terminal (typically http://127.0.0.1:7860). Alternatively, you can simply click the URL in the terminal while holding down the Ctrl key.

### Linux and macOS (Initial Setup)

> [!NOTE]
> First-time users, please follow these steps.
>
> After setting it up the first time, simply run `run_app.sh` script to launch the app.

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

Open your web browser and navigate to the URL displayed in the terminal (typically http://127.0.0.1:7860). Alternatively, you can simply click the URL in the terminal while holding down the Ctrl key.

### Run the App After the Initial Setup

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

Please see the [ACKNOWLEDGMENTS](https://github.com/LSeu-Open/Cellpose_Gradio/blob/main/ACKNOWLEDGMENTS) and [Licence](https://github.com/LSeu-Open/Cellpose_Gradio/blob/main/LICENSE) files for full license texts.

* This application is based on the **[Cellpose library](https://github.com/mouseland/cellpose)**. If you find it useful in your research, please cite the original paper:

**If you use Cellpose 1, 2 or 3, please cite the Cellpose 1.0 [paper](https://www.nature.com/articles/s41592-020-01018-x.epdf?sharing_token=yrCA1mB-y9TR8-RC8w_CPdRgN0jAjWel9jnR3ZoTv0Ms-A3TbUG5N7s_6d3I7lMImMDE6cyl-17ubiknffX50r-dX1un0XSIQ2PGYWsCV1du16fIaipcHNxste8FMByEL75Ek_S2_UEVkSk7lCFllWEVogGWJwmQkBC9uKq9UEA%3D)**:
Stringer, C., Wang, T., Michaelos, M., & Pachitariu, M. (2021). Cellpose: a generalist algorithm for cellular segmentation. Nature methods, 18(1), 100-106.

**If you use the new image restoration models or cyto3, please also cite the Cellpose3 [paper](https://www.biorxiv.org/content/10.1101/2024.02.10.579780v1)**:
Stringer, C. & Pachitariu, M. (2024). Cellpose3: one-click image restoration for improved segmentation. bioRxiv.
