from matplotlib import pyplot as plt
import numpy as np


def simple_plot(data):
    plt.plot(data)
    plt.show()


def slices_plot(splitted_data, slices_in_step, output_name, sim_step=0.1):
    plt.title(output_name)
    # сколько и как они называются

    len_plitted_data = len(splitted_data[0])

    plt.xticks(range(0, len_plitted_data + 1, len_plitted_data // 5), list(
        np.array(range(0, len_plitted_data + 1, len_plitted_data // 5)) * sim_step
    ))

    if sim_step == 0.25:
        plt.yticks([i * 0.3 for i in range(2, slices_in_step + 2)], range(1, slices_in_step + 1))

    plt.ylabel("№ слайса")
    plt.xlabel("мс")

    for i in range(0, slices_in_step):
        plt.plot(splitted_data[i] + (i * 0.3), linewidth=0.5)

    # plt.savefig(output_name, dpi=200)
    # plt.show()
    # plt.close()
    print(f"Save plot of {output_name}")