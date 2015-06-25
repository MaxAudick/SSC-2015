__author__ = 'max'

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def binary_list(size, low_val = -1, high_val = 1):
    bin_list = numpy.random.random_integers(0,1,size)
    list_out = []
    for val in bin_list:
        if val == 0:
            list_out.append(low_val)
        else:
            list_out.append(high_val)
    return list_out

def create_steps(num_walkers, num_steps):
    walk = []
    for val in range(num_walkers):
        walk += binary_list(num_steps)
    return numpy.array(walk).reshape((num_walkers, num_steps))

def create_1d_walk(num_walkers, num_steps):
    step_array = create_steps(num_walkers, num_steps)
    walk = numpy.zeros((len(step_array), len(step_array[0]) + 1))
    for walker in range(len(walk)):
        for step in range(len(step_array[0])):
            walk[walker][step+1] = walk[walker][step] + step_array[walker][step]
    return walk

def create_x_dimension_walk(num_walkers, num_steps, dimensions):
    """

    :param num_walkers: int - number of walkers
    :param num_steps: int - number of steps per walker
    :param dimensions: int - number of dimensions that walkers can travel in
    :return: 3-d array of form [walkers[dimensions[coordinates]]]
        such as [[[x1,x2,...,xN][y1,y2,...,yN]][[x1,x2,...,xN][y1,y2,...,yN]]...[[x1,x2,...,xN][y1,y2,...,yN]]]
    """
    walks_by_dimension = [create_1d_walk(num_walkers, num_steps) for val in range(dimensions)]
    walk = numpy.zeros((num_walkers, dimensions, num_steps + 1))
    for walker in range(num_walkers):
        for dimension in range(dimensions):
            walk[walker][dimension] = walks_by_dimension[dimension][walker]
    return walk

def plot_random_walk(num_walkers, num_steps, num_dimensions = 2):
    if num_dimensions == 2:
        fig, ax = plt.subplots()
        for walker in create_x_dimension_walk(num_walkers, num_steps, 2):
            ax.plot(walker[0, :], walker[1, :], '-')
            #ax.scatter(walker[0, num_steps], walker[1, num_steps], marker = 'o', s = 100, c = 'white', zorder = 3)
        ax.scatter(0, 0, marker='o', s=200, c='black', zorder=3)

    elif num_dimensions == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for walker in create_x_dimension_walk(num_walkers, num_steps, 3):
            color = make_random_color()
            ax.plot(walker[0, :], walker[1, :], walker[2, :], c=color, marker='o')
    plt.show()

def make_random_color():
    r = numpy.random.random_sample()
    g = numpy.random.random_sample()
    b = numpy.random.random_sample()
    return r, g, b


plot_random_walk(100, 5000, 3)
