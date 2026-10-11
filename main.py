import cv2
import numpy as np

# Global variables
clicked = False
point = (0, 0)
selected_bgr = None
selected_hsv = None

def get_hsv_color_name(h, s, v):
    """
    HSV values ke basis par accurate color name return karega.
    H: 0 to 180, S: 0 to 255, V: 0 to 255
    """
    # Check for Black, White, and Gray first
    if v < 40:
        return "Black"
    if s < 30 and v > 200:
        return "White"
    if s < 35:
        return "Gray"
    
    # Hue ranges for different colors
    if 0 <= h <= 10 or 170 <= h <= 180:
        return "Red"
    elif 11 <= h <= 22:
        # Check if it's Skin Tone vs Orange/Brown based on Saturation & Value
        if 40 <= s <= 160 and 80 <= v <= 250:
            return "Skin Tone"
        elif s > 160:
            return "Orange"
        else:
            return "Brown"
    elif 23 <= h <= 35:
        return "Yellow"
    elif 36 <= h <= 85:
        return "Green"
    elif 86 <= h <= 130:
        return "Blue"
    elif 131 <= h <= 169:
        return "Purple / Pink"
    else:
        return "Redish"

def mouse_click(event, x, y, flags, param):
    global clicked, point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        point = (x, y)

def main():
    global clicked, point, selected_bgr, selected_hsv
    
    cap = cv2.VideoCapture(0)
    window_name = "Advanced HSV Color & Skin Detector"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_click)
    
    print("Webcam started! Click on your face, clothes, or objects to test.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w, _ = frame.shape
            
        # Multi-pixel area sampling on click for maximum accuracy
        if clicked:
            x, y = point
            if 10 <= x < w - 10 and 10 <= y < h - 10:
                patch_bgr = frame[y-5:y+5, x-5:x+5]
                patch_hsv = hsv_frame[y-5:y+5, x-5:x+5]
                
                selected_bgr = tuple(map(int, np.mean(patch_bgr, axis=(0, 1))))
                selected_hsv = tuple(map(int, np.mean(patch_hsv, axis=(0, 1))))
            clicked = False
            
        # Display Result
        if selected_hsv is not None:
            b, g, r = selected_bgr
            hue, sat, val = selected_hsv
            
            color_name = get_hsv_color_name(hue, sat, val)
            
            # Draw sample box at clicked location
            cv2.rectangle(frame, (point[0]-10, point[1]-10), (point[0]+10, point[1]+10), (0, 255, 0), 2)
            
            # Top Banner for Info
            text_info = f"Color: {color_name} | HSV: ({hue}, {sat}, {val})"
            cv2.rectangle(frame, (20, 20), (600, 65), (b, g, r), -1)
            
            text_color = (0, 0, 0) if (int(r) + int(g) + int(b)) > 400 else (255, 255, 255)
            cv2.putText(frame, text_info, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.65, text_color, 2)

        cv2.imshow(window_name, frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()