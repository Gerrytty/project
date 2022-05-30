import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    arr_time_of_pre_spikes = []
    arr_time_of_post_spikes = []
    arr_weights = []

    with open("logs_with_0.001/spike_time_pre_0.001") as file:
        for i, line in enumerate(file):
            arr_time_of_pre_spikes.append(float(line.split()[2]))

    print("--------")

    with open("spike_time_post_0.001") as file:
        for i, line in enumerate(file):
            arr_time_of_post_spikes.append(float(line.split()[2]))

    with open("weights_log_0.001") as file:
        for i, line in enumerate(file):
            arr_weights.append(float(line.split()[2]))

    # for t in range(1000):
    #     with open("weights_log_0.001") as file:
    #         for i, line in enumerate(file):
    #             arr_weights.append(float(line.split()[t]))
    #         plt.plot(arr_weights)
    #         plt.show()
    #
    # raise Exception

    arr_weights = arr_weights[:500]

    max_weight = max(arr_weights)
    min_weight = min(arr_weights)

    arr_time_of_pre_spikes = arr_time_of_pre_spikes[:500]
    arr_time_of_post_spikes = arr_time_of_post_spikes[:500]

    plt.subplot(211)
    plt.title("Динамика изменения веса на одном синапсе")
    plt.plot(arr_weights)
    plt.xlim(0, len(arr_weights))
    print(arr_weights)
    plt.subplot(212)
    plt.title("Время спайков пре и пост нейронов")
    plt.xlim(0, len(arr_weights))

    x_tics_arr = []

    for point in range(len(arr_weights)):

        print(arr_time_of_pre_spikes[point])

        if arr_time_of_post_spikes[point] != 0 and arr_time_of_pre_spikes[point] != 0:
            plt.scatter(x=arr_time_of_pre_spikes[point], y=-1, color="r")
            plt.scatter(x=arr_time_of_post_spikes[point], y=1, color="b")
            x_tics_arr.append(arr_time_of_pre_spikes[point])
            x_tics_arr.append(arr_time_of_post_spikes[point])

    plt.legend(["pre", "post"])

    plt.yticks([], [])

    figure = plt.gcf()

    figure.set_size_inches(16, 8)

    plt.savefig("weights_dynamic.png", dpi=1000)

    plt.show()

    # for i in range(len(arr_time_of_post_spikes)):
    #     pass
