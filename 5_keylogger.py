from pynput import keyboard

log = ""
def on_press_callback(key):
    global log
    try:
        log += key.char
        print(f"\r{log}", end="")
    except AttributeError:
        if key == key.enter:
            print(f"\r{log}")
        elif key == key.space:
            log += " "
            print(f"\r{log}", end="")
        elif key == key.backspace:
            log = log[0:(len(log)-1)]
            print(f"\r{log}", end="")
        else: pass

keyboard_log = keyboard.Listener(on_press=on_press_callback)
with keyboard_log:
    keyboard_log.join()
