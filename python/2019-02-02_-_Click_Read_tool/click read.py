from pynput.mouse import Button, Controller
from time import sleep
from pynput import keyboard

global counter
counter = 0.00

def on_press(key):
    if key == keyboard.Key.esc:
        print()

def on_release(key):
    if key == keyboard.Key.esc:
        mouse = Controller()
        mouse.position = (1167, 503)
        mouse.press(Button.left)
        mouse.release(Button.left)

        from pynput import mouse
        
        def on_click(x, y, button, pressed):
            if pressed == True:
                while pressed:
                    counter = counter + 0.01
                    sleep(0.01)
            else:
                print(counter)
            if not pressed:
                # Stop listener
                return False

        # Collect events until released
        with mouse.Listener(
                on_click=on_click) as listener:
            listener.join()



with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
