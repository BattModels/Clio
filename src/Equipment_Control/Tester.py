from ultralytics import YOLO
import os
import cv2
import torch
num_pics = 5
# Get the full path of the current file
current_file = os.path.abspath(__file__)

classes = ['Clear', 'Sediment', 'Turbid']
# Get the directory containing this file
current_dir = os.path.dirname(current_file)
model = YOLO(os.path.join(current_dir, "best.pt"))
from Camera import take_picture
# Load the trained model

confidences = []
for i in range(num_pics):
    frame = take_picture()
    save_path = f"Detect {i}.jpg"
    cv2.imwrite(save_path, frame)
    # Perform inference on an image
    results = model.predict(frame, show=True, conf=0.01)
    confidences.append(results[0].probs.data)

result = torch.stack(confidences).sum(dim=0)
index = torch.argmax(result).item()
print(classes[index])