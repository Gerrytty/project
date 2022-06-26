import logging
import subprocess
import os
from multiprocessing import Pool
from data.analyser import Analyser
from reader.reader import FileReader
import multiprocessing


class Build:
    def __init__(self, path_to_compiler, script_place, build_file, build_name):
        self.path_to_compiler = path_to_compiler
        self.build_name = build_name
        self.script_place = script_place
        self.build_file = build_file
        logging.basicConfig(format='[%(funcName)s]: %(message)s', level=logging.INFO)
        self.logger = logging.getLogger()

    def print_log(self, out, err):
        for output in str(out.decode("UTF-8")).split("\n"):
            self.logger.info(output)
        for error in str(err.decode("UTF-8")).split("\n"):
            self.logger.error(error)

    def compile(self):
        cmd_build = f"{self.path_to_compiler} -std=c++11 -O3 -o {self.script_place}/{self.build_name} {self.script_place}/{self.build_file}"
        self.logger.info(f"Execute: {cmd_build}")
        process = subprocess.Popen(cmd_build, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        self.print_log(out, err)

    def build(self, build_string):
        cmd_run = f"{self.script_place}/{self.build_name}" + build_string
        self.logger.info(f"Execute: {cmd_run}")
        process = subprocess.Popen(cmd_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        # self.print_log(out, err)

    def calculate(self, individuals, *args):
        pass


class MultiGpuBuild(Build):
    def __init__(self, script_place, build_file, build_name, count_of_gpu, fitness_object):
        super().__init__("/usr/bin/nvcc", script_place, build_file, build_name)
        self.count_of_gpu = count_of_gpu
        self.fitness_object = fitness_object
        self.prepare()
        self.compile()

    def calc_individual(self, individual):

        if self.count_of_gpu == 1:
            curr_process = 0
        else:
            curr_process = int(multiprocessing.current_process().name.split("-")[1]) - 1
        print(f"Current process = {curr_process}")
        build_string = MultiGpuBuild.create_build_string(individual, curr_process)
        self.build(build_string)
        filereader = FileReader(f"{os.getcwd()}/{curr_process}/MN_E.dat")
        filereader.read()
        gras_analyser = Analyser(0.25)
        gras_analyser.analyse_data(filereader.data)
        fitness = self.fitness_object.calculate(gras_analyser,
                                                individual.current_population_num,
                                                individual.all_population_len)
        individual.fitness = fitness
        print(f"Result fitness = {fitness}")

    def calculate(self, individuals, *args):
        with Pool(processes=self.count_of_gpu) as pool:
            result = pool.map(self.calc_individual, individuals)

    @staticmethod
    def create_build_string(individual, gpu_num):
        string = f" {gpu_num} {individual.gen_size} "
        for i in range(individual.gen_size):
            string += f"{individual.weights[i]} {individual.delays[i]} "
        return string

    def prepare(self):
        for i in range(self.count_of_gpu):
            print(os.getcwd())
            if not os.path.isdir(f"{os.getcwd()}/{i}"):
                os.mkdir(f"{os.getcwd()}/{i}")


class OneGpuBuild(Build):
    def __init__(self, script_place, build_file, build_name, fitness_object):
        super().__init__("/usr/bin/nvcc", script_place, build_file, build_name)
        self.fitness_object = fitness_object

    def calc_individual(self, individual):
        build_string = MultiGpuBuild.create_build_string(individual, 0)
        self.build(build_string)
        filereader = FileReader(f"{os.getcwd()}/0/MN_E.dat")
        filereader.read()
        gras_analyser = Analyser(0.25)
        gras_analyser.analyse_data(filereader.data[:4400])

        fitness = self.fitness_object.calculate(gras_analyser,
                                                individual.current_population_num,
                                                individual.all_population_len)
        individual.fitness = fitness
        print(f"Result fitness = {fitness}")

    def calculate(self, individuals, *args):

        for individual in individuals:
            self.calc_individual(individual)