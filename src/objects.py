from collections import namedtuple
from itertools import count

import numpy as np

from config import CHUNK_DEPTH, CORRIDOR_H, CORRIDOR_W
from geometry import Point3d

Edge = namedtuple("edge", ["start", "end"])


class Object:
    """Base class for any object. Any object must contain its vertices and edges."""
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


class Cube(Object):
    """
    A solid/wired cube can be made from this using faces/edges.
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


class Chunk(Object):
    """
    Chunk object for infinite generation.
    """
    def __init__(self, index):
        self.z_start = index * (CHUNK_DEPTH + 3)
        self.z_end = self.z_start + CHUNK_DEPTH
        self.obstacles = []
        obstacle_count = np.random.randint(0, 4)

        for _ in range(obstacle_count):
            cx = np.random.randint(-CORRIDOR_W / 2, CORRIDOR_W / 2)
            cy = np.random.randint(-CORRIDOR_H / 2, CORRIDOR_H / 2)
            cz = np.random.randint(self.z_start, self.z_end)
            self.obstacles.append(Cube(1.5, cx=cx, cy=cy, cz=cz))

        self.vertices = [
            Point3d(-CORRIDOR_W / 2, -CORRIDOR_H / 2, self.z_start),  # 0
            Point3d(CORRIDOR_W / 2, -CORRIDOR_H / 2, self.z_start),  # 1
            Point3d(CORRIDOR_W / 2, CORRIDOR_H / 2, self.z_start),  # 2
            Point3d(-CORRIDOR_W / 2, CORRIDOR_H / 2, self.z_start),  # 3
            Point3d(-CORRIDOR_W / 2, -CORRIDOR_H / 2, self.z_end),  # 4
            Point3d(CORRIDOR_W / 2, -CORRIDOR_H / 2, self.z_end),  # 5
            Point3d(CORRIDOR_W / 2, CORRIDOR_H / 2, self.z_end),  # 6
            Point3d(-CORRIDOR_W / 2, CORRIDOR_H / 2, self.z_end),  # 7
        ]

        # 12 edges
        self.edges = [
            # front face (self.z_start)
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            # back face (self.z_end)
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            # connections
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

        super().__init__(self.vertices, self.edges)


def chunk_generator():
    """Exhaustive chunk object generator."""
    for i in count():
        yield Chunk(i)
