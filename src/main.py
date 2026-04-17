import time

from camera import Camera
from config import GRAVITY
from grid import Renderer
from keyboard import pressed
from objects import Chunk, chunk_generator
import numpy as np

camera = Camera()
renderer = Renderer(camera)

from collections import deque
import itertools

gen = chunk_generator()
active_chunks = deque(itertools.islice(gen, 5))  # seed with first 5

last_update = 0
speed = 0.1

while True:
    now = time.time()
    if now - last_update < 1 / 60:
        continue
    last_update = now

    camera.update(pressed, now)

    renderer.clear_grid()

    renderer.show_grid()

