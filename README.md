# Liquid-Red

A Python 3D rasterizer engine running entirely in the terminal. No GPU, no display server — just ASCII characters and math.
Built on perspective projection, barycentric rasterization, a z-buffer, and Lambert shading. Designed to be used as a library for TUI 3D applications and games.

---
 
## Features
 
- Perspective projection with configurable focal length and zoom
- Z-buffer for correct depth ordering
- Barycentric triangle rasterization
- Lambert shading with ASCII intensity ramp
- Camera with yaw/pitch rotation and jump physics
- Plane drawing helpers (`draw_plane_xy`, `draw_plane_xz`, `draw_plane_yz`)
- Solid cube with faces and wireframe edges
- Keyboard input via `pynput`
---
 
## Installation
 
```bash
pip install pynput numpy LiquidRed
```

---

## Quick Start
 
```python
import time
from LiquidRed.camera import Camera
from LiquidRed.grid import Renderer
from LiquidRed.events import pressed
from LiquidRed.geometry import Point3d
import numpy as np
 
CANVAS_WIDTH = 64
CANVAS_HEIGHT = 32
LIGHT = np.array([0, 0, -1])
 
camera = Camera(x=0, y=0, z=-5)
renderer = Renderer(camera, light_direction_vector=LIGHT)
 
last_update = 0
 
while True:
    now = time.time()
    if now - last_update < 1 / 60:
        continue
    last_update = now
 
    camera.update(pressed, now)
    renderer.clear_grid()
 
    # draw a floor plane
    renderer.draw_plane_xz(-4, 4, 0, 20, 2)
 
    renderer.show_grid()
```
 
---

### `Cube(size, cx, cy, cz)`
 
A solid cube centered at `(cx, cy, cz)`.
 
```python
from LiquidRed.objects import Cube
 
cube = Cube(size=2, cx=0, cy=0, cz=5)
 
# Draw as solid faces
for v0, v1, v2, v3 in cube.faces:
    renderer.draw_plane(v0, v1, v2, v3)
 
# Draw as wireframe
for i, j in cube.edges:
    renderer.draw_line(cube.vertices[i], cube.vertices[j])
```


###  Coordinate System
 
```
      -Y (up)
       |
       |
-X ----+---- +X
       |
       |
      +Y (down)
 
+Z = into the screen (away from camera)
-Z = toward the camera
```
 
Camera starts at negative Z looking toward positive Z. Place objects at positive Z values to put them in front of the camera.
 
---
    
 
## Example: Corridor Scene
 
```python
from LiquidRed.camera import Camera
from LiquidRed.grid import Renderer
from LiquidRed.events import pressed
import numpy as np, time
 
camera = Camera(z=-1)
renderer = Renderer(camera, np.array([0, 0, -1]))
 
W, H = 4, 3  # corridor half-width, half-height
 
while True:
    now = time.time()
    camera.update(pressed, now)
    renderer.clear_grid()
 
    # floor, ceiling, left wall, right wall
    renderer.draw_plane_xz(-W, W, 0, 30,  H)   # floor
    renderer.draw_plane_xz(-W, W, 0, 30, -H)   # ceiling
    renderer.draw_plane_yz(-H, H, 0, 30, -W)   # left
    renderer.draw_plane_yz(-H, H, 0, 30,  W)   # right
 
    renderer.show_grid()
    time.sleep(1/60)
```
 
---