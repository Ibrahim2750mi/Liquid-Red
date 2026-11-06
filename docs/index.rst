Liquid-Red
==========

A Python 3D rasterizer with an SDL2 graphical window and an optional ASCII terminal renderer.

Built on perspective projection, barycentric rasterization, a z-buffer, and Lambert shading.

.. toctree::
   :maxdepth: 2
   :caption: Guide

   getting_started
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

Features
--------

- Perspective projection with configurable focal length and zoom
- Z-buffer for correct depth ordering
- Barycentric triangle rasterization
- SDL2 GUI window with red or grayscale palettes
- Optional terminal output with ASCII intensity ramp
- Camera with yaw/pitch rotation and jump physics
- Plane helpers (``draw_plane_xy``, ``draw_plane_xz``, ``draw_plane_yz``)
- Solid cube + wireframe edges
- GUI keyboard input and optional terminal input via ``pynput``
