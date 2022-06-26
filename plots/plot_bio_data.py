from reader.reader import HdfReader
from plots.plots import slices_plot
from data.data_preprocess import norma

import matplotlib.pyplot as plt


def plot_bio():
    colors = ["r", "g", "black", "blue"]
    lines = []

    for i in range(4):
        hdf_reader = HdfReader("bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")
        data = hdf_reader.get_data(i)
        if len(data) == 1500:
            slices_plot(norma(data), 6, "Мотонейрон экстензор", color=colors[i], label=f"крыса № {i + 1}")

    # plot poly
    plt.plot([100, 250], [0.5, 0.5], color='black', label="поли ответ", linestyle="--")
    plt.plot([180, 250], [2.2, 2.2], color='black', linestyle="--")
    plt.plot([100, 180], [0.5, 2.2], color='blue', linestyle="--")
    plt.plot([250, 250], [0.5, 2.2], color='black', linestyle="--")

    # plot mono
    plt.plot([35, 60], [0.05, 0.05], color='red', label="моно ответ", linestyle="--")
    plt.plot([35, 60], [2.5, 2.5], color='red', linestyle="--")
    plt.plot([35, 35], [0.05, 2.5], color='red', linestyle="--")
    plt.plot([60, 60], [0.05, 2.5], color='red', linestyle="--")

    legend = plt.legend(prop={'size': 9})

    for legobj in legend.legendHandles:
        legobj.set_linewidth(2.0)


if __name__ == "__main__":
    plot_bio()
    # plt.savefig("Мотонейрон_экстензор_био.png", dpi=900)
    plt.show()
