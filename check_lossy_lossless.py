import os

import cv2
import matplotlib
import numpy as np
from scipy import stats
from lib import image_processing as imgProc
import seaborn as sns
from matplotlib import pyplot as plt


MAX_QUANTITY = 2

DIRECTORY_JPG = "disparity/jpg"
DIRECTORY_PNG = "disparity/png"
DIRECTORY_NPY = "disparity/npy"

DESTINATION_DIR_JPG = "lossy_lossless_comparision/matix_to_jpg"
DESTINATION_DIR_PNG = "lossy_lossless_comparision/matix_to_png"
DESTINATION_DIR_NPY = "lossy_lossless_comparision/matix_to_npy"
DESTINATION_DIR_ALL_FORMATS = "lossy_lossless_comparision/all_formats"

if __name__ == "__main__":
    left_img_list = imgProc.from_video_to_frame('dataset', '/befine_7cam_multip_left.mp4', max_quantity=MAX_QUANTITY)
    right_img_list = imgProc.from_video_to_frame('dataset', '/befine_7cam_multip_right.mp4', max_quantity=MAX_QUANTITY)
    disparities = imgProc.from_stereo_to_disparity_matrix(left_img_list, right_img_list, save=True,
                                                          destination_dir="disparity/jpg", format="jpg")
    imgProc.from_stereo_to_disparity_matrix(left_img_list, right_img_list, save=True,
                                            destination_dir="disparity/png", format="png")
    imgProc.from_stereo_to_disparity_matrix(left_img_list, right_img_list, save=True,
                                            destination_dir="disparity/npy", format="npy")

    int16_disparities = [np.int16(el) for el in disparities]
    curr = 0

    if not os.path.exists(DESTINATION_DIR_ALL_FORMATS):
        os.makedirs(DESTINATION_DIR_ALL_FORMATS)

    for filename in sorted(os.listdir(DIRECTORY_JPG)):
        print("Analyzing distribution of frame " + str(curr) + " in progress...")

        path_jpg = os.path.join(DIRECTORY_JPG, "disparity" + str(curr) + ".jpg")
        path_png = os.path.join(DIRECTORY_PNG,  "disparity" + str(curr) + ".png")
        path_npy = os.path.join(DIRECTORY_NPY,  "disparity" + str(curr) + ".npy")

        # checking if it is a file
        if os.path.isfile(path_jpg) and os.path.isfile(path_png) and os.path.isfile(path_npy):
            jpg = np.int16(cv2.imread(path_jpg, 0))
            png = np.int16(cv2.imread(path_png, 0))
            npy = np.int16(np.load(path_npy))

            sub_jpg = np.subtract(int16_disparities[curr], jpg)
            sub_png = np.subtract(int16_disparities[curr], png)
            sub_npy = np.subtract(int16_disparities[curr], npy)

            fig, ax = plt.subplots(1, 3)
            plt.title('Difference between original matrix and other formats')

            ax[0].set_title("From original matrix to jpg")
            sns.distplot(sub_jpg, axlabel="Pixel value", ax=ax[0])

            ax[1].set_title("From original matrix to png")
            sns.distplot(sub_png, axlabel="Pixel value", ax=ax[1])

            ax[2].set_title("From original matrix to npy")
            sns.distplot(sub_npy, axlabel="Pixel value", ax=ax[2])

            moda_jpg = stats.mode(sub_jpg, axis=None)
            moda_png = stats.mode(sub_png, axis=None)
            moda_npy = stats.mode(sub_npy, axis=None)


            ax[0].text(3, 4, f'Max: {sub_jpg.max()}' +
                     f'\nMin: {sub_jpg.min()}' +
                     f'\nMean: {round(sub_jpg.mean(), 2)}' +
                     f'\nStd: {round(sub_jpg.std(), 2)}' +
                     f'\nMedian: {int(np.median(sub_jpg))}' +
                     f'\nMode: {moda_jpg.mode} (counts : {moda_jpg.count})' +
                     f'\nTotal pixels: {sub_jpg.size}' +
                     f'\nOutlayer: {sub_jpg.size - moda_jpg.count}'
                     , fontsize=8,
                     bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

            ax[1].text(0.1, 35, f'Max: {sub_png.max()}' +
                       f'\nMin: {sub_png.min()}' +
                       f'\nMean: {round(sub_png.mean(), 2)}' +
                       f'\nStd: {round(sub_png.std(), 2)}' +
                       f'\nMedian: {int(np.median(sub_png))}' +
                       f'\nMode: {moda_png.mode} (counts : {moda_png.count})' +
                       f'\nTotal pixels: {sub_png.size}' +
                       f'\nOutlayer: {sub_png.size - moda_png.count}'
                       , fontsize=8,
                       bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

            ax[2].text(0.1, 35, f'Max: {sub_npy.max()}' +
                       f'\nMin: {sub_npy.min()}' +
                       f'\nMean: {round(sub_npy.mean(), 2)}' +
                       f'\nStd: {round(sub_npy.std(), 2)}' +
                       f'\nMedian: {int(np.median(sub_npy))}' +
                       f'\nMode: {moda_npy.mode} (counts : {moda_npy.count})' +
                       f'\nTotal pixels: {sub_npy.size}' +
                       f'\nOutlayer: {sub_npy.size - moda_npy.count}'
                       , fontsize=8,
                       bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

            ax[0].grid()
            ax[1].grid()
            ax[2].grid()

            plot_backend = matplotlib.get_backend()
            mng = plt.get_current_fig_manager()
            if plot_backend == 'TkAgg':
                mng.resize(*mng.window.maxsize())
            elif plot_backend == 'wxAgg':
                mng.frame.Maximize(True)
            elif plot_backend == 'Qt4Agg':
                mng.window.showMaximized()

            plt.gcf().set_size_inches((22, 13), forward=False)

            plt.savefig(DESTINATION_DIR_ALL_FORMATS + '/frame' + str(curr) + ".png", dpi=500,
                        pad_inches=0,
                        bbox_inches='tight')

            #plt.show()

            cv2.waitKey()

            print("Analyzing distribution of frame " + str(curr) + " completed\n")

            curr = curr + 1



    # JPG
    curr = 0
    if not os.path.exists(DESTINATION_DIR_JPG):
        os.makedirs(DESTINATION_DIR_JPG)

    for filename in sorted(os.listdir(DIRECTORY_JPG)):
        plt.title('Difference between original matrix and jpg')
        print("Analyzing distribution of frame " + str(curr) + " in progress...")
        f = os.path.join(DIRECTORY_JPG, filename)
        # checking if it is a file
        if os.path.isfile(f):
            jpg = np.int16(cv2.imread(f, 0))
            sub = np.subtract(int16_disparities[curr], jpg)
            sns.distplot(sub, axlabel="Pixel value")

            moda = stats.mode(sub, axis=None)

            plt.text(0.2, 35, f'Max: {sub.max()}' +
                     f'\nMin: {sub.min()}' +
                     f'\nMean: {round(sub.mean(), 2)}' +
                     f'\nStd: {round(sub.std(), 2)}' +
                     f'\nMedian: {int(np.median(sub))}' +
                     f'\nMode: {moda.mode} (counts : {moda.count})' +
                     f'\nTotal pixels: {sub.size}' +
                     f'\nOutlayer: {sub.size - moda.count}'
                     , fontsize=12,
                     bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

            plt.grid()

            plot_backend = matplotlib.get_backend()
            mng = plt.get_current_fig_manager()
            if plot_backend == 'TkAgg':
                mng.resize(*mng.window.maxsize())
            elif plot_backend == 'wxAgg':
                mng.frame.Maximize(True)
            elif plot_backend == 'Qt4Agg':
                mng.window.showMaximized()

            plt.gcf().set_size_inches((22, 13), forward=False)

            plt.savefig(DESTINATION_DIR_JPG + '/frame' + str(curr) + ".png", dpi=500,
                        pad_inches=0,
                        bbox_inches='tight')

            #plt.show()

            cv2.waitKey()

            print("Analyzing distribution of frame " + str(curr) + " completed\n")

            curr = curr + 1


    #PNG
    curr = 0
    if not os.path.exists(DESTINATION_DIR_PNG):
        os.makedirs(DESTINATION_DIR_PNG)

    for filename in sorted(os.listdir(DIRECTORY_PNG)):
        plt.title('Difference between original matrix and png')
        print("Analyzing distribution of frame " + str(curr) + " in progress...")
        f = os.path.join(DIRECTORY_PNG, filename)
        # checking if it is a file
        if os.path.isfile(f):
            png = np.int16(cv2.imread(f, 0))
            sub = np.subtract(int16_disparities[curr], png)
            sns.distplot(sub, axlabel="Pixel value")

            moda = stats.mode(sub, axis=None)

            plt.text(0.2, 35, f'Max: {sub.max()}' +
                     f'\nMin: {sub.min()}' +
                     f'\nMean: {round(sub.mean(), 2)}' +
                     f'\nStd: {round(sub.std(), 2)}' +
                     f'\nMedian: {int(np.median(sub))}' +
                     f'\nMode: {moda.mode} (counts : {moda.count})' +
                     f'\nTotal pixels: {sub.size}' +
                     f'\nOutlayer: {sub.size - moda.count}'
                     , fontsize=12,
                     bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

            plt.grid()

            plot_backend = matplotlib.get_backend()
            mng = plt.get_current_fig_manager()
            if plot_backend == 'TkAgg':
                mng.resize(*mng.window.maxsize())
            elif plot_backend == 'wxAgg':
                mng.frame.Maximize(True)
            elif plot_backend == 'Qt4Agg':
                mng.window.showMaximized()

            plt.gcf().set_size_inches((22, 13), forward=False)

            plt.savefig(DESTINATION_DIR_PNG + '/frame' + str(curr) + ".png", dpi=500,
                        pad_inches=0,
                        bbox_inches='tight')

            #plt.show()

            cv2.waitKey()

            curr = curr + 1

            print("Analyzing distribution of frame " + str(curr) + " completed\n")


    # NPY

    curr = 0
    if not os.path.exists(DESTINATION_DIR_NPY):
        os.makedirs(DESTINATION_DIR_NPY)

    for filename in sorted(os.listdir(DIRECTORY_NPY)):
        plt.title('Difference between original matrix and npy')
        print("Analyzing distribution of frame " + str(curr) + " in progress...")
        f = os.path.join(DIRECTORY_NPY, filename)
        # checking if it is a file
        if os.path.isfile(f):
            npy = np.int16(np.load(f))
            sub = np.subtract(int16_disparities[curr], npy)
            sns.distplot(sub, axlabel="Pixel value")

            moda = stats.mode(sub, axis=None)

            plt.text(0.2, 35, f'Max: {sub.max()}' +
                     f'\nMin: {sub.min()}' +
                     f'\nMean: {round(sub.mean(), 2)}' +
                     f'\nStd: {round(sub.std(), 2)}' +
                     f'\nMedian: {int(np.median(sub))}' +
                     f'\nMode: {moda.mode} (counts : {moda.count})' +
                     f'\nTotal pixels: {sub.size}' +
                     f'\nOutlayer: {sub.size - moda.count}'
                     , fontsize=12,
                     bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

            plt.grid()

            plot_backend = matplotlib.get_backend()
            mng = plt.get_current_fig_manager()
            if plot_backend == 'TkAgg':
                mng.resize(*mng.window.maxsize())
            elif plot_backend == 'wxAgg':
                mng.frame.Maximize(True)
            elif plot_backend == 'Qt4Agg':
                mng.window.showMaximized()

            plt.gcf().set_size_inches((22, 13), forward=False)

            plt.savefig(DESTINATION_DIR_NPY + '/frame' + str(curr) + ".png", dpi=500,
                        pad_inches=0,
                        bbox_inches='tight')

            #plt.show()

            cv2.waitKey()

            curr = curr + 1

            print("Analyzing distribution of frame " + str(curr) + " completed\n")