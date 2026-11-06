Getting Started
===============

Install the SDL2 GUI backend and its dependencies:

.. code-block:: bash

   python -m pip install "LiquidRed[gui]"

GUI Quick Start
---------------

Create a renderer, pass it to :class:`LiquidRed.gui.Window`, and present each frame:

.. code-block:: python

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

Controls are **W/A/S/D** to move, **arrow keys** to look, and **J** or **Space** to jump. Press **Esc** or close the window to exit.

Terminal Option
---------------

To use the ASCII renderer instead, install the core package:

.. code-block:: bash

   python -m pip install LiquidRed

The terminal mode uses ``pynput`` for global keyboard input and ``Renderer.show_grid()`` for output. See :ref:`terminal-example` for a complete script.
