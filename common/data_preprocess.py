import numpy as np
from scipy.signal import savgol_filter
import h5py


def read_data(path_to_file):
    with open(path_to_file) as file:
        return np.array(list(map(lambda x: -1 * float(x), file.readline().split())))


def norma(data):
    maximum = max(data)
    minimum = min(data)
    return np.array(list(map(lambda x: ((x - minimum) / (maximum - minimum)), data)))


def split_data_by_slices(data, num_of_slice):
    return np.split(data, num_of_slice)


def smooth(data):
    return savgol_filter(data, 17, 3, mode='nearest')