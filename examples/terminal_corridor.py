"""ASCII corridor example. Run with: python examples/terminal_corridor.py"""
import time

import numpy as np

from LiquidRed.camera import Camera
from LiquidRed.events import pressed
from LiquidRed.grid import Renderer

camera = Camera(z=-1)
renderer = Renderer(camera, np.array([0, 0, -1]), 64, 32)
half_width, half_height = 4, 3

while True:
    now = time.time()
    camera.update(pressed, now)
    renderer.clear_grid()

    renderer.draw_plane_xz(-half_width, half_width, 0, 30, half_height)
    renderer.draw_plane_xz(-half_width, half_width, 0, 30, -half_height)
    renderer.draw_plane_yz(-half_height, half_height, 0, 30, -half_width)
    renderer.draw_plane_yz(-half_height, half_height, 0, 30, half_width)

    renderer.show_grid()
    time.sleep(1 / 60)
