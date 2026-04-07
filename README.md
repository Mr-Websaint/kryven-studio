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
    Execute the following command in your terminal. Using `python -m streamlit` is recommended as it's more reliable than a direct command.
    ```bash
    python -m streamlit run kryven_studio.py
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

## Updating

The application has a built-in update check. When you start `kryven_studio.py`, it will automatically check for a new version.

If a new version is available, a notification will appear at the top of the page with an "Update Now" button. Clicking this button will launch the update process in a new console window. Follow the instructions in that window.

Your generated images in the `output` folder will not be affected by the update.

---

## Disclaimer

This is an unofficial, community-driven project. It is not affiliated with, endorsed by, or connected to the official Kryven team in any way. This tool was developed as a hobby project to provide a convenient user interface for the Kryven API.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
