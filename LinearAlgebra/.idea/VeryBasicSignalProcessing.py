__author__ = 'max'

import numpy as np


def make_noise(m, b, linspace=None):
    if linspace is None:
        linspace = np.linspace(0, 0, 101)
    for i in range(len(linspace)):
        rand = np.random.randn(1)
        linspace[i] += rand
    print linspace

make_noise(0, 10)