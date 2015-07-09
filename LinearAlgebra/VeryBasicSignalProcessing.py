__author__ = 'max'

import numpy as np
import matplotlib.pyplot as plt
import VectorOperations as VecOps


def make_noise(offset, expected):
    actual = np.zeros((len(expected), len(expected[0])))
    for r in range(len(actual)):
        for c in range(len(actual[0])):
            actual[r][c] += ((np.random.ranf() * 2 - 1) * offset) + expected[r][c]
    return actual


def xy_line(m, b, numpoints, start=0, end=100, axis_key='x'):
    if axis_key == 'x':
        start = m * start + b
        end = m * end + b
    else:
        start = (start - b) / m
        end = (end - b) / m
    linspace = np.linspace(start, end, numpoints + 1)
    return linspace


def xy_parabola(alist, num_points, start_point=0, end_point=100, axis_key='x'):
    step = (end_point - start_point) / num_points
    parabola = np.zeros((num_points, 1))
    if axis_key == 'x':
        x = start_point
        for point in range(num_points):
            for i, a in enumerate(alist):
                parabola[x][0] += a * (x ** i)
            x += step
    return parabola


def parabola(alist, num_points, start_point=0, end_point=100, axis_key='x'):
    step = (end_point - start_point) / num_points
    parabola = np.zeros((num_points, 2))
    if axis_key == 'x':
        x = start_point
        for point in range(num_points):
            for i, a in enumerate(alist):
                parabola[point][1] += a * (x ** i)
            parabola[point][0] = x
            x += step
    return parabola, step


def least_squares(actual, axis_coords):
    a = VecOps.multiply_matrices(VecOps.transpose(axis_coords), actual)
    b = VecOps.multiply_matrices(VecOps.transpose(axis_coords), axis_coords)
    return a[0][0] / b[0][0]


def get_axis(parabola, axis=1):
    coords = np.zeros((len(parabola), 1))
    for i in range(len(parabola)):
        coords[i][0] = parabola[i][axis]
    return coords


def get_h(num_terms, num_data_pts, step=1):
    h = np.zeros((num_data_pts, num_terms))
    for c in range(len(h[0])):
        if c == 0:
            for r in range(len(h)):
                h[r][c] = 1
        else:
            for r in range(len(h)):
                h[r][c] = r ** c * step
    return h


def best_fit(x, terms=1, step=1):
    h = get_h(terms, len(x), step)
    a = VecOps.multiply_matrices(VecOps.transpose(h), h)
    b = VecOps.multiply_matrices(VecOps.transpose(h), x)
    c = VecOps.multiply_matrices(VecOps.get_inverse(a), b)
    return c / step


def windowed_average(x, width):
    averaged = np.zeros((len(x), 1))
    for i in range(len(x)):
        averaged_val = 0
        w = width
        for shifter in range(width):
            shift_i = i + shifter - (width / 2)
            if 0 <= shift_i < len(x):
                averaged_val += x[shift_i][1]
            else:
                w -= 1
        averaged[i][0] = averaged_val / w
    return averaged


def f(x, eq):
    y = [0 for i in x]
    for i in range(len(eq)):
        out = eq[i][0]
        out *= (x ** i)
        y += out
    return tuple(y)


def arr_to_lst(arr, col=0):
    lst = [arr[r][col] for r in range(len(arr))]
    return lst


size = 1000
expected, step = parabola([2, 5, 3], size, 0 - (size / 2), size)
actual = make_noise(size ** 2, expected)
eq = best_fit(get_axis(actual), 3, step)
ave = windowed_average(actual, size / 4)
print expected
print
print actual
print
print eq
x = np.arange(size)
plt.plot(x, f(x, eq), '-', label='least squares')
plt.plot(x, tuple(arr_to_lst(expected, 1)), '-', linewidth=2.5, label='expected')
plt.scatter(x, tuple(arr_to_lst(actual, 1)), marker='.', s=10, label='actual')
plt.plot(x, tuple(ave), '-', label='moving average')
plt.legend(loc=1)
plt.show()
