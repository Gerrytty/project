import numpy as np
from scipy.signal import savgol_filter


def read_data(path_to_file):
    with open(path_to_file) as file:
        return np.array(list(map(float, file.readline().split())))


def split_data_by_slices(data, num_of_slice):
    return np.split(data, num_of_slice)


def smooth(data):
    return savgol_filter(data, 17, 3, mode='nearest')