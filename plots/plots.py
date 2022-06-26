from matplotlib import pyplot as plt
import numpy as np


def simple_plot(data):
    plt.plot(data)
    # plt.show()


def slices_plot(data, slices_in_step, output_name, sim_step=0.1, color=None, label=None, save=False):
    
    font = {'family': 'normal',
            'weight': 'normal',
            'size': 16}

    splitted_data = np.split(data, slices_in_step)

    plt.title(f"b)  {output_name}", font)

    len_plitted_data = len(splitted_data[0])

    y_ticks_arr = []

    plt.xticks(range(0, len_plitted_data + 1, len_plitted_data // 5), list(
        np.array(range(0, len_plitted_data + 1, len_plitted_data // 5)) * sim_step
    ), size=16)

    plt.ylabel("№ слайса", font)
    plt.xlabel("Время (мс)", font)

    for i in range(0, slices_in_step):
        y_ticks_arr.append(splitted_data[i][0] + (i * 0.3))
        if color is None:
            plt.plot(splitted_data[i] + (i * 0.3), linewidth=0.5)
        else:
            plt.plot(splitted_data[i] + (i * 0.3), linewidth=0.5, color=color)

    plt.plot([0], [0], color=color, label=label)

    print(y_ticks_arr)

    plt.yticks(y_ticks_arr, range(1, slices_in_step + 1), size=16)

    if save:
        plt.savefig(output_name, dpi=400)
        print(f"Save plot of {output_name}")
