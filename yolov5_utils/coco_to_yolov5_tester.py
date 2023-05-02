import cv2

import os
import random
import math

import yaml

from folder_bindings import file_img_folder, file_labels_folder, file_annotations


#TODO: Not working at the moment

colors = [
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
]



categories = {}
with open(file_annotations, "r") as f:
    loaded_cat_file = yaml.safe_load(f)

    print(loaded_cat_file)

    for id, cat in loaded_cat_file["names"].items():


        print(f"Loading categories binding: {id} - {cat}")

        categories[id] = cat

def get_random_picture():

    random_file = None
    random_file_jpg = None
    random_file_txt = None

    while True:
        random_file = str(random.choice(os.listdir(file_img_folder))).split(".")[-2]

        random_file_jpg = file_img_folder + "/" + random_file + ".png"
        random_file_txt = file_labels_folder + "/" + random_file + ".txt"

        

        with open(random_file_txt) as f:
            print(f"Attempting opening {random_file_txt}")
            lines = f.readlines()
            if len(lines) > 0:
                break


    

    img = cv2.imread(random_file_jpg)

    w,h = float(img.shape[1]), float(img.shape[0])

    with open(random_file_txt) as f:
        for line in f.readlines():
            split = line.split(" ")
            cat = int(split[0])

            print(f"Image: {w}x{h}")


            x_mid = float(split[1])
            y_mid = float(split[2])
            width = float(split[3])
            height = float(split[4])

            x_mid_unpacked = x_mid * w
            width_unpacked = width * w

            y_mid_unpacked = y_mid * h
            height_unpacked = height * h
            
            start_point = (round(x_mid_unpacked - width_unpacked/2), round(y_mid_unpacked - height_unpacked/2))
            end_point = (round(x_mid_unpacked + width_unpacked/2), round(y_mid_unpacked + height_unpacked/2))


            print(f"Line: {line}, unpacked: x={x_mid_unpacked}, y={y_mid_unpacked}, w={width_unpacked}, h={height_unpacked}")

            color_cat = colors[cat % 6]

            cv2.rectangle(img, start_point, end_point, color_cat, 1)
            cv2.putText(img, f"{categories[int(cat)]} ({cat})", (start_point[0], end_point[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_cat, 1, 1)


    return img


for i in range(3):
    print(f"Image test: {i}")
    cv2.imshow(f"Random test {i}", get_random_picture())

cv2.waitKey()