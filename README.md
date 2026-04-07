# Kryven AI Studio 🎨

A simple yet powerful web frontend for the Kryven AI Media Generation API, built with Streamlit. This application provides an intuitive graphical user interface to generate images and videos.

## Features

-   **Text-to-Image Generation:** Create images from text descriptions.
-   **Image-to-Image Generation:** Modify an existing image based on a text prompt.
-   **Image-to-Video Generation:** Animate a static image into a 4-second video clip.
-   **Dynamic Filenames:** Downloaded files are automatically named with a timestamp and a descriptive name based on the prompt.
-   **Persistent Results:** The last generated result remains visible even when you change settings.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mr-Websaint/kryven-studio.git
    cd kryven-studio
    ```

2.  **Install the dependencies:**
    Make sure you have Python 3.8+ installed.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Provide your API Key:**
    You will need an API key from [kryven.cc](https://kryven.cc).

2.  **Run the Streamlit application:**
    Execute the following command in your terminal:
    ```bash
    streamlit run kryven_studio.py
    ```

3.  **Use the application:**
    -   Open the URL displayed in your terminal in your browser.
    -   Enter your Kryven API key in the sidebar.
    -   Select the desired mode, fill in the fields, and start generating!

## Configuration

All settings can be configured directly in the application's sidebar:

-   **Kryven API Key:** Your personal key for API authentication.
-   **Mode:** Choose between "Text to Image" and "Image to Video".
-   **Model Type (for images):** Select the model to use (`a2e` or `seedream`).
-   **Aspect Ratio (for images):** Define the format of the generated image.
-   **Image URL (optional):** Provide a URL for image-to-image transformations.
-   **URL of the image to animate (for videos):** The source for video creation.