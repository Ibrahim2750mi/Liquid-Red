from collections import namedtuple
from functools import lru_cache

import numpy as np

Point3d = namedtuple("Point3D", ["x", "y", "z"])


def point_position_wrt_line(a, b, x, y):
    """
    :param a: array of point 1 on some line
    :param b: array of point 2 on the same line
    :param x: array of point x / the point x
    :param y: arrary of point y / the point y
    :return: +ve if p_i is to the left and -ve if right.
    """
    return (x - a.x) * (b.y - a.y) - (y - a.y) * (b.x - a.x)


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
    shades = ".:-=+*#%@"
    i = int(intensity * (len(shades) - 1))
    return shades[i]


@lru_cache
def check_coplanar(v1, v2, v3, p):
    p1 = np.array([v1.x, v1.y, v1.z], dtype=float)
    p2 = np.array([v2.x, v2.y, v2.z], dtype=float)
    p3 = np.array([v3.x, v3.y, v3.z], dtype=float)
    p4 = np.array([p.x, p.y, p.z], dtype=float)

    a = p2 - p1
    b = p3 - p1
    c = p4 - p1

    # scalar triple product
    volume = np.dot(a, np.cross(b, c))
    return abs(volume) < 0.1

