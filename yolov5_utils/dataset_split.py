import os
import random

# Constants - Set them before running
SPLIT_TRAIN = 70
SPLIT_VALIDATION = 15
SPLIT_TEST = 15

PATH_TO_TOTAL = "/media/bartosz/T7/samlet_datasett/total"

def main():

    if (SPLIT_TRAIN + SPLIT_VALIDATION + SPLIT_TEST) != 100:
        print("Splits do not add up to 100%")
        return

    # Get all files in the directory
    files = os.listdir(PATH_TO_TOTAL + "/images")

    # Get the number of files
    num_files = len(files)

    # Get the number of files for each split
    num_train = int(num_files * (SPLIT_TRAIN / 100))
    num_validation = int(num_files * (SPLIT_VALIDATION / 100))
    num_test = int(num_files * (SPLIT_TEST / 100))

    # Print
    print("Total number of files: ", num_files)
    print("Number of files for training: ", num_train)
    print("Number of files for validation: ", num_validation)
    print("Number of files for testing: ", num_test)

    # Split the files randomly
    print("Picking validation files...")
    validation_files = random.sample(files, num_validation)
    files = [file for file in files if file not in validation_files]
    print("Picking test files...")
    test_files = random.sample(files, num_test)
    print("Picking training files...")
    train_files = [file for file in files if file not in test_files]

    print("Picking complete.")

    print("Creating directories...")

    # Create the directories

    if not os.path.exists(PATH_TO_TOTAL + "/train"):
        os.mkdir(PATH_TO_TOTAL + "/train")
        os.mkdir(PATH_TO_TOTAL + "/train/images")
        os.mkdir(PATH_TO_TOTAL + "/train/labels")
    if not os.path.exists(PATH_TO_TOTAL + "/val"):
        os.mkdir(PATH_TO_TOTAL + "/val")
        os.mkdir(PATH_TO_TOTAL + "/val/images")
        os.mkdir(PATH_TO_TOTAL + "/val/labels")
    if not os.path.exists(PATH_TO_TOTAL + "/test"):
        os.mkdir(PATH_TO_TOTAL + "/test")
        os.mkdir(PATH_TO_TOTAL + "/test/images")
        os.mkdir(PATH_TO_TOTAL + "/test/labels")

    print("Moving train files...")

    # Move the files from img and label
    move_files(train_files, "train")
    move_files(validation_files, "val")
    move_files(test_files, "test")

    print("Moved training files")


def move_files(file_list: list, type: str):
    print(f"Moving files {type}...")
    for file in file_list:
        # os.rename(PATH_TO_TOTAL + "/images/" + file, PATH_TO_TOTAL + "/train/images/" + file)

        img_from = f"{PATH_TO_TOTAL}/images/{file}"
        img_to = f"{PATH_TO_TOTAL}/{type}/images/{file}"

        ext = file.split(".")[-1]
        file_label = file[:-len(ext)] + "txt"

        label_from = f"{PATH_TO_TOTAL}/labels/{file_label}"
        label_to = f"{PATH_TO_TOTAL}/{type}/labels/{file_label}"

        # if os.path.exists(img_from) and os.path.exists(label_from):
        print(f"{img_from} -> {img_to}")
        os.rename(img_from, img_to)
        print(f"{label_from} -> {label_to}")
        os.rename(label_from, label_to)


        # os.rename(PATH_TO_TOTAL + "/labels/" + file[:-len(ext)] + "txt", PATH_TO_TOTAL + "/train/labels/" + file[:-len(ext)] + "txt")
        # print(PATH_TO_TOTAL + "/labels/" + file[:-len(ext)] + "txt" + " -> " + PATH_TO_TOTAL + "/train/labels/" + file[:-len(ext)] + "txt")
    print(f"Moved files {type}.")

main()