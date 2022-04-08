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


if __name__ == "__main__":
    # gras_data = smooth(read_data("../gras_data/0_MN_E_left.dat")[:4400])
    # gras_data = norma(smooth(read_data("../gras_data/vm.txt")[:200]))
    gras_data = smooth(read_hdf5("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")[0])[:]
    print(len(gras_data))
    # print(list(gras_data))
    # gras_data = np.diff(gras_data)
    ids_of_maxs, ids_of_mins = find_extrema(gras_data)
    maxs_elems, mins_elems = np.take(gras_data, ids_of_maxs), np.take(gras_data, ids_of_mins)

    extrema_arr = []

    print(len(ids_of_maxs), len(maxs_elems))
    print(len(ids_of_mins), len(mins_elems))

    for i in range(len(mins_elems)):
        extrema_arr.append(Extrema(ids_of_mins[i], mins_elems[i], "min"))

    for i in range(len(maxs_elems)):
        extrema_arr.append(Extrema(ids_of_maxs[i], maxs_elems[i], "max"))

    extrema_arr.sort(key=lambda peak: peak.x)

    # for peak in extrema_arr:
    #     plt.scatter(x=peak.x, y=peak.y)

    peaks_arr = []

    i = 0
    while i < len(extrema_arr) - 2:
        peak = Peak(extrema_arr[i], extrema_arr[i + 1], extrema_arr[i + 2])
        if peak.is_good(0.2, 0):
            peaks_arr.append(peak)
        # peaks_arr.append(Peak(extrema_arr[i], extrema_arr[i + 1], extrema_arr[i + 2]))
        i += 2

    for i, peak in enumerate(peaks_arr):
        print(peak)
        if peak.is_good(0, 0):
            print(peak)
            plt.scatter(x=peak.left_min_extrema.x, y=peak.left_min_extrema.y, color="r")
            plt.scatter(x=peak.max_extrema.x, y=peak.max_extrema.y, color="b")
            plt.scatter(x=peak.right_min_extrema.x, y=peak.right_min_extrema.y, color="r")

            # if i == 1:
            #     plt.plot([peak.left_min_extrema.x, peak.left_min_extrema.x],
            #              [peak.max_extrema.y - 0.1, peak.left_min_extrema.y + 0.1], color="black")
            #
            #     plt.plot([peak.right_min_extrema.x, peak.right_min_extrema.x],
            #              [peak.left_min_extrema.y + 0.1, peak.max_extrema.y - 0.1], color="black")
            #
            #     plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x],
            #              [peak.max_extrema.y - 0.1, peak.max_extrema.y - 0.1], color="black")
            #
            #     plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x],
            #              [peak.left_min_extrema.y + 0.1, peak.left_min_extrema.y + 0.1], color="black")
            #
            # else:
            #     plt.plot([peak.left_min_extrema.x, peak.left_min_extrema.x], [peak.max_extrema.y - 0.1, peak.right_min_extrema.y + 0.1], color="black")
            #     plt.plot([peak.right_min_extrema.x, peak.right_min_extrema.x], [peak.max_extrema.y - 0.1, peak.right_min_extrema.y + 0.1], color="black")
            #
            #     plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x], [peak.right_min_extrema.y + 0.1, peak.right_min_extrema.y + 0.1], color="black")
            #     plt.plot([peak.left_min_extrema.x, peak.right_min_extrema.x], [peak.max_extrema.y - 0.1, peak.max_extrema.y - 0.1], color="black")

    plt.plot(gras_data)
    # plt.savefig("peaks.png", dpi=1000)
    plt.show()
