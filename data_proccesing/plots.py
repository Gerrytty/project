from matplotlib import pyplot as plt
import numpy as np


def simple_plot(data):
    plt.plot(data)
    plt.show()


def slices_plot(splitted_data, slices_in_step, output_name, sim_step=0.1):
    plt.title(output_name)
    # сколько и как они называются
    plt.xticks(range(0, len(splitted_data[0]) + 1, 50), list(
        np.array(range(0, len(splitted_data[0]) + 1, 50)) * sim_step
    ))

    plt.yticks([i * 1.05 for i in range(1, slices_in_step + 1)], range(1, 7))

    plt.ylabel("№ слайса")
    plt.xlabel("мс")

    for i in range(0, slices_in_step):
        plt.plot(splitted_data[i] + (i * 1.05), linewidth=0.5)

    # plt.savefig(output_name, dpi=200)
    # plt.show()
    # plt.close()
    print(f"Save plot of {output_name}")