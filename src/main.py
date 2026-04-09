import time

from config import GRAVITY

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
        if renderer.jump:
            renderer.camera_y = 5 * (now - renderer.jump) - GRAVITY / 2 * (now - renderer.jump)**2
        if renderer.camera_y < 0:
            renderer.jump = 0
        continue
    last_update = now

    if 'w' in pressed:
        renderer.camera_z_depth -= 0.1
    if 's' in pressed:
        renderer.camera_z_depth += 0.1
    if "a" in pressed:
        renderer.camera_x -= 0.1
    if "d" in pressed:
        renderer.camera_x += 0.1

    if "j" in pressed:
        renderer.jump = now


    renderer.clear_grid()

    for edge in cube.edges:
        x1, y1, z1 = cube.vertices[edge.start]
        x2, y2, z2 = cube.vertices[edge.end]

        p1 = renderer.project_3d(Point3d(x1, y1, z1))
        p2 = renderer.project_3d(Point3d(x2, y2, z2))

        if p1 and p2:
            renderer.draw_line(p1, p2)

    renderer.show_grid()

