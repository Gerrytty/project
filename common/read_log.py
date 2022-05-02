

class Log:
    def __init__(self, fitness_func=None, plus_peaks=None, minus_peaks=None, weight_and_delays=None):
        if fitness_func is None:
            self.fitness_func = []
            self.plus_peaks = []
            self.minus_peaks = []
            self.weight_and_delays = []
        else:
            self.fitness_func = fitness_func
            self.plus_peaks = plus_peaks
            self.minus_peaks = minus_peaks


def read_log_file(path_to_log_file):

    log = Log()

    with open(path_to_log_file) as file:
        for line in file:
            line_arr = list(map(float, line.split()))
            log.fitness_func.append(line_arr[0])
            log.plus_peaks.append(line_arr[1])
            log.minus_peaks.append(line_arr[2])
            log.weight_and_delays.append(line_arr[2:])

    return log


if __name__ == "__main__":
    log = read_log_file("out.txt")

    print(log.fitness_func)