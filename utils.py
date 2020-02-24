import math

def distance(x1, y1, x2, y2):
    return math.sqrt( ((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)) )

def normalize(x1, y1, x2, y2):
    if(distance(x1, y1, x2, y2) == 0):
        return [1, 0]

    return [ (x2 - x1) / distance(x1, y1, x2, y2), (y2 - y1) / distance(x1, y1, x2, y2) ]

def invert(vec):
    return [ -1 * vec[0], -1 * vec[1] ]

def expand(vec, multiplier):
    return [ vec[0] * multiplier, vec[1] * multiplier ]

def roundvec(vec):
    return [ round(vec[0]), round(vec[1]) ]