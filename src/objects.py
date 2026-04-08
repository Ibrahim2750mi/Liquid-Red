from collections import namedtuple
import math
CUBE_SIZE=3

Edge=namedtuple('Edge',['start','end'])

class Cube:
    def __init__(self):
        self.vertices=[]
        self.edges=[]
        self.generate_vertices()
        self.generate_edges()

    def generate_vertices(self):
        s=CUBE_SIZE
        self.vertices=[
            (-s,-s,-s),
            (s,-s,-s),
            (s,s,-s),
            (-s,s,-s),
            (-s,-s,s),
            (s,-s,s),
            (s,s,s),
            (-s,s,s),
        ]

    def generate_edges(self):
        self.edges=[
            Edge(0,1),Edge(1,2),Edge(2,3),Edge(3,0),
            Edge(4,5),Edge(5,6),Edge(6,7),Edge(7,4),
            Edge(0,4),Edge(1,5),Edge(2,6),Edge(3,7),
        ]


