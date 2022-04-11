import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from scipy.signal import savgol_filter
import h5py


def read_data(path_to_file):
    with open(path_to_file) as file:
        return np.array(list(map(lambda x: -1 * float(x), file.readline().split())))


def read_hdf5(path_to_file):

    arr_of_data = []

    with h5py.File(path_to_file, "r") as f:
        # List all groups
        print("Keys: %s" % f.keys())
        for key in list(f.keys()):
            arr_of_data.append(np.array(list(f[key])))

    return np.array(arr_of_data)


def norma(data):
    maximum = max(data)
    minimum = min(data)
    # return preprocessing.normalize(data.reshape(-1, 1))
    return np.array(list(map(lambda x: ((x - minimum) / (maximum - minimum)), data)))


def split_data_by_slices(data, num_of_slice):
    return np.split(data, num_of_slice)


def smooth(data):
    return savgol_filter(data, 17, 3, mode='nearest')