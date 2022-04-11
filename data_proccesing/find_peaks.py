import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np
from data_preprocess import *
from peak import Peak
from extrema import Extrema


def find_extrema(data):
    # for local maxima
    maximums = argrelextrema(data, np.greater)

    # for local minima
    minimums = argrelextrema(data, np.less)

    return maximums[0], minimums[0]


def find_peaks(data):
    ids_of_maxs, ids_of_mins = find_extrema(data)
    maxs_elems, mins_elems = np.take(data, ids_of_maxs), np.take(data, ids_of_mins)

    extrema_arr = []

    for i in range(len(mins_elems)):
        extrema_arr.append(Extrema(ids_of_mins[i], mins_elems[i], "min"))

    for i in range(len(maxs_elems)):
        extrema_arr.append(Extrema(ids_of_maxs[i], maxs_elems[i], "max"))

    extrema_arr.sort(key=lambda peak: peak.x)

    if extrema_arr[0].clazz == "min":
        extrema_arr.insert(0, Extrema(0, gras_data[0], "max"))

    if extrema_arr[-1].clazz == "min":
        extrema_arr.append(Extrema(len(gras_data), gras_data[-1], "max"))

    peaks_arr = []

    for i, extrema in enumerate(extrema_arr):
        if extrema.clazz == "min":
            peaks_arr.append(Peak(extrema_arr[i - 1], extrema, extrema_arr[i + 1]))

    return np.array(peaks_arr)


def filter_peaks(peaks_arr):
    return np.where([item.is_good() for item in peaks_arr], peaks_arr)


def plot_peaks(data, peaks_arr, filename, plot_boxes=False):

    plt.plot(data)

    for i, peak in enumerate(peaks_arr):

        plt.scatter(x=peak.left_min_extrema.x, y=peak.left_min_extrema.y, color="r")
        plt.scatter(x=peak.max_extrema.x, y=peak.max_extrema.y, color="b")
        plt.scatter(x=peak.right_min_extrema.x, y=peak.right_min_extrema.y, color="r")

        if plot_boxes:
            if peak.left_min_extrema.y > peak.right_min_extrema.y:
                plt.plot([peak.left_min_extrema.x, peak.left_min_extrema.x],
                         [peak.max_extrema.y - 0.1, peak.left_min_extrema.y + 0.1], color="black")
                plt.plot([peak.right_min_extrema.x, peak.right_min_extrema.x],
                         [peak.left_min_extrema.y + 0.1, peak.max_extrema.y - 0.1], color="black")
                plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x],
                         [peak.max_extrema.y - 0.1, peak.max_extrema.y - 0.1], color="black")
                plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x],
                         [peak.left_min_extrema.y + 0.1, peak.left_min_extrema.y + 0.1], color="black")
            else:
                plt.plot([peak.left_min_extrema.x, peak.left_min_extrema.x],
                         [peak.max_extrema.y - 0.1, peak.right_min_extrema.y + 0.1], color="black")
                plt.plot([peak.right_min_extrema.x, peak.right_min_extrema.x],
                         [peak.max_extrema.y - 0.1, peak.right_min_extrema.y + 0.1], color="black")
                plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x],
                         [peak.right_min_extrema.y + 0.1, peak.right_min_extrema.y + 0.1], color="black")
                plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x],
                         [peak.max_extrema.y - 0.1, peak.max_extrema.y - 0.1], color="black")

    plt.savefig(filename, dpi=400)
    plt.show()


if __name__ == "__main__":
    # gras_data = smooth(read_data("../gras_data/0_MN_E_left.dat")[:4400])
    # gras_data = norma(smooth(read_data("../gras_data/vm.txt")[:1500]))
    gras_data = smooth(norma(read_hdf5("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")[0][:400]))
    # gras_data = read_hdf5("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")[0][:400]
    peaks = find_peaks(gras_data)
    peaks = filter_peaks(peaks)

    plot_peaks(gras_data, peaks, "filtered_peaks.png")
