class Fitness:

    def __init__(self, bio_analyser):
        self.bio_analyser = bio_analyser

    def calculate(self, gras_analyser, *args):
        pass


class FitnessObj:
    def __init__(self, fitness, fitness_in, fitness_not, real_fitness):
        self.fitness = fitness
        self.fitness_in = fitness_in
        self.fitness_not = fitness_not
        self.real_fitness = real_fitness

    def __repr__(self):
        return f"{self.fitness} {self.fitness_in} {-self.fitness_not} {self.real_fitness}"

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness


class PolyFitnessRat(Fitness):

    def __init__(self, bio_analyser):
        super().__init__(bio_analyser)

    def calculate(self, gras_analyser, current_population=None, N=None):

        gras_peak_times = []

        for peak in gras_analyser.peaks:
            gras_peak_times.append(peak.time_of)

        gras_peak_times = set(gras_peak_times)

        if current_population is None:
            v = 1
        else:
            v = current_population // (N // 5) + 1

        fitness_in = len(gras_peak_times & self.bio_analyser.peaks)
        fitness_bad = len(gras_peak_times - self.bio_analyser.peaks)

        fitness = fitness_in - fitness_bad * v
        real_fitness = fitness_in - fitness_bad

        return FitnessObj(fitness, real_fitness, fitness_in, -fitness_bad)
