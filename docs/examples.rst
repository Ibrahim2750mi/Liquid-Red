Examples
========

GUI Corridor
------------

Install ``LiquidRed[gui]`` to run the SDL2 example. It draws a corridor and a cube, and uses the window keyboard controls:

.. literalinclude:: ../examples/gui_corridor.py
   :language: python

.. _terminal-example:

Terminal Corridor
-----------------

Install ``LiquidRed`` to run the ASCII terminal version. It uses ``pynput`` for keyboard input:

.. literalinclude:: ../examples/terminal_corridor.py
   :language: python

Cube Geometry
-------------

The cube exposes vertices, edges, and faces so it can be rendered in either mode:

.. code-block:: python

   from LiquidRed.objects import Cube

   cube = Cube(size=2, cx=0, cy=0, cz=5)

   for v0, v1, v2, v3 in cube.faces:
       renderer.draw_plane(v0, v1, v2, v3)

   for i, j in cube.edges:
       renderer.draw_line(cube.vertices[i], cube.vertices[j])
