# Interactive Precision Color & Skin Inspector (OpenCV)

An advanced, interactive Computer Vision application built using Python and OpenCV. It captures a live webcam feed and allows users to click anywhere on the screen to instantly inspect, analyze, and retrieve accurate color names, RGB values, and HEX codes using an optimized HSV color-space engine.

## 📌 Problem Statement
Standard color detectors often fail under variable indoor lighting or suffer from single-pixel noise, frequently confusing similar shades (such as confusing vibrant orange with skin tones, or white with gray). This project solves these challenges by utilizing an interactive **Click-to-Inspect ROI (Region of Interest) patch-sampling mechanism** combined with an advanced **HSV-based classification pipeline**.

## 🚀 Approach & Methodology
1. **Multi-Threaded Video Stream:** Implements a thread-safe video capture buffer to guarantee zero-lag, real-time performance.
2. **Interactive Mouse Sampling:** Listens for left-click events via OpenCV callbacks. When clicked, it extracts a multi-pixel patch around the coordinate to eliminate single-pixel noise.
3. **HSV Color Space Conversion:** Converts BGR values into HSV (Hue, Saturation, Value) format, making color classification robust against shadows and ambient room lighting changes.
4. **Smart Calibration Logic:** Uses precision thresholds to accurately distinguish between human skin tones, vibrant oranges, pure greens, whites, grays, and secondary hues.

## 📊 Key Features
- **Click-to-Inspect Architecture:** Click anywhere on the video feed to freeze and analyze the exact object or fabric color.
- **Detailed Color Metadata:** Displays the human-readable color name, precise RGB tuple, and exact **HEX code** (`#RRGGBB`).
- **Enterprise HUD Dashboard:** Features a dynamic UI panel with a live border color matching the exact sampled shade.
- **Lighting Resilience:** Specially tuned thresholds to prevent false positives on white, gray, and skin tones under standard indoor lighting.

## 🛠️ Setup & Run Instructions

### Prerequisites
Make sure Python is installed on your system.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Diksharautela08/opencv-color-detector.git
   cd ColorDetector
2. Install required dependencies:
   ```Bash
   pip install opencv-python numpy
3. Run the application:
   ```Bash
   python main.py

Note: Point any object or wear any colored clothing, click anywhere on the live video window to inspect it, and press the 'q' key to exit.