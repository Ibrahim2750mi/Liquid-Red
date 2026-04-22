from collections import namedtuple

from .geometry import Point3d

Edge = namedtuple("Edge", ["start", "end"])


class Object:
    """
    Base class for geometric objects.

    All objects must define a set of vertices and edges.

    Parameters
    ----------
    vertices : list[Point3d]
        List of vertex positions.
    edges : list[Edge]
        List of edges defined by vertex indices.

    Attributes
    ----------
    vertices : list[Point3d]
        Vertex positions in 3D space.
    edges : list[Edge]
        Connections between vertices (by index).
    """

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


class Cube(Object):
    """
    Cube primitive defined by vertices, edges, and faces.

    The cube is centered at (cx, cy, cz) and has equal side lengths.

    Parameters
    ----------
    size : float
        Length of each side of the cube.
    cx : float, optional
        X-coordinate of the cube center. Default is 0.
    cy : float, optional
        Y-coordinate of the cube center. Default is 0.
    cz : float, optional
        Z-coordinate of the cube center. Default is 0.

    Attributes
    ----------
    vertices : list[Point3d]
        Eight vertices of the cube.
    edges : list[Edge]
        Edges connecting vertices (by index).
    faces : list[tuple[Point3d, Point3d, Point3d, Point3d]]
        Faces of the cube represented as quads (4 vertices each).

    Notes
    -----
    - Faces can be used for solid rendering.
    - Edges can be used for wireframe rendering.
    """

    def __init__(self, size, cx=0, cy=0, cz=0):
        s = size / 2

        self.vertices = [
            Point3d(cx - s, cy - s, cz - s),
            Point3d(cx + s, cy - s, cz - s),
            Point3d(cx + s, cy + s, cz - s),
            Point3d(cx - s, cy + s, cz - s),
            Point3d(cx - s, cy - s, cz + s),
            Point3d(cx + s, cy - s, cz + s),
            Point3d(cx + s, cy + s, cz + s),
            Point3d(cx - s, cy + s, cz + s),
        ]

        self.faces = [
            (self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]),
            (self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]),
            (self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]),
            (self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]),
            (self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]),
            (self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]),
        ]

        self.edges = [
            Edge(0, 1),
            Edge(1, 2),
            Edge(2, 3),
            Edge(3, 0),
            Edge(4, 5),
            Edge(5, 6),
            Edge(6, 7),
            Edge(7, 4),
            Edge(0, 4),
            Edge(1, 5),
            Edge(2, 6),
            Edge(3, 7),
        ]

        super().__init__(self.vertices, self.edges)