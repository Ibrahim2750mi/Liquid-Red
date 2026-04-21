from pynput import keyboard

pressed = set()


def on_press(key):
    """
    When a key is pressed, it adds it to the pressed set.
    """
    pressed.add(getattr(key, "char", key))


def on_release(key):
    """
    When a key is released, it removes it from the pressed set.
    """
    pressed.discard(getattr(key, "char", key))


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
