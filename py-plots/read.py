import matplotlib.pyplot as plt
import numpy as np
import pickle

slices_in_step = 22


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def plot(data, output_name):
    data = np.array(list(map(lambda x: -x, data)))
    splitted_data = np.split(data, slices_in_step)
    plt.title("48 hours later iteration with learning coeff = 0.000005")
    plt.xticks(range(0, 220, 20), list(np.array(range(0, 11)) * 5))

    arr_y_ticks = []

    for i in range(0, slices_in_step):
        arr_y_ticks.append(splitted_data[i][0] + (i * 3000))
        plt.plot(splitted_data[i] + (i * 3000), linewidth=0.5)

    print(arr_y_ticks)

    plt.yticks(arr_y_ticks, range(len(arr_y_ticks)))

    plt.savefig(output_name, dpi=200)
    plt.show()
    plt.close()
    print(f"Seved plot of {output_name}")


if __name__ == "__main__":

    current_line = 110

    with open("new_test_with_fix_out_0.000001") as file:
        for i, line in enumerate(file):
            print(i)
            if i != current_line:
                continue
            arr = np.array(list(map(float, file.readline().split())))
            # plot(arr, "0_000005")

    # with open('out_0.001') as file:
    #     print(len(file.read().split()))
    # # exit()
    # # save
    # with open('data_0_001.bin', 'wb') as file:
    #     pickle.dump(np.fromfile("out_0.001", sep=' ', dtype=float), file)
    #
    # with open('data_0_001.bin', 'rb') as file:
    #     out: np.ndarray = pickle.load(file)[4400 * 86000:4400 * 86001]
    #
    # # [4400 * 86000:4400 * 86001]
    #
    # plot(out, "out_0_001_last_plot")
    # print(out.shape)
    # plt.plot(out)
    # plt.show()
    # exit()
    # size_off_one_step = 4400
    #
    # data = []
    #
    # current_size = 0
    #
    # with open('out_0.001') as f:
    #     for piece in read_in_chunks(f):
    #         print(piece)
    #         len_of_piece = len(piece.split(" "))
    #         data.extend(list(map(lambda x: -float(x), piece.split())))
    #         current_size += len_of_piece
    #         if current_size >= size_off_one_step:
    #             break
    #
    # print(data[:4400])
    # plot(np.array(data[:4400]), "out")