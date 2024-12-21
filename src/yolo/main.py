from ultralytics import YOLO
import cv2
import numpy as np
import os

# Load a model
model = YOLO("./yolo/yolo11n.pt")

def process_image(image_path):
    image = cv2.imread(image_path)
    results = model(image)[0]
    image = results.orig_img
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
    n=0
    for box in boxes:
        x1, y1, x2, y2 = box
        cv2.rectangle(image, (x1, y1), (x2, y2), (192, 192, 192), 2)
        cv2.imwrite(f'./test/crop_{n}.jpg', image[x1:y1, x2:y2])
        print(x1)
        n+=1
    new_image_path = os.path.splitext(image_path)[0] + '_yolo' + os.path.splitext(image_path)[1]
    cv2.imwrite(new_image_path, image)
    return boxes

print(process_image('./image.png'))