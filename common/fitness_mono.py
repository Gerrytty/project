from scipy import spatial


class FitnessMono:

    @staticmethod
    def calculate_fitness(individual, bio_analyser, gras_analyser):

        gras_analyser.split_peaks_by_slices(100, 11)
        # Раз в 5мс, 4 = шаг симуляции, 25 мс = длина одного слайса
        right_vector_of_mono_ans_times = [5 * 4 + i * 25 * 4 for i in range(0, 11)]
        right_vector_of_mono_ans_duration = [8 for i in range(0, 11)]

        print(right_vector_of_mono_ans_times)
        print(gras_analyser.splitted_peaks)

        vector_of_peaks = []
        vector_of_times_of_peaks = []
        vector_of_ampls_of_peaks = []
        vector_of_duration = []

        if gras_analyser.splitted_peaks is None:
            individual.fitness = float('inf')
            return individual.fitness

        for peak in gras_analyser.splitted_peaks:

            if len(peak) == 0:
                individual.fitness = float('inf')
                return individual.fitness

            vector_of_peaks.append(peak[0])
            vector_of_times_of_peaks.append(peak[0].time_of)
            vector_of_ampls_of_peaks.append(peak[0].ampl)
            vector_of_duration.append(peak[0].duration)

        print(f"ampls {vector_of_ampls_of_peaks}")
        print(spatial.distance.euclidean(right_vector_of_mono_ans_duration, vector_of_duration))

        individual.fitness = (1 + spatial.distance.euclidean(right_vector_of_mono_ans_times, vector_of_times_of_peaks))\
            # (1 + spatial.distance.euclidean(right_vector_of_mono_ans_duration, vector_of_duration))

        return individual.fitness
