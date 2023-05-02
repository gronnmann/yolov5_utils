import yaml
from os import listdir

# gammal labels til datasettet som skal mergast inn i
folder_old_annotations_path = "dataset_syntetisk/train/labels"

# mappe til nye labels fra samme datasettet
folder_new_annotations_path = "dataset_syntetisk/train/labels_fix"

# kategoriane som utgjer base (tools in use greia)
correct_categories_path = "yolov5/data/combined.yml"

# kategoriane som skal mergast inn i den (dei nye vi har laga)
incorrect_categories_path = "syntetisk_temp/verktoy.yaml"

categories = []
categories_names = []

new_yaml = {}

# Les inn basekategoriar
with open(correct_categories_path) as corr_categories_file:
    opened = yaml.safe_load(corr_categories_file)

    for id, cat in opened["names"].items():
        print(f"Reading: {id} - {cat}")
        categories.append({id: cat})
        categories_names.append(cat)
    new_yaml["path"] = opened["path"]
    new_yaml["test"] = opened["test"]
    new_yaml["train"] = opened["train"]
    new_yaml["val"] = opened["val"]

# Kva skal remappast
remappings = []

# Les inn og kombiner nye kategoriar
with open(incorrect_categories_path) as incorr_categories_file:
    opened = yaml.safe_load(incorr_categories_file)

    for i, cat in opened["names"].items():
        cat_capitalized = cat # Capitalize ved eine datasettet, ikkje ved andre

        if cat_capitalized in categories_names:
            new_index = categories_names.index(cat_capitalized)
            print(f"Found existing category: {cat}. Combining with index: {new_index}")
            remappings.append(new_index)
            categories_names.append(cat_capitalized)
        else:
            new_index = len(categories)
            print(f"Found new category {cat}. Giving index: {new_index}")
            remappings.append(new_index)
            categories.append({new_index: cat_capitalized})
            categories_names.append(cat_capitalized)

print(f"Loaded categories: {categories}")

new_yaml["names"] = categories


# Lager ny kombinert fil
with open("combined.yml", "w") as combined_file:
    yaml.dump(new_yaml, combined_file, default_flow_style=False)
print("Dumped combined dataset yml as combined.yml")

# Bytter kategori-id i filene i gamle labels-mappa og outputter det til nye
print("Searching old label folder")
for label_file in listdir(folder_old_annotations_path):
    file_lines = []
    with open(folder_old_annotations_path + "/" + label_file) as opened_label_file:
        for line in opened_label_file.readlines():
            split_line = line.split(" ")
            old_cat = split_line[0]
            new_cat = remappings[int(old_cat)]

            print(f"Remapping {label_file}, annotation {line}. Changing from {old_cat} to {new_cat}")

            split_line[0] = new_cat

            file_lines.append(" ".join([str(x) for x in split_line]))

    with open(folder_new_annotations_path + "/" + label_file, "w") as opened_dump_file:
        opened_dump_file.writelines(file_lines)

