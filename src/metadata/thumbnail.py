from imutils import build_montages
from imutils import paths
from imutils.object_detection import non_max_suppression

import numpy as np
import imutils
import cv2
import glob
import os
import random
import datetime

from PIL import Image, ImageEnhance


# Paths need a / at the end
# base_path = "/Users/julian/tt_comp/uploader/hq_content/upload_videos/addison_video/tt_thumbnails/"
# folder_path = "data/persistent/weekly_uploads/cutest_doggies_1/images"
# base_path = f"{folder_path}/thumbnails/"  # Path needs a / at the end
# target_path = f"{folder_path}/qc_thumbnails/"
# background_path = 'data/static/images/thumbnail_bg.png'
# brigthen_factor = 1.25

folder_path = "data/store/harrypotter"
base_path = f"{folder_path}/images/"  # Path needs a / at the end
target_path = f"{folder_path}/qc_thumbnails/"
background_path = 'data/static/images/thumbnail_bg.png'
brigthen_factor = 1.25

# Settings
white_lines = False
line_width = 0  # in px

# Global variables
img_paths = glob.glob1(base_path, "*")
del img_paths[0]


def brigthen_image(img_path, factor):
    """Brightens up the image by the certain factor

       Args:
           img_path (string): Path to the target image
           factor (float): Factor to brighten up the image (1 is default; 1.25 is 25%)
       """
    im = Image.open(
        img_path).convert("RGB")

    enhancer = ImageEnhance.Brightness(im)

    enhancer.enhance(factor).save(
        img_path.split(".")[0] + "_enhanced.png"
    )

# Measure image colorfulness


def image_colorfulness(image):
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))
    # compute rg = R - G
    rg = np.absolute(R - G)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)
    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # derive the "colorfulness" metric and return it
    return stdRoot + (0.3 * meanRoot)


