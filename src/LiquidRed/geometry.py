from collections import namedtuple
from functools import lru_cache

import numpy as np

Point3d = namedtuple("Point3D", ["x", "y", "z"])


@lru_cache
def point_position_wrt_line(a, b, p):
    """
    Compute the signed area (orientation test) of point `p`
    relative to the directed line from `a` to `b`.

    This is equivalent to the 2D cross product and is commonly
    used in computational geometry (e.g., barycentric coordinates).

    Parameters
    ----------
    a : Point3d
        First point defining the line.
    b : Point3d
        Second point defining the line.
    p : Point3d
        Point to test.

    Returns
    -------
    float
        Signed value indicating position:

        - Positive → `p` is to the left of the line (a → b)
        - Negative → `p` is to the right
        - Zero → `p` lies on the line

    Notes
    -----
    Only the x and y components are used.
    """
    return (p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x)


@lru_cache
def compute_surface_normal(v1, v2, v3):
    """
    Compute the unit normal vector of a surface defined by three points.

    The normal is calculated using the cross product of two edges:
    (v2 - v1) × (v3 - v1).

    Parameters
    ----------
    v1 : Point3d
        First vertex.
    v2 : Point3d
        Second vertex.
    v3 : Point3d
        Third vertex.

    Returns
    -------
    np.ndarray
        Normalized 3D normal vector.

    Notes
    -----
    - If the triangle is degenerate (zero area), a default normal
      of ``[0, 0, 1]`` is returned.
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
    Map a lighting intensity value to an ASCII character.

    This function implements simple Lambertian shading by selecting
    a character from a predefined gradient.

    Parameters
    ----------
    intensity : float
        Lighting intensity in the range [0, 1].

    Returns
    -------
    str
        ASCII character representing brightness.

    Notes
    -----
    - Lower intensity → darker characters
    - Higher intensity → brighter characters
    """
    shades = ".:-=+*#%@"
    i = int(intensity * (len(shades) - 1))
    return shades[i]