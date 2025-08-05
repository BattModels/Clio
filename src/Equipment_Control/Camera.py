import cv2
import os
from datetime import datetime
import time

# Create a folder to save images if it doesn't exist
save_folder = "captured_images"
os.makedirs(save_folder, exist_ok=True)
# Open the camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

def take_picture():
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

    time.sleep(2)
    ret, frame = cap.read()  # Capture frame
    if not ret:
        print("Error: Could not read the frame.")
        return None
    return frame

if __name__ == '__main__':
    current_time_str = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    cv2.imwrite(os.path.join(save_folder, f'{current_time_str}.jpg'), take_picture())
    print(f"Image saved as {current_time_str}.jpg")