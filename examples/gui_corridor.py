"""Corridor + cube in an SDL2 window. Run: pip install 'LiquidRed[gui]' && python examples/gui_corridor.py"""
import time

import numpy as np

from LiquidRed.camera import Camera
from LiquidRed.grid import Renderer
from LiquidRed.gui import Window
from LiquidRed.objects import Cube

W, H = 128, 64
# zoom is in canvas units (screen_x = x * focal * zoom / z + W/2); 10 frames a 64-wide canvas, so scale it
camera = Camera(z=-1, zoom=10 * W / 64)
light = np.array([0.5, -0.7, -1.0])
light /= np.linalg.norm(light)  # must be unit length or less: get_lambert_char indexes by intensity
renderer = Renderer(camera, light, W, H)

cube = Cube(size=2, cx=0, cy=1, cz=8)
HW, HH = 4, 3  # corridor half-width / half-height

win = Window(renderer, palette="red", fps=60)
while win.poll():
    camera.update(win.pressed, time.time())
    renderer.clear_grid()

    renderer.draw_plane_xz(-HW, HW, 0, 30, HH)   # floor
    renderer.draw_plane_xz(-HW, HW, 0, 30, -HH)  # ceiling
    renderer.draw_plane_yz(-HH, HH, 0, 30, -HW)  # left wall
    renderer.draw_plane_yz(-HH, HH, 0, 30, HW)   # right wall
    renderer.draw_plane_xy(-HW, HW, -HH, HH, 30)  # far wall closes the corridor
    for v0, v1, v2, v3 in cube.faces:
        renderer.draw_plane(v0, v1, v2, v3)
    for i, j in cube.edges:
        renderer.draw_line(cube.vertices[i], cube.vertices[j], char="@")  # char must be a keyword

    win.present()
    win.tick()
win.close()
