import os
import warnings
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import stats

from lib import compression as comp

warnings.filterwarnings('ignore')

DESTINATION_JPG_RESULTS = "compression/pillow/results/jpg"
DESTINATION_PNG_RESULTS = "compression/pillow/results/png"

SOURCE_ORIGINAL_DIR_JPG = "disparity/jpg"
SOURCE_ORIGINAL_DIR_PNG = "disparity/png"

SOURCE_COMPRESSED_DIR_JPG = "compression/pillow/jpg"
SOURCE_COMPRESSED_DIR_PNG = "compression/pillow/png"

#JPG
lst = os.listdir(SOURCE_ORIGINAL_DIR_JPG)  # your directory path
number_files = len(lst)

if not os.path.exists(DESTINATION_JPG_RESULTS):
    os.makedirs(DESTINATION_JPG_RESULTS)

for curr in range(0, number_files):
    comp.compress_img(SOURCE_ORIGINAL_DIR_JPG + "/disparity" + str(curr) + ".jpg", curr)

    print("\n")

    original_img = np.int16(cv2.imread(SOURCE_ORIGINAL_DIR_JPG + "/disparity" + str(curr) + ".jpg", 0))
    compressed_img = np.int16(cv2.imread(SOURCE_COMPRESSED_DIR_JPG + "/disparity" + str(curr) + "compressed.jpg", 0))

    sub = np.subtract(original_img, compressed_img)

    sns.distplot(sub, axlabel="Difference value")

    plot_backend = matplotlib.get_backend()
    mng = plt.get_current_fig_manager()
    if plot_backend == 'TkAgg':
        mng.resize(*mng.window.maxsize())
    elif plot_backend == 'wxAgg':
        mng.frame.Maximize(True)
    elif plot_backend == 'Qt4Agg':
        mng.window.showMaximized()

    moda = stats.mode(sub, axis=None)

    plt.text(10, 1.5, f'Max: {sub.max()}' +
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

    plt.gcf().set_size_inches((22, 13), forward=False)

    plt.savefig(DESTINATION_JPG_RESULTS + '/frame' + str(curr) + ".png", dpi=500, pad_inches=0, bbox_inches='tight')

    plt.show()

plt.close()

#PNG
lst = os.listdir(SOURCE_ORIGINAL_DIR_PNG)  # your directory path
number_files = len(lst)

if not os.path.exists(DESTINATION_PNG_RESULTS):
    os.makedirs(DESTINATION_PNG_RESULTS)

for curr in range(0, number_files):
    comp.compress_img(SOURCE_ORIGINAL_DIR_PNG + "/disparity" + str(curr) + ".png", curr, to_jpg=False)

    print("\n")

    original_img = np.int16(cv2.imread(SOURCE_ORIGINAL_DIR_PNG + "/disparity" + str(curr) + ".png", 0))
    compressed_img = np.int16(cv2.imread(SOURCE_COMPRESSED_DIR_PNG + "/disparity" + str(curr) + "compressed.png", 0))

    sub = np.subtract(original_img, compressed_img)

    sns.distplot(sub, axlabel="Difference value")

    plot_backend = matplotlib.get_backend()
    mng = plt.get_current_fig_manager()
    if plot_backend == 'TkAgg':
        mng.resize(*mng.window.maxsize())
    elif plot_backend == 'wxAgg':
        mng.frame.Maximize(True)
    elif plot_backend == 'Qt4Agg':
        mng.window.showMaximized()

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

    plt.gcf().set_size_inches((22, 13), forward=False)

    plt.savefig(DESTINATION_PNG_RESULTS + '/frame' + str(curr) + ".png", dpi=500, pad_inches=0, bbox_inches='tight')

    plt.show()