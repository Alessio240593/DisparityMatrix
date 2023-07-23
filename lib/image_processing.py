import os
import warnings

import cv2
import numpy as np

warnings.filterwarnings('ignore')


def from_video_to_frame(source_dir, dataset, fps=15, max_quantity=100, save=False, destination_dir="frame"):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    cap = cv2.VideoCapture(source_dir + dataset)
    cap.set(cv2.CAP_PROP_POS_FRAMES, fps)

    counts = 0
    res = []

    while cap.isOpened():
        ret, frame = cap.read()

        res.append(frame)

        if save:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            cv2.imwrite(destination_dir + "/frame" + str(counts) + ".png", frame)
            counts = counts + 1

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if len(res) == max_quantity:
            break

    cap.release()

    return res


def from_stereo_to_disparity_matrix(left_img_list, right_img_list, resolution=1.0, numDisparities=16, blockSize=5,
                                    windowSize=5, filterCap=63, lmbda=80000, sigma=1.2, brightness=0, contrast=1,
                                    save=False, destination_dir="disparity", format="png"):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    res = []
    counts = 0
    for curr in range(0, len(left_img_list)):
        imgLeft = left_img_list[curr]
        imgRight = right_img_list[curr]

        # Initialize the stereo block matching object
        left_matcher = cv2.StereoSGBM_create(minDisparity=0,
                                             numDisparities=numDisparities,
                                             blockSize=blockSize,
                                             P1=8 * 3 * windowSize ** 2,
                                             P2=32 * 3 * windowSize ** 2,
                                             disp12MaxDiff=1,
                                             uniquenessRatio=15,
                                             speckleWindowSize=0,
                                             speckleRange=2,
                                             preFilterCap=filterCap,
                                             mode=cv2.STEREO_SGBM_MODE_HH)

        right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

        wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
        wls_filter.setLambda(lmbda)
        wls_filter.setSigmaColor(sigma)

        # Step 6 - Perform stereo matching to compute disparity maps for both left and right views.
        displ = left_matcher.compute(imgLeft, imgRight)
        dispr = right_matcher.compute(imgRight, imgLeft)

        # Step 7 - Perform post-filtering
        imgLb = cv2.copyMakeBorder(imgLeft, top=0, bottom=0, left=np.uint16(numDisparities / resolution), right=0,
                                   borderType=cv2.BORDER_CONSTANT, value=[155, 155, 155])
        filteredImg = wls_filter.filter(displ, imgLb, None, dispr)

        # Step 8 - Adjust image resolution, brightness, contrast, and perform disparity truncation hack
        filteredImg = filteredImg * resolution
        filteredImg = filteredImg + (brightness / 100.0)
        filteredImg = (filteredImg - 128) * contrast + 128
        filteredImg = np.clip(filteredImg, 0, 255)
        filteredImg = np.uint8(filteredImg)

        if save:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            if format == "npy":
                np.save(destination_dir + "/disparity" + str(counts), filteredImg)
            else:
                cv2.imwrite(destination_dir + "/disparity" + str(counts) + "." + format, filteredImg)
            counts = counts + 1

        res.append(filteredImg)
    return res


if __name__ == "__main__":
    print("*** Image processing library ***")