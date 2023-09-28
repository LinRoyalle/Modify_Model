
import segyio
import numpy as np


def add_abnormal_signal(filename, length, width, velocity, density):
    data_list = []
    with segyio.open(filename, 'r+') as sgyfile:
        for it in range(len(sgyfile.trace)):
            data_list.append(sgyfile.trace[it])


