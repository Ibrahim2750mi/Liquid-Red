Examples
========

Cube Example
------------

.. code-block:: python

   from LiquidRed.objects import Cube

   cube = Cube(size=2, cx=0, cy=0, cz=5)

   for v0, v1, v2, v3 in cube.faces:
       renderer.draw_plane(v0, v1, v2, v3)

   for i, j in cube.edges:
       renderer.draw_line(cube.vertices[i], cube.vertices[j])


Coordinate System
-----------------

::

         -Y (up)
          |
          |
   -X ----+---- +X
          |
          |
         +Y (down)

   +Z = into the screen
   -Z = toward the camera


Corridor Scene
--------------

.. code-block:: python

   import time
   import numpy as np

   from LiquidRed.camera import Camera
   from LiquidRed.grid import Renderer
   from LiquidRed.events import pressed

   camera = Camera(z=-1)
   renderer = Renderer(camera, np.array([0, 0, -1]), 64, 32)

   W, H = 4, 3

   while True:
       camera.update(pressed, time.time())
       renderer.clear_grid()

       renderer.draw_plane_xz(-W, W, 0, 30,  H)
       renderer.draw_plane_xz(-W, W, 0, 30, -H)
       renderer.draw_plane_yz(-H, H, 0, 30, -W)
       renderer.draw_plane_yz(-H, H, 0, 30,  W)

       renderer.show_grid()
       time.sleep(1/60)
