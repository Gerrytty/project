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
        extrema_arr.insert(0, Extrema(0, data[0], "max"))

    if extrema_arr[-1].clazz == "min":
        extrema_arr.append(Extrema(len(data), data[-1], "max"))

    peaks_arr = []

    for i, extrema in enumerate(extrema_arr):
        if extrema.clazz == "min":
            peak = Peak(extrema_arr[i - 1], extrema, extrema_arr[i + 1])
            peaks_arr.append(peak)

    return np.array(peaks_arr)


def filter_peaks(peaks_arr, threshold):

    arr = []

    for peak in peaks_arr:
        if peak.is_good(threshold):
            arr.append(peak)

    return arr

    # return np.where([item.is_good(threshold) for item in peaks_arr], peaks_arr)


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

def split_peaks_by_slices(peaks_arr, slice_len_in_steps, count_slices):
    splitted_arr = [[] for _ in range(count_slices)]

    i = 0
    current_slice = slice_len_in_steps
    current_num_slice = 0
    while current_num_slice < count_slices:
        if peaks_arr[i].left_min_extrema.x < current_slice:
            splitted_arr[current_num_slice].append(peaks_arr[i])
            i += 1
        else:
            current_slice += slice_len_in_steps
            current_num_slice += 1

    return splitted_arr


if __name__ == "__main__":
    smoothed_gras_data = smooth(norma(read_hdf5("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")[0][530:780]))
    peaks = find_peaks(smoothed_gras_data)
    peaks = filter_peaks(peaks, 0.01)

    # splitted = split_peaks_by_slices(peaks, 25 * 4, 6)

    plt.subplot(311)
    plt.title("a")
    gras_data = norma(read_hdf5("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")[0][530:780])

    plot_peaks(gras_data, find_peaks(gras_data), "all_peaks.png")
    plt.subplot(312)
    plt.title("b")
    plot_peaks(smoothed_gras_data, peaks, "all_peaks.png")

    plt.subplot(313)
    plt.title("c")
    plot_peaks(smoothed_gras_data, peaks, "all_peaks.png", True)

    plt.savefig("comaring.png", dpi=400)
    plt.show()
