from population import Population
from random import randint
from build import Build
from analyser import Analyser
from filereader import Filereader
from individual import Individual
from filereader import HdfReader
from fitness_mono import FitnessMono

from random import choice


class GA:
    def __init__(self, available_weights, available_delays, bio_analyser):
        self.available_weights = available_weights
        self.available_delays = available_delays
        self.current_population = Population(self.available_weights, self.available_delays)
        self.current_population.init_population(30)
        self.bio_analyser = bio_analyser
        self.bests = None
        self.n_bests_we_choose = 5
        self.gen_len = 2

    def log_bests(self):
        if self.bests is not None:
            with open("bests.log", "a") as f:
                f.write(f"{self.bests[0]}\n")

    def calculate_fitness_at_population(self):
        for individual in self.current_population.individuals:
            Build.build(individual, 1, 0)
            fitness = FitnessMono.calculate_fitness(individual, self.bio_analyser,
                                                    Analyser("../GRAS/8_muscle_and_oms/vm.txt", Filereader()))

    def simple_crossover(self, individual1, individual2):
        crossover_point = randint(0, self.gen_len)
        return Individual(self.available_weights, self.available_delays,  gen=(individual1.gen[:crossover_point] + individual2.gen[crossover_point:]))

    def simple_mutation(self, individual, mutation_count=2):
        new_gen = []

        for i in range(len(individual.gen)):
            new_gen.append(individual.gen[i])

        for i in range(mutation_count):
            mutation_index = randint(0, self.gen_len * 2 - 1)
            if mutation_index < self.gen_len:
                new_gen[mutation_index] = choice(self.available_weights)
            else:
                new_gen[mutation_index] = choice(self.available_delays)

        return Individual(self.available_weights, self.available_delays, gen=new_gen, gen_size=2)

    def evolute(self):

        self.bests = self.current_population.get_bests()
        self.log_bests()

        news = []
        for best in self.bests:
            news.append(best)

        for i in range(5):
            i1_index = randint(0, self.n_bests_we_choose)
            i2_index = randint(0, self.n_bests_we_choose)
            i3_index = randint(0, self.n_bests_we_choose)

            news.append(self.simple_crossover(self.current_population.individuals[i1_index], self.current_population.individuals[i2_index]))
            news.append(self.simple_mutation(self.current_population.individuals[i3_index]))

        return Population(self.available_weights, self.available_delays, individuals=news)

    def run(self):
        # calc 50 iteration of algorithm
        for i in range(20):
            self.calculate_fitness_at_population()
            self.current_population = self.evolute()
            print(f"Iter № {i}")


if __name__ == "__main__":
    weights = [(i + 1) * 50 for i in range(100)]
    delays = [(i + 1) * 0.5 for i in range(10)]

    bio_analyser = Analyser("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5", HdfReader(0))

    ga = GA(weights, delays, bio_analyser)
    ga.run()
