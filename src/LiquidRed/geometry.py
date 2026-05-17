from collections import namedtuple
from functools import lru_cache

import numpy as np

Point3d = namedtuple("Point3D", ["x", "y", "z"])


def point_position_wrt_line(a, b, x, y):
    """
    Compute the signed area (orientation test) of point `(x,y)`
    relative to the directed line from `a` to `b`.

    This is equivalent to the 2D cross product and is commonly
    used in computational geometry (e.g., barycentric coordinates).

    Parameters
    ----------
    a : Point3d
        First point defining the line.
    b : Point3d
        Second point defining the line.
    x : ndarray
        x of the Point to test.
    y : ndarray
        y of the Point to test.

    Returns
    -------
    ndarray
        Signed value indicating position:

        - Positive → `(x,y)` is to the left of the line (a -> b)
        - Negative → `(x,y)` is to the right
        - Zero → `(x,y)` lies on the line

    Notes
    -----
    Only the x and y components are used.
    """
    return (x - a.x) * (b.y - a.y) - (y - a.y) * (b.x - a.x)


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


@lru_cache
def check_coplanar(v1, v2, v3, p):
    """
    Check if four points are coplanar using the scalar triple product.

    Parameters
    ----------
    v1, v2, v3 : Point3d
        Points defining a plane.
    p : Point3d
        Point to test.

    Returns
    -------
    bool
        True if coplanar (within tolerance).
    """
    p1 = np.array([v1.x, v1.y, v1.z], dtype=float)
    p2 = np.array([v2.x, v2.y, v2.z], dtype=float)
    p3 = np.array([v3.x, v3.y, v3.z], dtype=float)
    p4 = np.array([p.x, p.y, p.z], dtype=float)

    a = p2 - p1
    b = p3 - p1
    c = p4 - p1

    volume = np.dot(a, np.cross(b, c))
    return abs(volume) < 0.1
