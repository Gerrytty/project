import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np
from data_preprocess import read_data, split_data_by_slices, smooth


def find_extrema(data):
    # for local maxima
    maximums = argrelextrema(data, np.greater)

    # for local minima
    minimums = argrelextrema(data, np.less)

    return maximums[0], minimums[0]


class Extrema:
    def __init__(self, x, y, clazz):
        self.x = x
        self.y = y
        self.clazz = clazz


class Peak:
    def __init__(self, left_min_extrema, max_extrema, right_min_extrema):
        self.left_min_extrema = left_min_extrema
        self.max_extrema = max_extrema
        self.right_min_extrema = right_min_extrema

    def __repr__(self):
        return f"({self.left_min_extrema.x}, {self.left_min_extrema.y}) ({self.max_extrema.x}, {self.max_extrema.y}) ({self.right_min_extrema.x}, {self.right_min_extrema.y})"

    def is_good(self):
        return abs(self.left_min_extrema.y - self.max_extrema.y) > 100


if __name__ == "__main__":
    gras_data = smooth(read_data("../gras_data/0_MN_E_left.dat")[:200])
    gras_data = np.diff(gras_data)
    ids_of_maxs, ids_of_mins = find_extrema(gras_data)
    maxs_elems, mins_elems = np.take(gras_data, ids_of_maxs), np.take(gras_data, ids_of_mins)

    extrema_arr = []
    for i in range(len(maxs_elems)):
        extrema_arr.append(Extrema(ids_of_maxs[i], maxs_elems[i], "max"))
        extrema_arr.append(Extrema(ids_of_mins[i], mins_elems[i], "min"))

    extrema_arr.sort(key=lambda peak: peak.x)

    peaks_arr = []

    i = 0
    while i < len(extrema_arr) - 2:
        peak = Peak(extrema_arr[i], extrema_arr[i + 1], extrema_arr[i + 2])
        if peak.is_good():
            peaks_arr.append(peak)
        # peaks_arr.append(Peak(extrema_arr[i], extrema_arr[i + 1], extrema_arr[i + 2]))
        i += 2

    for peak in peaks_arr:
        print(peak)
        plt.scatter(x=peak.left_min_extrema.x, y=peak.left_min_extrema.y, color="r")
        plt.scatter(x=peak.max_extrema.x, y=peak.max_extrema.y, color="b")
        plt.scatter(x=peak.right_min_extrema.x, y=peak.right_min_extrema.y, color="r")

    plt.plot(gras_data)
    plt.show()
