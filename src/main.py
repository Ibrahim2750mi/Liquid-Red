import time

from config import GRAVITY
from grid import Renderer, Point3d
from keyboard import pressed
from objects import Cube
import numpy as np


renderer = Renderer()
cube = Cube()

last_update = 0
speed = 0.1

while True:
    now = time.time()
    if now - last_update < 1 / 60:
        continue
    last_update = now

    if renderer.jump:
        renderer.camera_y = 5 * (now - renderer.jump) - GRAVITY / 2 * (now - renderer.jump) ** 2
    if renderer.camera_y < 0:
        renderer.jump = 0

    speed = 0.1

    if 'w' in pressed:
        renderer.camera_x += speed * np.sin(renderer.camera_yaw)
        renderer.camera_z_depth -= speed * np.cos(renderer.camera_yaw)

    if 's' in pressed:
        renderer.camera_x -= speed * np.sin(renderer.camera_yaw)
        renderer.camera_z_depth += speed * np.cos(renderer.camera_yaw)
    if 'a' in pressed:
        renderer.camera_x -= speed * np.cos(renderer.camera_yaw)
        renderer.camera_z_depth -= speed * np.sin(renderer.camera_yaw)
    if 'd' in pressed:
        renderer.camera_x += speed * np.cos(renderer.camera_yaw)
        renderer.camera_z_depth += speed * np.sin(renderer.camera_yaw)
    if "," in pressed:
        renderer.camera_yaw += 0.002
    if "." in pressed:
        renderer.camera_yaw -= 0.002

    if "j" in pressed and renderer.jump == 0:
        renderer.jump = now


    renderer.clear_grid()

    for edge in cube.edges:
        x1, y1, z1 = cube.vertices[edge.start]
        x2, y2, z2 = cube.vertices[edge.end]

        p1 = renderer.plot_point(Point3d(x1, y1, z1))
        p2 = renderer.plot_point(Point3d(x2, y2, z2))

        if p1 and p2:
            renderer.draw_line(p1, p2)

    renderer.show_grid()

