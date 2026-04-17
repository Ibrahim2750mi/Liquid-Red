from collections import deque
from itertools import islice, chain
import time

from camera import Camera
from config import CORRIDOR_H, CORRIDOR_W
from grid import Renderer
from keyboard import pressed
from objects import chunk_generator
from geometry import Point3d

camera = Camera()
renderer = Renderer(camera)


gen = chunk_generator()
active_chunks = deque(islice(gen, 2))

last_update = 0

while True:
    now = time.time()
    if now - last_update < 1 / 60:
        continue
    last_update = now

    camera.update(pressed, now)

    renderer.clear_grid()

    # Despawn chunks
    while active_chunks and active_chunks[0].z_end < camera.z - 10:
        active_chunks.popleft()
    while len(active_chunks) < 2:
        active_chunks.append(next(gen))

    # Draws chunk
    # walls
    for chunk in active_chunks:
        z0, z1 = chunk.z_start, chunk.z_end
        # renderer.draw_plane_xz(-CORRIDOR_W / 2, CORRIDOR_W / 2, z0, z1, -CORRIDOR_H / 2, "#")
        # renderer.draw_plane_xz(-CORRIDOR_W / 2, CORRIDOR_W / 2, z0, z1, CORRIDOR_H / 2, "#")
        renderer.draw_plane_yz(-CORRIDOR_H / 2, CORRIDOR_H / 2, z0, z1, -CORRIDOR_W / 2, "+")
        renderer.draw_plane_yz(-CORRIDOR_H / 2, CORRIDOR_H / 2, z0, z1, CORRIDOR_W / 2, "+")

    # mesh
    for chunk in active_chunks:
        for i,j in chunk.edges:
            renderer.draw_line(chunk.vertices[i], chunk.vertices[j], char="#")
    all_faces = chain.from_iterable(obs.faces for chunk in active_chunks for obs in chunk.obstacles)
    for v0, v1, v2, v3 in all_faces:
        renderer.draw_plane(v0, v1, v2, v3, ".")

    renderer.show_grid()

