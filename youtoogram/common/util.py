import os

import cv2
import numpy as np


def create_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)


def save_to_jpg(file, file_path, file_name):
    extension = '.jpg'
    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    file_full_path = os.path.join(file_path, file_name + extension)
    cv2.imwrite(file_full_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return file_full_path
