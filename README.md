# Liquid-Red

Liquid-Red is a Python 3D rasterizer with an SDL2 graphical window and an optional ASCII terminal renderer. It uses perspective projection, barycentric rasterization, a z-buffer, and Lambert shading.

## Install

Install the GUI backend (recommended):

```bash
python -m pip install "LiquidRed[gui]"
```

For terminal rendering and keyboard input only:

```bash
python -m pip install LiquidRed
```

## GUI quick start

```python
import time

import numpy as np

from LiquidRed.camera import Camera
from LiquidRed.grid import Renderer
from LiquidRed.gui import Window

camera = Camera(z=-1)
renderer = Renderer(camera, np.array([0, 0, -1]), 64, 32)
window = Window(renderer)

try:
    while window.poll():
        camera.update(window.pressed, time.time())
        renderer.clear_grid()
        renderer.draw_plane_xz(-4, 4, 0, 20, 2)
        window.present()
        window.tick()
finally:
    window.close()
```

The full GUI corridor example is in [`examples/gui_corridor.py`](examples/gui_corridor.py).

## Terminal option

The same renderer can print its character grid in the terminal. Importing `LiquidRed.events` starts the keyboard listener used by this example:

```python
import time

import numpy as np

from LiquidRed.camera import Camera
from LiquidRed.events import pressed
from LiquidRed.grid import Renderer

camera = Camera(z=-1)
renderer = Renderer(camera, np.array([0, 0, -1]), 64, 32)

while True:
    now = time.time()
    camera.update(pressed, now)
    renderer.clear_grid()
    renderer.draw_plane_xz(-4, 4, 0, 20, 2)
    renderer.show_grid()
    time.sleep(1 / 60)
```

## Features

- SDL2 GUI window with keyboard input, resizable display, and red or grayscale palettes
- Optional ASCII terminal output and `pynput` keyboard input
- Perspective projection, configurable focal length, and zoom
- Z-buffer, barycentric triangle rasterization, and Lambert shading
- Camera yaw, pitch, and jump controls
- Plane helpers and cube geometry

For API documentation and more examples, see the [docs](docs/index.rst).
