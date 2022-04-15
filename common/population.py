from individual import Individual


class Population:

    def __init__(self, available_weights, available_delays, gen_size=2, individuals=None):

        self.available_weights = available_weights
        self.available_delays = available_delays
        self.gen_size = gen_size

        if individuals is None:
            self.individuals = []
        else:
            self.individuals = individuals

    def init_population(self, population_size=30):
        self.individuals = [Individual(self.available_weights, self.available_delays, self.gen_size) for _ in range(population_size)]

    def get_bests(self, n=5):
        return sorted(self.individuals)[:n]

    def __repr__(self):
        return " ".join(str(self.individuals))
