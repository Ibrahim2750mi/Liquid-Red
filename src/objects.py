from itertools import count

import numpy as np

from geometry import Point3d
from config import CHUNK_DEPTH, CORRIDOR_H, CORRIDOR_W

class Cube:
    def __init__(self, size, cx=0, cy=0, cz=0):
        s = size / 2
        self.vertices = [
            Point3d(cx-s, cy-s, cz-s), Point3d(cx+s, cy-s, cz-s),
            Point3d(cx+s, cy+s, cz-s), Point3d(cx-s, cy+s, cz-s),
            Point3d(cx-s, cy-s, cz+s), Point3d(cx+s, cy-s, cz+s),
            Point3d(cx+s, cy+s, cz+s), Point3d(cx-s, cy+s, cz+s),
        ]
        self.faces = [
            (self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]),
            (self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]),
            (self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]),
            (self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]),
            (self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]),
            (self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]),
        ]


class Chunk:
    def __init__(self, index):
        self.z_start = index * CHUNK_DEPTH
        self.z_end = self.z_start + CHUNK_DEPTH
        self.obstacles = []
        obstacle_count = np.random.randint(0, 4)
        for _ in range(obstacle_count):
            cx = np.random.randint(-CORRIDOR_W / 2, CORRIDOR_W / 2)
            cy = np.random.randint(-CORRIDOR_H / 2, CORRIDOR_H / 2)
            cz = np.random.randint(self.z_start, self.z_end)
            self.obstacles.append(Cube(2, cx=cx, cy=cy, cz=cz))

def chunk_generator():
    for i in count():
        yield Chunk(i)

