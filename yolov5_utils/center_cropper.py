import os
import cv2

file_img_folder = "../dataset/train/images"

# open folder
# for each file in folder
# open file
def squarize_folder(folder_path: str):
    files = os.listdir(folder_path)

    for file in files:
        file_whole_path = folder_path + "/" + file

        # print("Opening file: " + file_whole_path)
        img = cv2.imread(file_whole_path)

        # cv2.imshow("Image", img)
        # check if image is square
        if (img is None):
            print(f"File {file_whole_path}is not an image, skipping")
            continue

        height, width, channels = img.shape

        if height != width:
            # crop to square from center
            if height > width:
                # crop height to width
                # get height - width
                # divide by 2
                # crop from half to half + width
                crop_start = int((height - width) / 2)
                crop_end = int(crop_start + width)
                #check if odd
                img = img[crop_start:crop_end, 0:width]
            else:
                crop_start = int((width - height) / 2)
                crop_end = int(crop_start + height)

                img = img[0:height, crop_start:crop_end]

            # save image
            cv2.imwrite(file_whole_path, img)

            # cv2.imshow("Cropped", img)
            # cv2.waitKey(0)

squarize_folder(file_img_folder)