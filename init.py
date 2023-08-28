import os

from lib import image_processing as imgProc
from lib import compression as comp

MAX_QUANTITY = 10
SOURCE_ORIGINAL_DIR_PNG = "disparity/png"
SOURCE_COMPRESSED_DIR_PNG = "compression/pillow/png"


def disparity_compression():
    if not os.path.exists(SOURCE_ORIGINAL_DIR_PNG):
        os.makedirs(SOURCE_ORIGINAL_DIR_PNG)

    if not os.path.exists(SOURCE_COMPRESSED_DIR_PNG):
        os.makedirs(SOURCE_COMPRESSED_DIR_PNG)

    left_img_list = imgProc.from_video_to_frame('dataset', '/befine_7cam_multip_left.mp4', max_quantity=MAX_QUANTITY)
    right_img_list = imgProc.from_video_to_frame('dataset', '/befine_7cam_multip_right.mp4', max_quantity=MAX_QUANTITY)
    imgProc.from_stereo_to_disparity_matrix(left_img_list, right_img_list, save=True,
                                            destination_dir="disparity/png", format="png")

    lst = os.listdir(SOURCE_ORIGINAL_DIR_PNG)  # your directory path
    number_files = len(lst)

    for curr in range(0, number_files):
        comp.compress_img(SOURCE_ORIGINAL_DIR_PNG + "/disparity" + str(curr) + ".png", curr, to_jpg=False)


if __name__ == '__main__':
    disparity_compression()