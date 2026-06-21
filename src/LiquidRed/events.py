from pynput import keyboard

pressed = set()


def on_press(key):
    """
    Handle key press events.

    Adds the pressed key to the global ``pressed`` set.

    Parameters
    ----------
    key : pynput.keyboard.Key or pynput.keyboard.KeyCode
        Key object received from the listener.

    Notes
    -----
    - For character keys (e.g., 'w', 'a'), ``key.char`` is used.
    - For special keys (e.g., Shift, Space), the key object itself is stored.
    """
    pressed.add(getattr(key, "char", key))


def on_release(key):
    """
    Handle key release events.

    Removes the released key from the global ``pressed`` set.

    Parameters
    ----------
    key : pynput.keyboard.Key or pynput.keyboard.KeyCode
        Key object received from the listener.

    Notes
    -----
    Uses ``discard`` to safely remove keys without raising errors
    if the key is not present.
    """
    pressed.discard(getattr(key, "char", key))


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
