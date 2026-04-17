from collections import namedtuple
from functools import lru_cache

import numpy as np


Point3d = namedtuple('Point3D', ['x', 'y', 'z'])

@lru_cache
def point_position_wrt_line(a, b, p):
    """
    :param a: point 1 on some line
    :param b: point 2 on the same line
    :param p: point
    :return: +ve if p is to the left and -ve if right.
    """
    return (p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x)

@lru_cache
def compute_surface_normal(v1, v2, v3):
    """
    Returns the direction vector of the surface formed by the plane v1, v2, v3.
    """
    a = np.array([v2.x - v1.x, v2.y - v1.y, v2.z - v1.z])
    b = np.array([v3.x - v1.x, v3.y - v1.y, v3.z - v1.z])

    n = np.cross(a, b)

    norm = np.linalg.norm(n)
    if norm == 0:
        return np.array([0, 0, 1])

    return n / norm

@lru_cache
def get_lambert_char(intensity):
    """
    Returns the character that corresponds to intensity.
    """
    shades = " .:-=+*#%@"
    i = int(intensity * (len(shades) - 1))
    return shades[i]