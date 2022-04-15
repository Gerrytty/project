from find_peaks import *
from filereader import *

if __name__ == "__main__":
    smoothed_gras_data = smooth(norma(HdfReader(0).read("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")))
    # smoothed_gras_data = smooth(norma(read_data("../gras_data/0_MN_E_left.dat")))[:1100]
    # smoothed_gras_data = smooth(norma(read_data("../gras_data/vm.txt")))[:1100]

    # smoothed_gras_data = smooth(norma(read_data("/home/yuliya/Diplom_^_^_new_v/GRAS/8_muscle_and_oms/vm.txt")))[:1100]

    peaks = find_peaks(smoothed_gras_data)
    peaks = filter_peaks(peaks, 0.01)
    plot_peaks(smoothed_gras_data, peaks, "out")

    # plt.subplot(311)
    # plt.title("a")
    # gras_data = norma(read_hdf5("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")[0][530:780])
    #
    # plot_peaks(gras_data, find_peaks(gras_data), "all_peaks.png")
    # plt.subplot(312)
    # plt.title("b")
    # plot_peaks(smoothed_gras_data, peaks, "all_peaks.png")
    #
    # plt.subplot(313)
    # plt.title("c")
    # plot_peaks(smoothed_gras_data, peaks, "all_peaks.png", True)
    #
    # plt.savefig("comaring.png", dpi=400)
    plt.show()