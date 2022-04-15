from common.filereader import *
from analyser import Analyser

if __name__ == "__main__":
    analyser = Analyser("../GRAS/8_muscle_and_oms/vm.txt", Filereader())
    analyser.data = analyser.data[:1100]
    analyser.smooth()
    analyser.normalize()
    analyser.find_peaks()

    print(analyser.peaks[0].ampl)