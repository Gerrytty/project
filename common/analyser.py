from common.find_peaks import *


class Analyser:
    def __init__(self, path_to_data, reader, need_filter_peaks=True, filter_factor=0.01):
        self.path_to_data = path_to_data
        self.data = reader.read(path_to_data)
        self.data = smooth(self.data)
        self.data = norma(self.data)
        self.peaks = find_peaks(self.data)
        
        if need_filter_peaks:
            self.peaks = filter_peaks(self.peaks, filter_factor)

        self.splitted_peaks = None

    def split_peaks_by_slices(self, slice_len_in_steps, count_slices):
        splitted_arr = [[] for _ in range(count_slices)]

        if not self.peaks:
            return splitted_arr

        i = 0
        current_slice = slice_len_in_steps
        current_num_slice = 0
        while current_num_slice < count_slices:
            if self.peaks[i].left_min_extrema.x < current_slice:
                splitted_arr[current_num_slice].append(self.peaks[i])
                i += 1
            else:
                current_slice += slice_len_in_steps
                current_num_slice += 1

        self.splitted_peaks = splitted_arr

        return splitted_arr
