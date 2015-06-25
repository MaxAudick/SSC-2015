__author__ = 'max'

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def position_list(num_dimensions, num_steps):
    dir_list = numpy.random.random_integers(0, num_dimensions * 2 - 1, num_steps)
    arr_out = numpy.zeros((num_dimensions, num_steps + 1))
    for idx, val in enumerate(dir_list):
        arr_out[val / 2][idx + 1] = val % 2 * 2 - 1
        for dim in range(len(arr_out)):
            arr_out[dim][idx + 1] = arr_out[dim][idx] + arr_out[dim][idx + 1]
    return arr_out

def create_random_walk(num_walkers, num_dimensions, num_steps):
    arr_walk = numpy.zeros((num_walkers, num_dimensions, num_steps + 1))
    for val in range(num_walkers):
        arr_walk[val] = position_list(num_dimensions, num_steps)
    return arr_walk

def plot_random_walk(num_walkers, num_steps, num_dimensions = 2):
    if num_dimensions == 2:
        fig, ax = plt.subplots()
        for walker in create_random_walk(num_walkers, 2, num_steps):
            ax.plot(walker[0, :], walker[1, :], '-')
            #ax.scatter(walker[0, num_steps], walker[1, num_steps], marker = 'o', s = 100, c = 'white', zorder = 3)
        ax.scatter(0, 0, marker='o', s=200, c='black', zorder=3)

    elif num_dimensions == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for walker in create_random_walk(num_walkers, 3, num_steps):
            ax.plot(walker[0, :], walker[1, :], walker[2, :], c=make_random_color(), marker='o')
    plt.show()

def make_random_color():
    r = numpy.random.random_sample()
    g = numpy.random.random_sample()
    b = numpy.random.random_sample()
    return r, g, b

plot_random_walk(100, 10000, 2)
