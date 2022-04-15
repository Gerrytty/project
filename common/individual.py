from random import choice


class Individual:
    def __init__(self, available_weights, available_delays, gen_size=2,  gen=None, fitness=0):
        self.fitness = fitness
        self.gen_size = gen_size
        if gen is None:
            self.weights = []
            self.delays = []
            self.gen = []

            for i in range(gen_size):
                self.weights.append(choice(available_weights))
                self.delays.append(choice(available_delays))

            self.gen = self.weights + self.delays
        else:
            self.gen = gen

            self.weights = []
            self.delays = []

            for i in range(gen_size):
                self.weights.append(gen[i])
                self.delays.append(gen[i + gen_size])

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __repr__(self):
        return f"{self.fitness} {self.gen}"
