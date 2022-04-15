from common.fitness_mono import FitnessMono
from common.individual import Individual
from analyser import Analyser
from common.filereader import Filereader, HdfReader
from build import Build

if __name__ == "__main__":
    bio_analyser = Analyser("../bio_data/bio_E_PLT_21cms_40Hz_2pedal_0.1step.hdf5", HdfReader(0))
    gras_analyser = Analyser("../GRAS/8_muscle_and_oms/vm.txt", Filereader())

    individ = Individual([0 for _ in range(100)], [0 for _ in range(100)])

    individ.gen = [2, 900, 5, 2100, 3]
    Build.build(individ, 1, 0)

    fitness = FitnessMono(individ, bio_analyser, gras_analyser)
    fitness.calculate_fitness()

    print(individ.fitness)


