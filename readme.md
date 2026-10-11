# Interactive Color & Skin Detector using OpenCV

An advanced Computer Vision mini-project built using Python and OpenCV that captures live webcam input and interactively detects and names colors (along with Skin Tone recognition) using HSV color space and multi-pixel sampling.

## 📌 Problem Statement
Standard color detection systems often struggle with unstable lighting conditions or single-pixel inaccuracies. The goal of this project is to build an interactive, robust color detection tool that samples a region of interest (ROI) when clicked and accurately translates the color into human-readable names using HSV color thresholds.

## 🚀 Approach & Methodology
1. **Live Feed & Interaction:** Captures real-time video using `cv2.VideoCapture(0)` and listens for left-click events via OpenCV Mouse Callbacks.
2. **Multi-Pixel Region Sampling (ROI):** Instead of checking a single unstable pixel, the script extracts a 10x10 patch around the clicked coordinate and calculates the average BGR and HSV values for stability.
3. **HSV Color Space Conversion:** Converts BGR frames to HSV (Hue, Saturation, Value) format, making color classification immune to ambient lighting changes.
4. **Smart Classification Logic:** Uses tailored threshold ranges to accurately distinguish between Primary Colors, Grayscale, Browns, and Human Skin Tones.

## 📊 Features
- Interactive single-click color inspection.
- Accurate detection of Red, Green, Blue, Yellow, Orange, Brown, Black, White, and Human Skin Tones.
- Dynamic info banner showing live HSV values and the detected color name.
- Smart text-contrast rendering for high readability.

## 🛠️ Setup & Run Instructions

### Prerequisites
Make sure Python is installed on your system.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the project:
   ```bash
   python main.py

Note: Press the 'q' key while the webcam window is active to exit the application. 