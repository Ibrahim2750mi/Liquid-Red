from collections import namedtuple
from itertools import count

import numpy as np

from geometry import Point3d
from config import CANVAS_HEIGHT, CANVAS_WIDTH, CHUNK_DEPTH

Edge=namedtuple('Edge',['start','end'])

class Cube:
    def __init__(self, cube_size, cx=0, cy=0, cz=0):
        self.vertices=[]
        self.edges=[]
        self.generate_vertices(cube_size / 2)
        self.generate_edges()
        self.cx = cx
        self.cy = cy
        self.cz = cz

    def generate_vertices(self, s):
        self.vertices=[
            Point3d(-s + self.cx,-s + self.cy,-s + self.cz),
            Point3d(s + self.cx,-s + self.cy,-s + self.cz),
            Point3d(s + self.cx,s + self.cy,-s + self.cz),
            Point3d(-s + self.cx,s + self.cy,-s + self.cz),
            Point3d(-s + self.cx,-s + self.cy,s + self.cz),
            Point3d(s + self.cx,-s + self.cy,s + self.cz),
            Point3d(s + self.cx,s + self.cy,s + self.cz),
            Point3d(-s + self.cx,s + self.cy,s + self.cz),
        ]

    def generate_edges(self):
        self.edges=[
            Edge(0,1),Edge(1,2),Edge(2,3),Edge(3,0),
            Edge(4,5),Edge(5,6),Edge(6,7),Edge(7,4),
            Edge(0,4),Edge(1,5),Edge(2,6),Edge(3,7),
        ]


class Chunk:
    def __init__(self, index):
        self.z_start = index * CHUNK_DEPTH
        self.obstacles = []
        obstacle_count = np.random.randint(0, 4)
        for _ in range(obstacle_count):
            cx, cy = np.random.randint(0, CANVAS_WIDTH), np.random.randint(0, CANVAS_HEIGHT)
            cz = np.random.randint(self.z_start, self.z_start + CHUNK_DEPTH)
            self.obstacles.append(Cube(3, cx=cx, cy=cy, cz=cz))

def chunk_generator():
    # hint: use itertools.count() here
    for i in count():
        yield Chunk(i)

