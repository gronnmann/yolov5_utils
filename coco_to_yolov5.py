import json
from os.path import exists
from folder_bindings import file_img_folder, file_annotations, file_labels_folder
import yaml

img_data = {}
# image saved as dict object with fields: id, filename, width, height, boxes: [category id, box data]

changed_categories = {}
# updated categories saved as {oldindex: (newindex, name)}
# For some reason COCO annotations (or atleast 2014) have weird category ids, which YOLO doesn't like.
# will get converted from 0-n

with open(file_annotations) as f:
    json_data = json.load(f)

    images = json_data["images"]

    annotations = json_data["annotations"]

    categories = json_data["categories"]

    # Categories conversion and dataset file saving

    for i, category_id_fixed in enumerate(categories):
        cat_id = category_id_fixed["id"]
        cat_name = category_id_fixed["name"]
        changed_categories[str(cat_id)] = (i, cat_name)

        print(f"Renamed category {cat_id}:{cat_name} to {i}:{cat_name}")

    dataset_yml = {
        "path": "Please specify dataset root dir",
        "train": "Please specify train folder",
        "val": "Please specify val folder",
        "test": "Please specify val folder",
        "names": {int(value[0]): value[1] for key, value in changed_categories.items()},
    }

    with open("dataset_converted.yml", "w") as dataset_file:
        yaml.dump(dataset_yml, dataset_file, default_flow_style=False)
        print("Dumping renamed categories in dataset_converted.yml")

    # Image loading

    for img in images:

        file = img["file_name"]
        size = (img["width"], img["height"])
        id = img["id"]

        file_path = file_img_folder + "/" + file
        img_exists = exists(file_path)

        if img_exists:
            print(f"Loading image: {file}:. Size: {size}. Path: {file_path} Exists: {img_exists}")
            image_instance = {
                "id": id,
                "filename": file,
                "width": size[0],
                "height": size[1],
                "boxes": [],
            }
            img_data[id] = image_instance
        else:
            print("Skipping {file}, doesnt exist...")

    # Annotation loading, matching with image files

    for annotation in annotations:
        id = annotation["image_id"]
        bounding_box = annotation["bbox"]
        category_id = annotation["category_id"]

        img_object = img_data.get(id)
        if img_object == None:
            print(f"Image object {id} not found...")
        else:
            category_id_fixed = changed_categories[str(category_id)][0]
            img_object["boxes"].append([category_id_fixed, bounding_box])
            print(f"Writing category {category_id_fixed} boundingbox to {id}. Box: {bounding_box}")

        print(f"Image {id}: {bounding_box}")

# Saving of all the data

for data in img_data.values():
    bounding_boxes = data["boxes"]
    img_width = float(data["width"])
    img_height = float(data["height"])

    img_file_name = str(data["filename"]).split(".")[-2] + ".txt"
    full_path = file_labels_folder + "/" + img_file_name

    img_file_data = []

    print(f"Saving to {full_path}. Numboxes = {len(bounding_boxes)}")

    annotation_file = open(full_path, "w")

    with open(full_path, "w") as annotation_file:

        # Saving all boxes to corresponding file

        for box_data in bounding_boxes:
            box = box_data[1]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]

            # Conversion from (x1, y1) (x2, y2) COCO to normalized (x_mid, y_mid, width, height) YOLOv5 format

            normalized_x = (x + (w / 2)) / img_width
            normalized_y = (y + (h / 2)) / img_height

            normalized_width = box[2] / img_width
            normalized_height = box[3] / img_height

            box_string = f"{box_data[0]} {normalized_x} {normalized_y} {normalized_width} {normalized_height}"
            img_file_data.append(box_string)

        print("\n".join(img_file_data))
        annotation_file.writelines("\n".join(img_file_data))
