from data_preprocess import *


class Filereader:
    def read(self, path_to_data):
        return read_data(path_to_data)


class HdfReader:

    def __init__(self, num_of_step):
        self.num_of_step = num_of_step

    def read(self, path_to_data):
        arr_of_data = []

        with h5py.File(path_to_data, "r") as f:
            # List all groups
            print("Keys: %s" % f.keys())
            for key in list(f.keys()):
                arr_of_data.append(np.array(list(f[key])))

        return np.array(arr_of_data)[self.num_of_step]