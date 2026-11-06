"""
SDL2 window backend for LiquidRed.

Replaces the two terminal-bound pieces of the engine:

- output: ``Renderer.show_grid()`` prints ASCII, ``Window.present()`` draws the same grid as pixels
- input:  ``LiquidRed.events`` uses a global pynput listener, ``Window.pressed`` is filled from window events

Requires the optional extra: ``pip install LiquidRed[gui]``.
"""
import ctypes
import time

import numpy as np

try:
    import sdl2
except ImportError as exc:  # pragma: no cover
    raise ImportError("LiquidRed.gui needs PySDL2: pip install 'LiquidRed[gui]'") from exc

#: Characters the renderer can write, darkest to brightest (" " is an empty cell).
#: ``".:-=+*#%@"`` is the ramp used by :func:`LiquidRed.geometry.get_lambert_char`.
RAMP = " .:-=+*#%@"


def _gray(t):
    return 255 * t, 255 * t, 255 * t


def _red(t):
    return 255 * t, 70 * t**2, 50 * t**2


#: Palette name -> function mapping brightness ``t`` in [0, 1] to an (r, g, b) tuple.
PALETTES = {"red": _red, "gray": _gray}

_KEYMAP = {
    sdl2.SDLK_w: "w",
    sdl2.SDLK_a: "a",
    sdl2.SDLK_s: "s",
    sdl2.SDLK_d: "d",
    sdl2.SDLK_j: "j",
    sdl2.SDLK_SPACE: "j",
    sdl2.SDLK_COMMA: ",",
    sdl2.SDLK_PERIOD: ".",
    sdl2.SDLK_LEFT: "left",
    sdl2.SDLK_RIGHT: "right",
    sdl2.SDLK_UP: "up",
    sdl2.SDLK_DOWN: "down",
}


def make_lut(palette="red"):
    """
    Build a lookup table from character code point to RGB.

    Parameters
    ----------
    palette : str or callable
        A key of :data:`PALETTES`, or a function ``t -> (r, g, b)`` with ``t`` in [0, 1].

    Returns
    -------
    np.ndarray
        ``(128, 3)`` uint8 array indexed by ``ord(char)``. Empty cells stay black.
    """
    fn = PALETTES[palette] if isinstance(palette, str) else palette
    lut = np.zeros((128, 3), dtype=np.uint8)
    for i, ch in enumerate(RAMP[1:]):
        t = 0.18 + 0.82 * i / (len(RAMP) - 2)  # darkest lit char is dim, not black
        lut[ord(ch)] = [int(c) for c in fn(t)]
    return lut


class Window:
    """
    SDL2 window that displays a :class:`~LiquidRed.grid.Renderer`.

    Parameters
    ----------
    renderer : Renderer
        Renderer whose ``grid`` is displayed.
    title : str, optional
        Window title.
    scale : int, optional
        Window pixels per grid cell. ``0`` picks a size that gives roughly a 768px wide window.
    palette : str or callable, optional
        See :func:`make_lut`.
    fps : int, optional
        Frame cap used by :meth:`tick`.

    Attributes
    ----------
    pressed : set[str]
        Currently held keys, in the format ``Camera.update`` expects
        (``"w"``, ``"a"``, ``"s"``, ``"d"``, ``","``, ``"."``, ``"j"``, plus
        ``"left"``, ``"right"``, ``"up"``, ``"down"``).

    Examples
    --------
    >>> win = Window(renderer)
    >>> while win.poll():
    ...     camera.update(win.pressed, time.time())
    ...     renderer.clear_grid()
    ...     renderer.draw_plane_xz(-4, 4, 0, 20, 2)
    ...     win.present()
    ...     win.tick()
    >>> win.close()
    """

    def __init__(self, renderer, title="LiquidRed", scale=0, palette="red", fps=60):
        self.renderer = renderer
        self.pressed = set()
        self.lut = make_lut(palette)
        self._frame_time = 1.0 / fps
        self._t0 = time.perf_counter()

        w, h = renderer.canvas_width, renderer.canvas_height
        scale = scale or max(1, 768 // w)

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise RuntimeError(sdl2.SDL_GetError().decode())
        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"0")  # nearest-neighbour upscale

        self._win = sdl2.SDL_CreateWindow(
            title.encode(),
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            w * scale,
            h * scale,
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE,
        )
        self._ren = sdl2.SDL_CreateRenderer(
            self._win, -1, sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        ) or sdl2.SDL_CreateRenderer(self._win, -1, sdl2.SDL_RENDERER_SOFTWARE)
        sdl2.SDL_RenderSetLogicalSize(self._ren, w, h)  # keeps aspect ratio when resized
        self._tex = sdl2.SDL_CreateTexture(
            self._ren, sdl2.SDL_PIXELFORMAT_RGB24, sdl2.SDL_TEXTUREACCESS_STREAMING, w, h
        )
        self._event = sdl2.SDL_Event()

    def poll(self):
        """
        Process window events and update :attr:`pressed`.

        Returns
        -------
        bool
            ``False`` once the window was closed or Esc was pressed.
        """
        running = True
        ev = self._event
        while sdl2.SDL_PollEvent(ctypes.byref(ev)):
            if ev.type == sdl2.SDL_QUIT:
                running = False
            elif ev.type == sdl2.SDL_KEYDOWN:
                if ev.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                key = _KEYMAP.get(ev.key.keysym.sym)
                if key:
                    self.pressed.add(key)
            elif ev.type == sdl2.SDL_KEYUP:
                self.pressed.discard(_KEYMAP.get(ev.key.keysym.sym))
            elif ev.type == sdl2.SDL_WINDOWEVENT and ev.window.event == sdl2.SDL_WINDOWEVENT_FOCUS_LOST:
                self.pressed.clear()  # no stuck keys after alt-tab
        return running

    def to_rgb(self):
        """
        Convert ``renderer.grid`` to an image.

        Returns
        -------
        np.ndarray
            ``(height, width, 3)`` uint8 array.
        """
        # '<U1' stores one uint32 code point per cell, so a view gives the ordinals without a copy
        codes = self.renderer.grid.view(np.uint32)
        return self.lut[np.minimum(codes, 127)]

    def present(self):
        """
        Draw the current grid to the window. GUI replacement for ``Renderer.show_grid``.
        """
        rgb = self.to_rgb()
        sdl2.SDL_UpdateTexture(self._tex, None, rgb.ctypes.data_as(ctypes.c_void_p), rgb.shape[1] * 3)
        sdl2.SDL_RenderClear(self._ren)
        sdl2.SDL_RenderCopy(self._ren, self._tex, None, None)
        sdl2.SDL_RenderPresent(self._ren)

    def tick(self):
        """
        Sleep so the loop runs at no more than ``fps``. ``Camera.update`` moves a fixed
        amount per call, so this also sets movement speed.
        """
        spare = self._frame_time - (time.perf_counter() - self._t0)
        if spare > 0:
            sdl2.SDL_Delay(int(spare * 1000))
        self._t0 = time.perf_counter()

    def close(self):
        """
        Destroy the window and shut SDL down.
        """
        sdl2.SDL_DestroyTexture(self._tex)
        sdl2.SDL_DestroyRenderer(self._ren)
        sdl2.SDL_DestroyWindow(self._win)
        sdl2.SDL_Quit()
