__author__ = 'max'

def dot_product(u, v):
    """
    :param u: vector
    :param v: vector
    :return: dot product of u and v
    >>> dot_product([1, 0], [0, 1])
    0
    >>> dot_product([1, 4], [2, 3])
    14
    >>> dot_product([1, 3], [2, 'a'])
    'error: member of vector not a number'
    """
    if len(u) == len(v):
        product = 0
        for i in range(len(u)):
            try:
                int(u[i])
                int(v[i])
                product += u[i] * v[i]
            except:
                return 'error: member of vector not a number'
    return product


def unit_vector(u):
    """
    :param u: vector
    :return: dot product of u
    >>> unit_vector([1, 0])
    [1.0, 0.0]
    >>> unit_vector([10, 18])
    [0.48564293117863205, 0.8741572761215377]
    >>> unit_vector([3, 'a'])
    'error: member of vector not a number'
    """
    l = 0
    for val in u:
        try:
            l += val ** 2
        except:
            return 'error: member of vector not a number'
    l **= .5
    for i, val in enumerate(u):
        u[i] = val / l
    return u

if __name__ == "__main__":
    import doctest
    doctest.testmod()

u = [0, 1, 2, 3, 4]
v = [5, 6, 7, 8, 9]
print dot_product(u, v)
print unit_vector(u)
print dot_product([1,4], [2,3])
