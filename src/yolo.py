from ultralytics import YOLO
import cv2
import numpy as np
import pathlib
import os
import time

# Load a model
script_path = pathlib.Path(__file__).parent.resolve()
project_path = pathlib.Path(__file__).parent.resolve()/'..'
project_path=project_path.resolve()
images_path = project_path/'data'/'images'
images_path = images_path.resolve()
yolo_path = script_path/'yolo'/'yolo11n-seg.pt'
model = YOLO(str(yolo_path))

def process_image(image_path, mode='crop'):
    image = cv2.imread(image_path)
    results = model(image)[0]
    image = results.orig_img
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)
    if mode=='crop':
        n=0
        idx = image_path.replace('images', 'crops').split('/')[-1].split('.')[0]
        idx_path = project_path/'data'/'crops'/str(idx)
        try:
            os.mkdir(str(idx_path))
            
            if len(boxes)!=0:
                for box in boxes:
                    x1, y1, x2, y2 = box
                    #cv2.rectangle(image, (x1, y1), (x2, y2), (192, 192, 192), 2)
                    cv2.imwrite(str(idx_path/f'crop_{n}.jpg'), image[y1:y2, x1:x2])
                    n+=1
            else:
                cv2.imwrite(str(idx_path/f'crop_0.jpg'), image)
        except FileExistsError:
            print('Dir already exist! Scip this image')
    elif mode=='search':
        n=0
        test_path = project_path/f'data/test_images/crops/test_{time.time()}'
        print(test_path)
        os.mkdir(str(test_path))
        for box in boxes:
            x1, y1, x2, y2 = box
            #cv2.rectangle(image, (x1, y1), (x2, y2), (192, 192, 192), 2)
            cv2.imwrite(str(test_path/f'crop_{n}.jpg'), image[y1:y2, x1:x2])
            n+=1
        return str(test_path/f'crop_{n}.jpg')

def get_all_crops():
    images_arr = os.listdir(str(images_path))
    for image in images_arr:
        process_image(str(images_path/image), 'crop')
