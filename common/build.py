import multiprocessing
import logging
import subprocess

logging.basicConfig(format='[%(funcName)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger()


class Build:
    buildname = "cpg"
    script_place = "/home/yuliya/Diplom_^_^_new_v/GRAS/8_muscle_and_oms"
    nvcc = "/usr/bin/nvcc"
    buildfile = "cpgWithArrs.cu"

    @staticmethod
    def create_build_string(individual, number, num=0):
        print(individual)
        string = f" {individual.gen_size} "
        for i in range(individual.gen_size):
            string += f"{individual.weights[i]} {individual.delays[i]} "
        return string


    @staticmethod
    def build(individual, num_steps, itest):
        for i in range(num_steps):
            cmd_run = f"{Build.script_place}/{Build.buildname}" + Build.create_build_string(individual, itest, i)

            logger.info(f"Execute: {cmd_run}")
            process = subprocess.Popen(cmd_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()

            # for output in str(out.decode("UTF-8")).split("\n"):
            #     logger.info(output)
            # for error in str(err.decode("UTF-8")).split("\n"):
            #     logger.info(error)

    @staticmethod
    def compile():
        cmd_build = f"{Build.nvcc} -std=c++11 -O3 -o {Build.script_place}/{Build.buildname} {Build.script_place}/{Build.buildfile}"
        logger.info(f"Execute: {cmd_build}")
        process = subprocess.Popen(cmd_build, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()

        for output in str(out.decode("UTF-8")).split("\n"):
            logger.info(output)
        for error in str(err.decode("UTF-8")).split("\n"):
            logger.info(error)

    @staticmethod
    def run_tests(individuals):
        processes = []

        for i in range(len(individuals)):
            p = multiprocessing.Process(target=Build.build, args=(individuals[i], i,))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()