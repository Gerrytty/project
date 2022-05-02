from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    availiable = [[i + 80 for i in range(120)],
                [i + 280 for i in range(120)],
                [i + 480 for i in range(120)],
                [i + 680 for i in range(120)],
                [i + 900 for i in range(100)],
                [i + 1100 for i in range(100)],
                [i + 1320 for i in range(80)],
                [i + 1536 for i in range(64)],
                [i + 1736 for i in range(64)],
                [i + 1936 for i in range(64)],
                [i + 2152 for i in range(48)],
                [i + 2352 for i in range(48)]]

    for i, arr in enumerate(availiable):
        plt.plot(range(0, 200), [200 * i for j in range(0, 200)])
        for point in arr:
            plt.scatter(x=point - 200 * i, y=i*200, color="black")

    plt.show()