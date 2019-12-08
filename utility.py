import math

def vector_add(v1, v2):
    """
    Adds two 2d-vectors together because Python would rather concatenate them.

    Parameters:
        v1 ((int, int)): The first vector
        v2 ((int, int)): The second vector

    Returns:
        (int, int): The result of adding the corresponding elements of v1 and v2.
    """
    return v1[0] + v2[0], v1[1] + v2[1]


def vector_subtract(v1, v2):
    """
    Subtracts two 2d-vectors together.

    Parameters:
        v1 ((int, int)): The first vector
        v2 ((int, int)): The second vector

    Returns:
        (int, int): The result of subtracting the corresponding elements of v1 and v2.
    """
    return v1[0] - v2[0], v1[1] - v2[1]

def vector_floor(v):
    """
    Truncates the value of each element of a vector.
    """
    return math.floor(v[0]), math.floor(v[1])