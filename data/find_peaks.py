import matplotlib.pyplot as plt

from scipy.signal import argrelextrema
from data.peak import Peak
from data.extrema import Extrema
import numpy as np


def find_extrema(data):
    # for local maxima
    maximums = argrelextrema(data, np.greater)

    # for local minima
    minimums = argrelextrema(data, np.less)

    return maximums[0], minimums[0]


def find_peaks(data, step):
    ids_of_maxs, ids_of_mins = find_extrema(data)
    maxs_elems, mins_elems = np.take(data, ids_of_maxs), np.take(data, ids_of_mins)

    if len(mins_elems) == 0 or len(maxs_elems) == 0:
        return []

    extrema_arr = []

    for i in range(len(mins_elems)):
        extrema_arr.append(Extrema(ids_of_mins[i], mins_elems[i], "min", step))

    for i in range(len(maxs_elems)):
        extrema_arr.append(Extrema(ids_of_maxs[i], maxs_elems[i], "max", step))

    extrema_arr.sort(key=lambda peak: peak.x)

    if extrema_arr[0].clazz == "min":
        extrema_arr.insert(0, Extrema(0, data[0], "max", step))

    if extrema_arr[-1].clazz == "min":
        extrema_arr.append(Extrema(len(data), data[-1], "max", step))

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


def find_peaks_and_filter(data, step):
    peaks = find_peaks(data, step)
    peaks = filter_peaks(peaks, 0.06)
    return peaks


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
