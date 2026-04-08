import time

from grid import Renderer

last_update = 0

renderer = Renderer()

while True:
    now = time.time()
    if now - last_update < 1 / 60:
        last_update = now
        continue
    renderer.show_grid()
