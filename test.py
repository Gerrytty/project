from random import choice
from random import randint
from common.gcc_build import Build
from scipy import spatial

import numpy as np

# weights and delays where we choose
weights = [(i + 1) * 50.0 for i in range(100)]
delays = [(i + 1) * 0.5 for i in range(10)]


class Mix:
    @staticmethod
    def simple_crossover(individual1, individual2):
        crossover_point = randint(0, 16)
        return Individual(gen=(individual1.gen[:crossover_point] + individual2.gen[crossover_point:]))

    @staticmethod
    def simple_mutation(individual, mutation_count=2):
        new_gen = []

        for i in range(16):
            new_gen.append(individual.gen[i])

        for i in range(mutation_count):
            mutation_index = randint(0, 15)
            if mutation_index < 8:
                new_gen[mutation_index] = choice(weights)
            else:
                new_gen[mutation_index] = choice(delays)

        return Individual(gen=new_gen)


class Evolution:

    @staticmethod
    def get_fitness(individual: Individual):
        Build.build(individual)
        with open("/home/yuliya/test/dat/0_MN_E_left.dat") as f:
            data = np.array(list(map(lambda x: (-float(x) + 40000) / 1000, f.readline().split())))

        p_peaks = get_poly_peaks(np.split(data, 22))
        if len(p_peaks[:11]) != len(poly_x[:11]):
            individual.fitness = 4000
        else:
            individual.fitness = spatial.distance.euclidean(p_peaks[:11], poly_x[:11])

    @staticmethod
    def calc(pop):
        for individual in pop.individuals:
            Evolution.get_fitness(individual)
        bests = pop.get_bests()
        print(bests[0].fitness)
        f = open("out.txt", "a")
        s = " ".join(list(map(str, bests[0].gen)))
        f.write(f"{bests[0].fitness} {s}\n")

        news = []
        for best in bests:
            news.append(best)
        for i in range(3):
            i1_index = randint(0, 5)
            i2_index = randint(0, 5)
            i3_index = randint(0, 5)
            news.append(Mix.simple_crossover(pop.individuals[i1_index], pop.individuals[i2_index]))
            news.append(Mix.simple_mutation(pop.individuals[i3_index]))

        print(len(news))
        return Population(individuals=news)