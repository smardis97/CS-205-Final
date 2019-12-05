import math

def vector_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def vector_subtract(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]

def vector_floor(v):
    return math.floor(v[0]), math.floor(v[1])