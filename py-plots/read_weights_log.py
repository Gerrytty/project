import matplotlib.pyplot as plt


if __name__ == "__main__":

    lines_arr_dt = []
    lines_arr_dw = []

    with open("logs_with_0.001/out_0.001") as file:
        for i, line in enumerate(file):
            print(i)
            arr = list(map(float, line.split()))

            if any([x != -1 for x in arr]):
                lines_arr_dt.append(list(map(float, line.split())))
            else:
                print("skip")

            if len(lines_arr_dt) >= 1000:
                break

    with open("logs_with_0.001/weights_log_0.001") as file:
        for i, line in enumerate(file):
            print(i)
            arr = list(map(float, line.split()))

            if any([x != -1 for x in arr]):
                lines_arr_dw.append(list(map(float, line.split())))
            else:
                print("skip")

            if len(lines_arr_dw) >= 1000:
                break

    print(len(lines_arr_dt))
    print(len(lines_arr_dw))

    x_array = []
    y_array = []

    for i in range(100):
        for j in range(len(lines_arr_dt[i])):
            if lines_arr_dt[i][j] != -1 and lines_arr_dw[i][j] != -1:
                x_array.append(lines_arr_dt[i][j])
                y_array.append(lines_arr_dw[i][j])

        print("-----------------")

    plt.title('Hebbian')
    plt.xlabel("Δt (ms) = (t_post  - t_pre)")
    plt.ylabel("ΔW (%)")
    # plt.xlim(-5, 5)
    # plt.ylim(-10, 10)
    plt.axvline(0, linestyle="-", color="black")
    plt.axhline(0, linestyle="-", color="black")

    plt.scatter(x=y_array, y=x_array)
    plt.savefig("hebbian_0_001.png")
    plt.show()