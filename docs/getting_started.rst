Getting Started
===============

Installation
------------

.. code-block:: bash

   pip install pynput numpy LiquidRed

Quick Start
-----------

.. code-block:: python

   import time
   import numpy as np

   from LiquidRed.camera import Camera
   from LiquidRed.grid import Renderer
   from LiquidRed.events import pressed

   camera = Camera(z=-5)
   renderer = Renderer(camera, np.array([0, 0, -1]), 64, 32)

   while True:
       camera.update(pressed, time.time())
       renderer.clear_grid()
       renderer.draw_plane_xz(-4, 4, 0, 20, 2)
       renderer.show_grid()
