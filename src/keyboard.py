from pynput import keyboard

pressed = set()

def on_press(key):
    pressed.add(getattr(key, 'char', key))

def on_release(key):
    pressed.discard(getattr(key, 'char', key))

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()