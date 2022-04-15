from matplotlib import pyplot as plt

from common.data_preprocess import *
from common.plots import slices_plot, simple_plot


def main():
	data = smooth(read_data("GRAS/8_muscle_and_oms/vm.txt"))[:1100]
	data = norma(data[:1100])
	# print(len(data))
	# bio_data_arr = read_hdf5("bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5")

	# for data in bio_data_arr[0:4]:
	# 	data = norma(data)
	# 	slices_plot(np.split(data, 6), 6, "Мотонейрон экстезор")
	#
	# plt.savefig("bio-plot.png", dpi=1800)

	# slices_plot(np.split(data, 11), 11, "out")
	simple_plot(data)
	slices_plot(np.split(data, 11), 11, "out", sim_step=0.25)
	# slices_plot(np.split(bio_data_arr[1], 6), 6, "out")
	plt.show()


if __name__ == "__main__":
	main()