def show_brightness():

    # initialize the results list
    # print("[INFO] computing colorfulness metric for dataset...")
    results = []
    # loop over the image paths
    for imagePath in img_paths:

        imagePath = base_path + imagePath
        # load the image, resize it (to speed up computation), and
        # compute the colorfulness metric for the image
        image = cv2.imread(imagePath)
        # print("")
        # print(imagePath)
        # print("")
        image = imutils.resize(image, width=250)
        C = image_colorfulness(image)
        # display the colorfulness score on the image
        cv2.putText(image, "{:.2f}".format(C), (40, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 3)
        # add the image and colorfulness metric to the results list
        results.append((image, C, imagePath))

    # print("[INFO] displaying results...")
    results = sorted(results, key=lambda x: x[1], reverse=True)
    mostColor = [r[0] for r in results[:25]]
    leastColor = [r[0] for r in results[-25:]][::-1]

    sortedImagePaths = [r[2] for r in results]

    # print(sortedImagePaths)

    return sortedImagePaths


def compare_image(min_diff, image_1_path, image_2_path):
    minimum_commutative_image_diff = min_diff

    image_1 = cv2.imread(image_1_path, 0)
    image_2 = cv2.imread(image_2_path, 0)
    commutative_image_diff = get_image_difference(image_1, image_2)

    if commutative_image_diff < minimum_commutative_image_diff:
        # print("Matched")
        # print(commutative_image_diff)
        # return commutative_image_diff
        return True

    elif commutative_image_diff > minimum_commutative_image_diff:
        # print("No Match")
        # print(commutative_image_diff)
        # return commutative_image_diff
        return False

    else:
        # print("Failed")
        pass

    # return 10000 #random failure value


def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(
        first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(
        first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff, since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff


def select_thumbnail_images(similarity_perc):

    # if not at least 1 at the end of the loop, it executes the backup matching
    min_requirement = 0

    # pick_random_base_img

    elem = random.choice(img_paths)
    elem_path = base_path + elem

    # compare_base_to_rest

    # print(img_paths)

    for img in img_paths:

        img_path = base_path + img

        if elem_path == img_path:
            continue

        else:
            match = compare_image(similarity_perc, elem_path, img_path)

            if match == True:
                break

            else:
                pass

    img_left_path = elem_path
    img_right_path = img_path
    # print(img_left_path, img_right_path)

    sortedImages = show_brightness()

    idx = 0

    for i, img_center_path in enumerate(sortedImages):

        # create x images with the most colorful images
        # break if the image count is more than that

        if i >= 10:
            break

        match2 = compare_image(similarity_perc, img_left_path, img_center_path)

        # print(img_left_path, img_center_path)
        if match2 == True:

            # print(white_lines)

            if white_lines:
                default_img_size = 427  # 3 images - 1280px width
                # line_width = 5
                img_width = default_img_size - line_width

            else:
                img_width = 427

            if img_left_path == img_center_path:
                continue

            # Concatenation of the images
            # img_bg = Image.open('/Users/julian/tt_comp/metadata/images/thumbnail_bg.png')
            img_bg = Image.open(background_path)
            img1 = Image.open(img_left_path)
            img2 = Image.open(img_center_path)
            img3 = Image.open(img_right_path)

            img1 = img1.resize((img_width, 720))
            img2 = img2.resize((img_width, 720))
            img3 = img3.resize((img_width, 720))

            images = [img1, img2, img3]

            img_bg = img_bg.resize((1280, 720))

            # for i in range(len(images)):
            #     img_bg.paste(images[i], (430,0))
            #     img_bg.save(f"/Users/julian/tt_comp/metadata/metadata_generators/test_thumbnails/yt_thumbnail_{i+1}.png")

            # for i, url in enumerate(urls):
            # print(img_bg)

            if white_lines:
                img_bg.paste(img1, (0, 0))
                # img_bg.paste(img2, (default_img_size + line_width,0))
                # img_bg.paste(img3, (default_img_size * 2 + line_width * 2,0))
                img_bg.paste(img2, (img_width + line_width + 5, 0))
                img_bg.paste(img3, (img_width * 2 + line_width * 2 + 10, 0))
                final_img_path = target_path + f"yt_thumbnail_{idx+1}.png"
                img_bg.save(final_img_path)
                brigthen_image(final_img_path, brigthen_factor)

                idx += 1

                min_requirement += 1

            else:
                img_bg.paste(img1, (0, 0))
                # img_bg.paste(img2, (default_img_size + line_width,0))
                # img_bg.paste(img3, (default_img_size * 2 + line_width * 2,0))
                img_bg.paste(img2, (img_width, 0))
                img_bg.paste(img3, (img_width * 2, 0))
                final_img_path = target_path + f"yt_thumbnail_{idx+1}.png"
                img_bg.save(final_img_path)
                brigthen_image(final_img_path, brigthen_factor)

                idx += 1

                min_requirement += 1

        else:
            # print("No match")
            continue

     # if not at least 1 at the end of the loop, it matches a few images randomly
    if min_requirement == 0:
        select_thumbnail_images(0.8)


def backup_thumbnail():

    thumbnail_count = len(glob.glob1(target_path, "*"))

    if thumbnail_count == 0:

        img_left_path = "data/temp/images/thumbnails/thumbnail_1.jpg"
        img_center_path = "data/temp/images/thumbnails/thumbnail_2.jpg"
        img_right_path = "data/temp/images/thumbnails/thumbnail_3.jpg"

        img_bg = Image.open(background_path)
        img1 = Image.open(img_left_path)
        img2 = Image.open(img_center_path)
        img3 = Image.open(img_right_path)

        img1 = img1.resize((img_width, 720))
        img2 = img2.resize((img_width, 720))
        img3 = img3.resize((img_width, 720))

        images = [img1, img2, img3]

        img_bg = img_bg.resize((1280, 720))

        img_bg.paste(img1, (0, 0))
        img_bg.paste(img2, (img_width + line_width, 0))
        img_bg.paste(img3, (img_width * 2 + line_width * 2, 0))
        final_img_path = target_path + f"data/temp/images/thumbnails/yt_thumbnail_1.png"
        img_bg.save(final_img_path)
        brigthen_image(final_img_path, brigthen_factor)

    else:
        pass


def manual_match(left, center, right):

    background_path = "data/static/images/thumbnail_bg.png"
    # img_left_path = f"{folder_path}/thumbnails/thumbnail_{left}.jpg"
    # img_center_path = f"{folder_path}/thumbnails/thumbnail_{center}.jpg"
    # img_right_path = f"{folder_path}/thumbnails/thumbnail_{right}.jpg"

    img_left_path = "data/store/harrypotter/images/thumbnail_100.jpg"
    img_center_path = "data/store/harrypotter/images/thumbnail_5.jpg"
    img_right_path = "data/store/harrypotter/images/09182093.jpg"

    if white_lines:
        default_img_size = 427  # 3 images - 1280px width
        # line_width = 5
        img_width = default_img_size - line_width

    else:
        img_width = 427

    img_bg = Image.open(background_path)
    img1 = Image.open(img_left_path)
    img2 = Image.open(img_center_path)
    img3 = Image.open(img_right_path)

    img1 = img1.resize((img_width, 720))
    img2 = img2.resize((img_width, 720))
    img3 = img3.resize((img_width, 720))

    images = [img1, img2, img3]

    img_bg = img_bg.resize((1280, 720))

    if white_lines:
        img_bg.paste(img1, (0, 0))
        # img_bg.paste(img2, (default_img_size + line_width,0))
        # img_bg.paste(img3, (default_img_size * 2 + line_width * 2,0))
        img_bg.paste(img2, (img_width + line_width + 5, 0))
        img_bg.paste(img3, (img_width * 2 + line_width * 2 + 10, 0))
        final_img_path = target_path + f"yt_thumbnail_{1}.png"
        img_bg.save(final_img_path)
        brigthen_image(final_img_path, brigthen_factor)

    else:
        img_bg.paste(img1, (0, 0))
        # img_bg.paste(img2, (default_img_size + line_width,0))
        # img_bg.paste(img3, (default_img_size * 2 + line_width * 2,0))
        img_bg.paste(img2, (img_width, 0))
        img_bg.paste(img3, (img_width * 2, 0))
        final_img_path = target_path + \
            f"yt_thumbnail_{datetime.datetime.now()}.png"
        img_bg.save(final_img_path)
        brigthen_image(final_img_path, brigthen_factor)


if __name__ == '__main__':
    # select_thumbnail_images(0.8)  # similarity_percentage
    manual_match(3, 12, 2)
