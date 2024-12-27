import cv2
import pathlib
import os
import numpy as np

def create_test_images():
    '''
    Function for create test dataset
    '''
    image_path = pathlib.Path(__file__).parent.resolve()/'..'/'data'/'images' # path to images
    image_path = image_path.resolve()

    for _, _, files in os.walk(image_path):
        for i in files:
            img = cv2.imread(image_path/i)
            noise = np.random.normal(1, 1, img.shape).astype('uint8') # generate Gauss noise
            noisy_image = cv2.add(img, noise) # add Gauss noise to image
            cv2.imwrite(image_path/'..'/'test_images'/'auto'/f'{i}', noisy_image)
            

create_test_images()