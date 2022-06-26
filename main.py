from build.build import MultiGpuBuild, OneGpuBuild
from data.analyser import BioAnalyser, Target, Analyser
from ga.fitness import PolyFitnessRat
from ga.ga import GA
from reader.reader import FileReader
from grpc_client.client import Sender

if __name__ == "__main__":
    s = Sender("172.20.10.5", 8085)

    fitness = PolyFitnessRat(bio_analyser=Target())

    build = OneGpuBuild(script_place="/home/yuliya/diplom/gras-cpg/cpu_objects",
                          build_file="cpgSim.cu",
                          build_name="cpg",
                          # count_of_gpu=4,
                          fitness_object=fitness)

    ga = GA(gen_len=28,
            count_of_populations=500,
            available_weights=[i * 50 for i in range(1, 100)],
            available_delays=[i * 0.25 for i in range(1, 20)],
            build=build,
            sender=s)

    ga.run()
