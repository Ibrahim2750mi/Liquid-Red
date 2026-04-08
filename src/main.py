# import time
#
# from grid import Renderer
#
# last_update = 0
#
# renderer = Renderer()
#
# while True:
#     now = time.time()
#     if now - last_update < 1 / 60:
#         last_update = now
#         continue
#     renderer.show_grid()
#

from grid import Renderer, point3d
from objects import Cube

renderer = Renderer()
cube = Cube()

for edge in cube.edges:
    x1,y1,z1 = cube.vertices[edge.start]
    x2,y2,z2 = cube.vertices[edge.end]
    p1 = renderer.project_3d(point3d(x1,y1,z1,'#'))
    p2 = renderer.project_3d(point3d(x2,y2,z2,'#'))
    renderer.draw_line(p1, p2)

renderer.show_grid()
