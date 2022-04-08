import numpy as np
from matplotlib import pyplot as plt

from data_proccesing.data_preprocess import *
from data_proccesing.plots import simple_plot, slices_plot


def main():
	# data = smooth(read_data("gras_data/vm.txt"))
	bio_data_arr = read_hdf5("bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")

	for data in bio_data_arr[0:4]:
		data = norma(data)
		slices_plot(np.split(data, 6), 6, "Мотонейрон экстезор")

	plt.savefig("bio-plot.png", dpi=1800)

	# slices_plot(np.split(bio_data_arr[0], 6), 6, "out")
	# slices_plot(np.split(bio_data_arr[1], 6), 6, "out")
	plt.show()


if __name__ == "__main__":
	main()