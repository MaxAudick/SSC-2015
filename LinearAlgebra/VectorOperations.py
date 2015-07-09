__author__ = 'max'

import numpy as np
import unittest


def is_linearly_independent_2x2(u, v):
    """ Determine if two 2D vectors are linearly independent.

    Vectors are represented by numpy arrays.
    """
    uv = get_uv(u, v)
    if uv[0][0] * uv[1][1] - uv[1][0] * uv[0][1] != 0:
        return True
    else:
        return False


def get_uv(u, v):
    """ Get a combined array of two 2D vectors.

    Vectors are represented by numpy arrays.
    """
    uv = np.zeros((2, 2))
    uv[0][0] = u[0]
    uv[1][0] = u[1]
    uv[0][1] = v[0]
    uv[1][1] = v[1]
    return uv


def get_inverse_2x2(u, v):
    """ If u and v are linearly independent., create [0 1] and [1 0] via linear combinations of u and v.

    Vectors are represented as arrays.
    """
    if not is_linearly_independent_2x2(u, v):
        return
    uv = get_uv(u, v)
    iden = get_uv([1, 0],[0, 1])
    a = np.zeros((2, 4))
    for i in range(2):
        for j in range(2):
            a[i][j] = uv[i][j]
            a[i][j+2] = iden[i][j]

    q = a[0][1] / a[1][1]
    a[0] = a[0] - q * a[1]

    q = a[1][0] / a[0][0]
    a[1] = a[1] - q * a[0]

    a[0] /= a[0][0]

    a[1] /= a[1][1]

    for i in range(2):
        for j in range(2):
            uv[i][j] = a[i][j+2]
    return uv


def is_linearly_independent(matrix):
    """ Return True if the matrix is linearly independent, else return False.
    >>> a = np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]])
    >>> is_linearly_independent(a)
    True
    >>> a = np.array([[2., 1., -1.], [4., 2., -2.], [-2., 1., 2.]])
    >>> is_linearly_independent(a)
    False
    """
    for i in range(len(matrix)):
        for j in range(i+1, len(matrix)):
            row1 = matrix[i]
            row2 = matrix[j]
            if row1[i] != 0:
                q = row2[i] / row1[i]
                matrix[j] = row2 - q * row1
    for i in range(len(matrix)):
        i = len(matrix) - i - 1
        for j in range(i):
            j = i - j - 1
            row1 = matrix[i]
            row2 = matrix[j]
            if row1[i] != 0:
                q = row2[i] / row1[i]
                matrix[j] = row2 - q * row1
        if matrix[i][i] != 0:
            matrix[i] /= matrix[i][i]
        else:
            return False
    return True


def get_identity(l):
    """ Return the square identity matrix of the specified size.
    >>> get_identity(3)
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    """
    identity = np.zeros((l, l))
    for i in range(l):
        identity[i][i] = 1
    return identity


def make_2D(matrix):
    new_matrix = np.zeros((1, len(matrix)))
    for i in range(len(matrix)):
        new_matrix[0][i] = matrix[i]
    return new_matrix


def get_inverse(a):
    """ If a matrix is square, return its inverse.
    >>> a = np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]])
    >>> get_inverse(a)
    array([[ 4.,  3., -1.],
           [-2., -2.,  1.],
           [ 5.,  4., -1.]])
    """
    if len(a) == len(a[0]):
        i = get_identity(len(a))
        inverse = gaussian_solve(a, i)
        return inverse


def multiply_matrices(a, b):
    """ Multiply two matrices if possible.
    >>> a = np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]])
    >>> b = np.array([[ 4.,  3., -1.], [-2., -2.,  1.], [ 5.,  4., -1.]])
    >>> multiply_matrices(a, b)
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    """
    try:
        x = len(b[0])
    except:
        b = make_2D(b)
    try:
        x = len(a[0])
    except:
        a = make_2D(a)
    if len(a[0]) != len(b):
        print 'error: matrices cannot be multiplied'
        return
    out = np.zeros((len(a), len(b[0])))
    for i in range(len(out)):
        for j in range(len(out[0])):
            sum = 0
            for k in range(len(a[i])):
                sum += a[i][k] * b[k][j]
            out[i][j] = sum
    return out


def gaussian_solve(a, b):
    """ Solve two matrices using the gauss-jordan method.
    >>> a = np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]])
    >>> b = np.array([[8.], [-11.], [-3.]])
    >>> gaussian_solve(a, b)
    array([[ 2.],
           [ 3.],
           [-1.]])
    """
    g = np.zeros((len(a), len(a[0]) + len(b[0])))
    for i in range(len(a)):
        for j in range(len(a[0])):
            g[i][j] = a[i][j]
    for i in range(len(b)):
        for j in range(len(b[0])):
            g[i][j + len(a[0])] = b[i][j]
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            row1 = g[i]
            row2 = g[j]
            if row1[i] != 0:
                q = row2[i] / row1[i]
                g[j] = row2 - q * row1
    for i in range(len(a)):
        i = len(a) - i - 1
        for j in range(i):
            j = i - j - 1
            row1 = g[i]
            row2 = g[j]
            if row1[i] != 0:
                q = row2[i] / row1[i]
                g[j] = row2 - q * row1
        if g[i][i] != 0:
            g[i] /= g[i][i]
        else:
            return 'error: matrix is not linearly independent'
    out = np.zeros((len(b), len(b[0])))
    for i in range(len(b)):
        for j in range(len(b[0])):
            out[i][j] = g[i][j + len(a[0])]
    return out


def rand_matrix(row, col, low=0, high=100):
    rand = np.zeros((row, col))
    for i in range(len(rand)):
        for j in range(len(rand[0])):
            rand[i][j] = int(np.random.randint(low, high + 1))
    return rand


def transpose(matrix):
    try:
        rows = len(matrix)
        cols = len(matrix[0])
        trans = np.zeros((cols, rows))
        for i in range(rows):
            for j in range(cols):
                trans[j][i] = matrix[i][j]
        return trans

    except:
        rows = 1
        cols = len(matrix)
        trans = np.zeros((cols, rows))
        for i in range(cols):
            trans[i][0] = matrix[i]
        return trans



if __name__ == '__main__':
    import doctest
    doctest.testmod()
