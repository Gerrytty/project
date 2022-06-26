from random import choice


class Individual:
    def __init__(self, available_weights, available_delays, gen_size=2,  gen=None, fitness=0):
        # todo make it class
        self.fitness = fitness
        self.gen_size = gen_size
        self.born_from = None
        self.current_population_num = 0
        self.all_population_len = 0

        if gen is None:
            self.weights = [choice(available_weights) for _ in range(gen_size)]
            self.delays = [choice(available_delays) for _ in range(gen_size)]
            self.gen = self.weights + self.delays
        else:
            self.gen = gen
            self.weights = gen[:self.gen_size]
            self.delays = gen[self.gen_size:]

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __repr__(self):
        return f"{self.fitness} {self.gen}"
