import time
from collections import deque
from itertools import chain, islice

from camera import Camera
from config import CORRIDOR_H, CORRIDOR_W
from grid import Renderer
from keyboard import pressed
from objects import chunk_generator

camera = Camera(focal_length=30)
renderer = Renderer(camera)


gen = chunk_generator()
active_chunks = deque(islice(gen, 2))

last_update = 0

while True:
    now = time.time()
    if now - last_update < 1 / 60:
        continue
    print((1/(now - last_update)))
    #last_update = now

    t0 = time.perf_counter()
    camera.update(pressed, now)
    t1 = time.perf_counter()
    renderer.clear_grid()
    t2 = time.perf_counter()
    # Despawn chunks
    while active_chunks and active_chunks[0].z_end < camera.z - camera.focal_length:
        active_chunks.popleft()
    while len(active_chunks) < 2:
        active_chunks.append(next(gen))

    # Draws chunk
    #walls
    for chunk in active_chunks:
        z0, z1 = chunk.z_start, chunk.z_end
        # renderer.draw_plane_xz(-CORRIDOR_W / 2, CORRIDOR_W / 2, z0, z1, -CORRIDOR_H / 2, "#")
        # renderer.draw_plane_xz(-CORRIDOR_W / 2, CORRIDOR_W / 2, z0, z1, CORRIDOR_H / 2, "#")
        renderer.draw_plane_yz(-CORRIDOR_H / 2, CORRIDOR_H / 2, z0, z1, -CORRIDOR_W / 2, "+")
        renderer.draw_plane_yz(-CORRIDOR_H / 2, CORRIDOR_H / 2, z0, z1, CORRIDOR_W / 2, "+")

    # mesh
    for chunk in active_chunks:
        for i, j in chunk.edges:
            renderer.draw_line(chunk.vertices[i], chunk.vertices[j], char="#")
    all_faces = chain.from_iterable(obs.faces for chunk in active_chunks for obs in chunk.obstacles)
    for v0, v1, v2, v3 in all_faces:
        renderer.draw_plane(v0, v1, v2, v3, ".")
    t3 = time.perf_counter()

    #   renderer.check_collision()

    renderer.show_grid()
    t4 = time.perf_counter()
    print(
    f"camera:{(t1 - t0) * 1000:.1f}ms  clear:{(t2 - t1) * 1000:.1f}ms  draw:{(t3 - t2) * 1000:.1f}ms  show:{(t4 - t3) * 1000:.1f}ms")
    last_update = now
