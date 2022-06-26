from data.data_preprocess import *
from data.find_peaks import *
from reader.reader import HdfReader
import math


class Analyser:
    def __init__(self, sim_step, smooth_func=smooth, norma_func=norma, find_peaks_func=find_peaks_and_filter):
        self.sim_step = sim_step
        self.smooth_func = smooth_func
        self.norma_func = norma_func
        self.find_peaks_func = find_peaks_func
        self.splitted_peaks = None
        self.peaks = None
        self.data = None

    def analyse_data(self, data):
        self.data = self.norma_func(self.smooth_func(data))
        self.peaks = self.find_peaks_func(self.data, self.sim_step)
        return self.peaks

    def split_peaks_by_slices(self, slice_len_in_ms, count_slices):
        splitted_arr = [[] for _ in range(count_slices)]

        if not self.peaks:
            return splitted_arr

        i = 0
        current_slice = slice_len_in_ms
        current_num_slice = 0
        while current_num_slice < count_slices:

            if i >= len(self.peaks):
                break

            if self.peaks[i].left_min_extrema.x < current_slice:
                splitted_arr[current_num_slice].append(self.peaks[i])
                i += 1
            else:
                current_slice += slice_len_in_ms
                current_num_slice += 1

        self.splitted_peaks = splitted_arr

        return splitted_arr


class BioAnalyser:

    def __init__(self, path_to_data, step=0.1):
        self.peaks = []
        self.reader = HdfReader(path_to_data)
        self.step = step
        self.merge_peaks()

    def merge_peaks(self):
        all_peaks = []

        for i in range(len(self.reader.data)):
            data = self.reader.get_data(i)
            if len(data) == 1500:
                analyser = Analyser(self.step)
                peaks = analyser.analyse_data(data)
                all_peaks.extend(list(peaks))

        all_peaks.sort(key=lambda x: x.max_extrema.x)

        self.peaks = all_peaks

    def find_nearest_peak(self, target_peak):
        nearest_peak_dist = self.dist(target_peak, self.peaks[0])
        for peak in self.peaks[1:]:
            peak_dist = self.dist(peak, target_peak)
            if peak_dist < nearest_peak_dist:
                nearest_peak_dist = peak_dist

    def dist(self, peak1, peak2):
        return math.sqrt((peak1.max_extrema.x - peak2.max_extrema.y) ** 2)


class Target:
    def __init__(self):
        self.peaks = [i + 80 for i in range(120)] + \
                     [i + 280 for i in range(120)] + \
                     [i + 480 for i in range(120)] + \
                     [i + 680 for i in range(120)] + \
                     [i + 920 for i in range(100)] + \
                     [i + 1120 for i in range(100)] + \
                     [i + 1330 for i in range(80)] + \
                     [i + 1536 for i in range(64)] + \
                     [i + 1736 for i in range(64)] + \
                     [i + 1936 for i in range(64)] + \
                     [i + 2152 for i in range(48)] + \
                     [i + 2352 for i in range(48)] + \
                     [40 + i * 200 for i in range(0, 11)]

        peaks = []

        for peak in self.peaks:
            peaks.append(peak * 0.25)

        self.peaks = set(peaks)