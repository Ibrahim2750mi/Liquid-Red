from importlib import import_module

from .camera import Camera
from . import geometry
from .grid import Renderer
from .objects import Cube, Edge, Object


def __getattr__(name):
    # ``LiquidRed.events`` starts a global pynput keyboard listener when imported, which GUI
    # users (LiquidRed.gui) don't want. Load it on first access instead of at package import.
    # ``from LiquidRed.events import pressed`` is unaffected.
    if name == "events":
        return import_module(".events", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
