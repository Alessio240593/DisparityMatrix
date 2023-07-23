import os
import warnings

import matplotlib
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import stats

ROOT_DIR = "distribution/"

warnings.filterwarnings('ignore')


def distribution_of_differences_over_time(disparities):
    destination_dir = ROOT_DIR + 'distribution_of_differences_over_time'

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for curr in range(0, (len(disparities) - 1)):
        plt.title('Disparity distribution of differences over time')
        print("Analyzing distribution of differences frame " + str(curr) + " - frame " + str(
            curr + 1) + " in progress...")

        current_frame = np.int16(disparities[curr])
        next_frame = np.int16(disparities[curr + 1])

        sub = np.subtract(current_frame, next_frame)

        sns.distplot(sub, axlabel='Pixel value')

        plot_backend = matplotlib.get_backend()
        mng = plt.get_current_fig_manager()
        if plot_backend == 'TkAgg':
            mng.resize(*mng.window.maxsize())
        elif plot_backend == 'wxAgg':
            mng.frame.Maximize(True)
        elif plot_backend == 'Qt4Agg':
            mng.window.showMaximized()

        moda = stats.mode(sub, axis=None)

        plt.text(103, 0.08, f'Max: {sub.max()}' +
                 f'\nMin: {sub.min()}' +
                 f'\nMean: {round(sub.mean(), 2)}' +
                 f'\nStd: {round(sub.std(), 2)}' +
                 f'\nMedian: {int(np.median(sub))}' +
                 f'\nMode: {moda.mode} (counts : {moda.count})', fontsize=12,
                 bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

        plt.grid()

        plt.gcf().set_size_inches((22, 13), forward=False)

        plt.savefig(destination_dir + '/frame' + str(curr) + "- frame" + str(curr + 1) + ".png", dpi=500, pad_inches=0,
                    bbox_inches='tight')

        plt.show()

        print("Analyzing distribution of differences frame " + str(curr) + " frame " + str(curr + 1) + " completed\n")


def distribution_of_frame(disparities):
    destination_dir = ROOT_DIR + 'distribution_of_frame'

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for curr in range(0, len(disparities)):
        plt.title('Disparity distribution')
        print("Analyzing distribution of frame " + str(curr) + " in progress...")

        current_frame = disparities[curr]

        sns.distplot(current_frame, axlabel='Pixel value')

        moda = stats.mode(current_frame, axis=None)

        plt.text(0, 0.05, f'Max: {current_frame.max()}' +
                 f'\nMin: {current_frame.min()}' +
                 f'\nMean: {round(current_frame.mean(), 2)}' +
                 f'\nStd: {round(current_frame.std(), 2)}' +
                 f'\nMedian: {int(np.median(current_frame))}' +
                 f'\nMode: {moda.mode} (counts : {moda.count})', fontsize=12,
                 bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

        plot_backend = matplotlib.get_backend()
        mng = plt.get_current_fig_manager()
        if plot_backend == 'TkAgg':
            mng.resize(*mng.window.maxsize())
        elif plot_backend == 'wxAgg':
            mng.frame.Maximize(True)
        elif plot_backend == 'Qt4Agg':
            mng.window.showMaximized()

        plt.grid()

        plt.gcf().set_size_inches((22, 13), forward=False)

        plt.savefig(destination_dir + '/frame' + str(curr) + ".png", dpi=500, pad_inches=0, bbox_inches='tight')

        plt.show()

        print("Analyzing distribution of frame " + str(curr) + " completed\n")


def distribution_of_rows_differences(disparities):
    destination_dir = ROOT_DIR + 'distribution_of_rows_differences'

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for curr in range(0, len(disparities)):
        plt.title('Disparity distribution of rows differences')
        print("Analyzing distribution of frame " + str(curr) + " in progress...")
        current_frame = disparities[curr]

        sub = np.zeros(current_frame.shape)

        for row in range(1, (current_frame.shape[0] - 1)):
            bottom_row = abs(np.array(current_frame[row, :] - current_frame[row + 1, :]))
            top_row = abs(np.array(current_frame[row, :] - current_frame[row - 1, :]))
            sub[row, :] = ((bottom_row + top_row) / 2)

        sub[0, :] = np.array(current_frame[0, :] - current_frame[1, :])
        sub[current_frame.shape[0] - 1, :] = np.array(
            current_frame[current_frame.shape[0] - 1, :] - current_frame[current_frame.shape[0] - 2, :])

        sub = (np.rint(sub)).astype(int)

        sns.distplot(sub[:, :])

        moda = stats.mode(sub[:, :], axis=None)

        plt.text(200, 0.13, f'Max: {sub[:, :].max()}' +
                 f'\nMin: {sub[:, :].min()}' +
                 f'\nMean: {round(sub[:, :].mean(), 2)}' +
                 f'\nStd: {round(sub[:, :].std(), 2)}' +
                 f'\nMedian: {int(np.median(sub[:, :]))}' +
                 f'\nMode: {moda.mode} (counts : {moda.count})', fontsize=12,
                 bbox=dict(boxstyle='square,pad=1', facecolor='blue', alpha=0.5))

        plot_backend = matplotlib.get_backend()
        mng = plt.get_current_fig_manager()
        if plot_backend == 'TkAgg':
            mng.resize(*mng.window.maxsize())
        elif plot_backend == 'wxAgg':
            mng.frame.Maximize(True)
        elif plot_backend == 'Qt4Agg':
            mng.window.showMaximized()

        plt.grid()

        plt.gcf().set_size_inches((22, 13), forward=False)

        plt.savefig(destination_dir + '/frame' + str(curr) + ".png", dpi=500, pad_inches=0, bbox_inches='tight')

        plt.show()

        print("Analyzing distribution of frame " + str(curr) + " completed\n")


if __name__ == '__main__':
    print("*** Distribution library ***")
else:
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)
