import os

import PIL
from PIL import Image

DESTINATION_DIR = "compression/pillow/"


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, curr, new_size_ratio=0.9, quality=90, width=None, height=None, to_jpg=True):
    # load the image to memory
    img = Image.open(image_name)
    # print the original image shape
    print("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(image_name)
    # print the size before compression/resizing
    print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
        img = img.resize((int(img.size[0]), int(img.size[1])), PIL.Image.LANCZOS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        #img = img.resize((width, height), PIL.Image.LANCZOS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        ext = ".jpg"

    if not os.path.exists(DESTINATION_DIR + ext[1:]):
        os.makedirs(DESTINATION_DIR + ext[1:])

    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(DESTINATION_DIR + ext[1:] + "/disparity" + str(curr) + "compressed" + ext, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(DESTINATION_DIR + ext[1:] + "/disparity" + str(curr) + "compressed" + ext, quality=quality, optimize=True)
    print("[+] New file saved:", DESTINATION_DIR + ext[1:] + "/disparity" + "0" + "compressed" + ext)
    # get the new image size in bytes
    new_image_size = os.path.getsize(DESTINATION_DIR + ext[1:] + "/disparity" + "0" + "compressed" + ext)
    # print the new size in a good format
    print("[+] Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # print the saving percentage
    print(f"[+] Image size change: {saving_diff / image_size * 100:.2f}% of the original image size.\n\n")


if __name__ == "__main__":
    print("*** Compression library ***")