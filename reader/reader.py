import numpy as np
import h5py


class Reader:
    def __init__(self, path):
        self.path = path
        self.data = []

    def read(self) -> np.ndarray:
        pass

    def get_data(self) -> np.ndarray:
        pass


class FileReader(Reader):
    def __init__(self, path):
        super().__init__(path)
        self.read()

    def read(self) -> np.ndarray:
        with open(self.path) as file:
            arr = np.array(list(map(lambda x: -1 * float(x), file.readline().split())))
            self.data = arr
        return arr

    def get_data(self, *args):
        return self.data


class HdfReader(Reader):

    def __init__(self, path):
        super().__init__(path)
        self.read()

    def read(self):
        arr_of_data = []

        with h5py.File(self.path, "r") as f:
            # List all groups
            # print("Keys: %s" % f.keys())
            for key in list(f.keys()):
                arr_of_data.append(np.array(list(f[key])))

        self.data = arr_of_data

        return np.array(arr_of_data)

    def get_data(self, step=0) -> np.ndarray:
        return self.data[step]
