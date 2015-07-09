__author__ = 'max'

import numpy as np
import VectorOperations as VecOps

def make_noise(offset, expected):
    linspace = np.zeros(len(expected))
    for i in range(len(linspace)):
        linspace[i] += ((np.random.ranf() * 2 - 1) * offset) + expected[i]
    return linspace


def xy_linspace(m, b, numpoints, start=0, end=100, axis_key='x'):
    if axis_key == 'x':
        start = m * start + b
        end = m * end + b
    else:
        start = (start - b) / m
        end = (end - b) / m
    linspace = np.linspace(start, end, numpoints + 1)
    return linspace


def least_squares(actual, axis_coords):
    a = VecOps.multiply_matrices(VecOps.transpose(axis_coords), actual)
    b = VecOps.multiply_matrices(VecOps.transpose(axis_coords), axis_coords)
    return a[0][0] / b[0][0]


def best_fit(actual):
    return


expected = VecOps.transpose(VecOps.make_2D(xy_linspace(1, 1, 100)))
print expected
x_coords = VecOps.transpose(VecOps.make_2D(xy_linspace(1, 1, 100)))
print x_coords
actual = VecOps.transpose(VecOps.make_2D(make_noise(11, expected)))
print actual
print 'slope:', least_squares(actual, x_coords)
