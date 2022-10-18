import os

import torch
import cv2
import yaml

colors = [
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
]

model = torch.hub.load('yolov5', "custom", source="local", path="yolov5/runs/train/exp/weights/ALET.pt")

categories = {}
with open("dataset_converted.yml", "r") as f:
    loaded_cat_file = yaml.safe_load(f)

    print(loaded_cat_file)

    for id, cat in loaded_cat_file["names"].items():
        print(f"Loading categories binding: {id} - {cat}")

        categories[id] = cat


def run_test(test_img):
    img = cv2.imread(test_img)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model(img2)

    for box in results.xyxy[0]:
        x_start = round(box[0].item())
        y_start = round(box[1].item())

        x_end = round(box[2].item())
        y_end = round(box[3].item())

        category = int(box[5].item())

        color_cat = colors[category % 6]

        cv2.rectangle(img, (x_start, y_start), (x_end, y_end), color_cat, 2)
        cv2.putText(img, f"{categories[int(category)]} ({category})", (x_start, y_end), cv2.FONT_HERSHEY_DUPLEX, 3,
                    color_cat, 1, 1)

        print(f"{x_start} {y_start} {x_end} {y_end} cat: {category}")

    cv2.imshow("Model test", cv2.resize(img, (1000, 800)))
    cv2.waitKey()

run_test("testing/image 0000.jpeg")

