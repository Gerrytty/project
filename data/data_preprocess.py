import numpy as np
from scipy.signal import savgol_filter


def norma(data, min_in_data=None, max_in_data=None):
    if min_in_data is None:
        min_in_data = min(data)
    if max_in_data is None:
        max_in_data = max(data)
    return np.array(list(map(lambda x: ((x - min_in_data) / (max_in_data - min_in_data)), data)))


def split_data_by_slices(data, num_of_slice):
    return np.split(data, num_of_slice)


def smooth(data):
    return savgol_filter(data, 17, 3, mode='nearest')