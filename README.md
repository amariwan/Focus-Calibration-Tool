# Focus Calibration Tool

This Python script provides a focus calibration tool using OpenCV and picamera2 for Raspberry Pi. It allows users to calibrate and visualize focus quality in different regions of an image.

## Features

- **Live Edge Detection:** Real-time edge detection using Canny algorithm.
- **Focus Calibration:** Allows calibration of focus by monitoring white pixel counts.
- **Interactive Interface:** Keyboard shortcuts for calibration, focus toggling, and saving images.

## Requirements

- Python 3.x
- Raspberry Pi with Picamera2
- OpenCV (`pip install opencv-python`)
- python-dotenv (`pip install python-dotenv`)
- picamera2 (`pip install picamera2`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amariwan/focus-calibration-tool.git
   cd focus-calibration-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and configure the following parameters:
   ```dotenv
   IMAGE_SAVE_PATH=
   CAMERA_RESOLUTION_WIDTH=3280
   CAMERA_RESOLUTION_HEIGHT=2464
   PREVIEW_WIDTH=1920
   PREVIEW_HEIGHT=1080
   ```

4. Run the script:
   ```bash
   python focus_calibration.py
   ```

## Usage

- **Calibration:** Press `c` to toggle calibration mode. In this mode, the script monitors and records the maximum white pixel count in each defined region.
- **Focus Check:** Press `f` to toggle focus mode. This highlights regions based on their deviation from the calibrated maximum white pixel count, indicating focus quality.
- **Save Results:** Press `q` to save the current frame with annotated regions as an image (`focus_<timestamp>.jpg`) and a text file (`data_<timestamp>.txt`) containing region details.
- **Organize Images:** Press `o` to save the current frame with annotated regions in a specified directory structure based on input parameters.

## Configuration

- Edit the `.env` file to adjust parameters such as image save path and camera resolutions according to your setup.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors of OpenCV, Picamera2, and python-dotenv libraries.
- Inspired by the need for a simple yet effective focus calibration tool for Raspberry Pi.

