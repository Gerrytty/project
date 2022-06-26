from ga.population import Population
from ga.individual import Individual
from grpc_client.client import make_message

from random import randint
from random import choice


class GA:
    def __init__(self, gen_len, count_of_populations, available_weights, available_delays, build, sender):
        self.available_weights = available_weights
        self.available_delays = available_delays
        self.gen_len = gen_len
        self.current_population = Population(self.available_weights, self.available_delays, gen_size=self.gen_len)
        self.current_population.init_population(100)
        self.bests = None
        self.n_bests_we_choose = 20
        self.builder = build
        self.current_population_num = 0
        self.count_of_populations = count_of_populations
        self.sender = sender
        sender.start()

    def log_bests(self):
        if self.bests is not None:
            with open("bests.log", "a") as file:
                file.write(f"{self.bests[0]}\n")

    def calculate_fitness_at_population(self):
        for individual in self.current_population.individuals:
            individual.current_population_num = self.current_population_num
            individual.all_population_len = self.count_of_populations

        self.builder.calculate(self.current_population.individuals)

    def one_point_crossover(self, individual1, individual2):
        crossover_point = randint(1, self.gen_len - 1)
        return Individual(self.available_weights, self.available_delays, gen=(individual1.gen[:crossover_point]
                                                                              + individual2.gen[crossover_point:]))

    def two_point_crossover(self, individual1, individual2):
        crossover_point_1 = randint(1, self.gen_len - 2)
        crossover_point_2 = randint(crossover_point_1 + 1, self.gen_len - 1)

        new_gen = individual1.gen[:crossover_point_1] + individual2.gen[
                                                        crossover_point_1:crossover_point_2] + individual1.gen[
                                                                                               crossover_point_2:]

        return Individual(self.available_weights, self.available_delays, gen=new_gen)

    def mutation(self, individual, mutation_count=5):
        new_gen = individual.gen.copy()

        count_of_mutation_in_gen = randint(1, mutation_count)

        for i in range(count_of_mutation_in_gen):
            mutation_index = randint(0, self.gen_len * 2 - 1)
            if mutation_index < self.gen_len:
                random_weight = choice(self.available_weights)
                print(random_weight, mutation_index)
                new_gen[mutation_index] = random_weight
            else:
                random_delay = choice(self.available_delays)
                print(new_gen)
                print(random_delay, mutation_index)
                new_gen[mutation_index] = random_delay

        return Individual(self.available_weights, self.available_delays, gen=new_gen, gen_size=self.gen_len)

    def indexed_mutation(self, individual, mutation_count=5):
        new_gen = individual.gen.copy()

        for i in range(mutation_count):
            mutation_index = randint(0, self.gen_len * 2 - 1)
            if mutation_index < self.gen_len:
                weight_index = self.available_weights.index(new_gen[mutation_index])
                if weight_index >= 4:
                    new_gen[mutation_index] = choice(self.available_weights[weight_index - 4:weight_index + 4])
                else:
                    new_gen[mutation_index] = choice(self.available_weights[:weight_index + 4])
            else:
                delay_index = self.available_delays.index(new_gen[mutation_index])
                if delay_index >= 4:
                    new_gen[mutation_index] = choice(self.available_delays
                                                     [delay_index - 4:
                                                      self.available_delays.index(new_gen[mutation_index]) + 4])
                else:
                    new_gen[mutation_index] = choice(self.available_delays
                                                     [:self.available_delays.index(new_gen[mutation_index]) + 4])

        return Individual(self.available_weights, self.available_delays, gen=new_gen)

    def point_mutation(self, individual):
        new_gen = individual.gen.copy()

        mutation_index = randint(0, self.gen_len * 2 - 1)

        for i in range(self.gen_len - mutation_index - 1):
            if (i + mutation_index) < self.gen_len:
                new_gen[i + mutation_index] = choice(self.available_weights)
            else:
                new_gen[i + mutation_index] = choice(self.available_delays)

        return Individual(self.available_weights, self.available_delays,gen=new_gen)

    def evolute(self):

        self.bests = self.current_population.get_bests(self.n_bests_we_choose)
        besets_by_left = sorted(self.current_population.individuals, key=lambda x: x.fitness.fitness_in)
        besets_by_right = sorted(self.current_population.individuals, key=lambda x: x.fitness.fitness_not)

        self.sender.current_population += 1
        self.sender.message = make_message(self.current_population_num,
                                           self.bests[0].fitness.fitness,
                                           self.bests[0].fitness.real_fitness,
                                           self.bests[0].weights,
                                           self.bests[0].delays)

        self.log_bests()

        news = []

        for best in self.bests:
            news.append(best)

        for i in range(5):
            news.append(Individual(self.available_weights, self.available_delays, gen_size=self.gen_len))

        for i in range(10):
            news.append(self.one_point_crossover(choice(self.bests), choice(self.bests)))
            news.append(self.one_point_crossover(choice(besets_by_left), choice(self.bests)))
            news.append(self.one_point_crossover(choice(besets_by_right), choice(self.bests)))
            news.append(self.two_point_crossover(choice(self.bests), choice(self.bests)))
            news.append(self.mutation(choice(self.bests)))
            news.append(self.point_mutation(choice(self.bests)))
            news.append(self.indexed_mutation(choice(self.bests)))
            news.append(self.two_point_crossover(Individual(self.available_weights, self.available_delays, gen_size=self.gen_len), choice(self.bests)))

        return Population(self.available_weights, self.available_delays, individuals=news)

    def run(self):
        for i in range(self.count_of_populations):
            self.current_population_num = i
            self.calculate_fitness_at_population()
            self.current_population = self.evolute()
            print(f"Iter № {i}")
