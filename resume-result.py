import matplotlib.pyplot as plt
import random


def generate_spikes_time(start, end):

    spikes_arr_x = []
    spikes_arr_y = []

    for i in range(1000):
        random_x = random.randint(0, 100)
        if start <= random_x <= end:
            percentage_of_spike_stays = 90
        else:
            percentage_of_spike_stays = 10

        spike_stay = random.randint(0, 100)

        if spike_stay <= percentage_of_spike_stays:
            spikes_arr_x.append(random_x)
            spikes_arr_y.append(random.random())

    return spikes_arr_x, spikes_arr_y


if __name__ == "__main__":
    # plt.subplot(211)
    # ax1 = plt.gca()
    # ax1.title.set_text('Экстензор')
    # x, y = generate_spikes_time(70, 100)
    # plt.scatter(x=x, y=y, linewidths=0.05)
    # plt.subplot(212)
    # ax1 = plt.gca()
    # ax1.title.set_text('Флексор')
    # x, y = generate_spikes_time(20, 50)
    # plt.scatter(x=x, y=y, linewidths=0.05)
    # plt.savefig("resume-cpg.png", dpi=1000)

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 4), dpi=80)

    axes.flat[0].title.set_text('Экстензор')
    x, y = generate_spikes_time(70, 80)
    axes.flat[0].scatter(x=x, y=y, linewidths=0.05)

    axes.flat[1].title.set_text('Флексор')
    x, y = generate_spikes_time(20, 50)
    axes.flat[1].scatter(x=x, y=y, linewidths=0.05)

    fig.tight_layout()
    plt.savefig("resume.png")
    plt.show()
