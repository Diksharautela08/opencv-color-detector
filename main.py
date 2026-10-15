import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GLOG_minloglevel'] = '2'

import cv2
import numpy as np
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

current_frame = None
selected_data = {
    "name": "Click anywhere on video",
    "rgb": (0, 0, 0),
    "hex": "#000000",
    "pos": None
}

class VideoStreamBuffer:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            grabbed, frame = self.stream.read()
            with self.lock:
                self.grabbed = grabbed
                if grabbed:
                    self.frame = frame
            time.sleep(0.01)

    def read(self):
        with self.lock:
            if not self.grabbed or self.frame is None:
                return False, None
            return True, self.frame.copy()

    def stop(self):
        self.stopped = True
        self.stream.release()

def get_accurate_color_name(bgr_color):
    b, g, r = int(bgr_color[0]), int(bgr_color[1]), int(bgr_color[2])
    hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()
    
    bgr_pixel = np.array([[[b, g, r]]], dtype=np.uint8)
    hsv_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)
    h, s, v = int(hsv_pixel[0][0][0]), int(hsv_pixel[0][0][1]), int(hsv_pixel[0][0][2])
    
    # Check Black
    if v < 30:
        return "Black", (r, g, b), hex_code
        
    # Improved White & Gray Detection (Allows slightly lower brightness for indoor white objects)
    if s < 35:
        if v > 140: return "White / Off-White", (r, g, b), hex_code
        elif v > 70: return "Light Gray", (r, g, b), hex_code
        else: return "Dark Gray", (r, g, b), hex_code

    # Hue-based classification
    if (h >= 0 and h <= 8) or (h >= 170 and h <= 179):
        if v < 90: return "Dark Red", (r, g, b), hex_code
        elif s < 120: return "Light Pink / Rose", (r, g, b), hex_code
        else: return "Pure Red", (r, g, b), hex_code
        
    elif h > 8 and h <= 22:
        # Differentiating bright Orange from skin tone based on Saturation
        if s > 110 and v > 100:
            return "Vibrant Orange", (r, g, b), hex_code
        else:
            return "Skin Tone / Flesh", (r, g, b), hex_code
            
    elif h > 22 and h <= 35:
        return "Yellow / Gold", (r, g, b), hex_code
        
    elif h > 35 and h <= 85:
        if v < 90: return "Dark Green", (r, g, b), hex_code
        elif s < 70: return "Olive / Sage Green", (r, g, b), hex_code
        else: return "Pure / Bright Green", (r, g, b), hex_code
        
    elif h > 85 and h <= 100:
        return "Aqua / Cyan", (r, g, b), hex_code
        
    elif h > 100 and h <= 135:
        if v < 90: return "Navy Blue", (r, g, b), hex_code
        elif s < 60: return "Slate / Steel Blue", (r, g, b), hex_code
        else: return "Royal / Sky Blue", (r, g, b), hex_code
        
    elif h > 135 and h <= 162:
        return "Violet / Purple", (r, g, b), hex_code
        
    elif h > 162 and h < 170:
        return "Pink / Magenta", (r, g, b), hex_code
        
    else:
        return "Multicolor / Mixed", (r, g, b), hex_code

def mouse_click_handler(event, x, y, flags, param):
    global current_frame, selected_data
    if event == cv2.EVENT_LBUTTONDOWN:
        if current_frame is not None:
            h_f, w_f, _ = current_frame.shape
            if 0 <= x < w_f and 0 <= y < h_f:
                patch = current_frame[max(0, y-3):min(h_f, y+4), max(0, x-3):min(w_f, x+4)]
                mean_bgr = np.mean(patch, axis=(0, 1))
                
                c_name, rgb_val, hex_val = get_accurate_color_name(mean_bgr)
                selected_data["name"] = c_name
                selected_data["rgb"] = rgb_val
                selected_data["hex"] = hex_val
                selected_data["pos"] = (x, y)
                
                logging.info(f"Clicked -> Color: {c_name} | RGB: {rgb_val} | HEX: {hex_val}")

def main():
    global current_frame
    vs = VideoStreamBuffer(src=0).start()
    time.sleep(1.5)
    
    window_name = "GestureSpeak - Click-to-Inspect Color Analyzer"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_click_handler)
    
    logging.info("Click-to-Inspect Color Analyzer Operational. Click anywhere on the video feed to check color. Press 'q' to exit.")

    while True:
        success, frame = vs.read()
        if not success or frame is None:
            time.sleep(0.01)
            continue
            
        frame = cv2.flip(frame, 1)
        current_frame = frame.copy()
        h_frame, w_frame, _ = frame.shape

        if selected_data["pos"] is not None:
            px, py = selected_data["pos"]
            cv2.circle(frame, (px, py), 8, (255, 255, 255), 2)
            cv2.circle(frame, (px, py), 3, (0, 0, 255), -1)

        cv2.rectangle(frame, (20, 20), (w_frame - 20, 135), (25, 25, 25), -1)
        
        border_color = (255, 255, 255)
        if selected_data["pos"] is not None:
            r, g, b = selected_data["rgb"]
            border_color = (int(b), int(g), int(r))
            
        cv2.rectangle(frame, (20, 20), (w_frame - 20, 135), border_color, 2)
        
        cv2.putText(frame, f"COLOR: {selected_data['name']}", (35, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"RGB: {selected_data['rgb']}", (35, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.putText(frame, f"HEX: {selected_data['hex']} (Click anywhere to inspect)", (35, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        
        cv2.putText(frame, "Click-to-Inspect Engine v3.1 | Press 'q' to Quit", (30, h_frame - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

        cv2.imshow(window_name, frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    vs.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()