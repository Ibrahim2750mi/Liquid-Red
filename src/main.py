import time
#
# from grid import Renderer
#
last_update = 0
#
# renderer = Renderer()
#

from config import CAMERA_Z_DEPTH
from grid import Renderer, Point3d
from keyboard import pressed
from objects import Cube


renderer = Renderer()
cube = Cube()

while True:
    now = time.time()
    if now - last_update < 1 / 60:
        continue
    last_update = now

    if 'w' in pressed:
        renderer.camera_z_depth -= 0.1
    if 's' in pressed:
        renderer.camera_z_depth += 0.1

    renderer.clear_grid()

    for edge in cube.edges:
        x1, y1, z1 = cube.vertices[edge.start]
        x2, y2, z2 = cube.vertices[edge.end]

        p1 = renderer.project_3d(Point3d(x1, y1, z1))
        p2 = renderer.project_3d(Point3d(x2, y2, z2))

        if p1 and p2:
            renderer.draw_line(p1, p2)

    renderer.show_grid()

