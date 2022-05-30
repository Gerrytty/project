import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
	all_arr = []

	# all_arr = np.append(all_arr, [10])
	# all_arr = np.append(all_arr, [10])
	print(all_arr)
	# raise Exception


	i = 0

	with open("gen_weights_log_0.001", "r", buffering=100000) as file:
		for line in file:
			all_arr.append(float(line.split()[0]))
			if i > 9000 and i < 10000:
				# print(len(list(map(float, line.split()))))
				all_arr.append(np.array(list(map(float, line.split()))))
				# print(all_arr[0])
			print(i)
			i += 1

	all_arr = np.array(all_arr).T

	print(len(all_arr))

	print(all_arr[0])

	plt.title("Weight dynamic on one synapse with learning rate = 0.001:\nspike_generator_neuron->neuron")

	plt.plot(all_arr[:1000])
	plt.xlabel("time (ms)")
	plt.ylabel("weight")
	plt.xticks(range(0, 1001, 200), list(np.array(range(0, 6)) * 50))
	plt.savefig("generator_weights.png", dpi=200)
	plt.show()

	# print("plot")

	# for w in all_arr:
	# 	plt.plot(w)
	# 	plt.show()