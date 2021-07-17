from pynput.keyboard import Key, Listener, Controller
import logging

log_dir = ""

logging.basicConfig(filename=(log_dir + "Key Log.txt"), level=logging.DEBUG, format='%(asctime)s: %(messages)s:')

keyboard = Controller()

def on_press(key):
        if key == Key.space:
            keyboard.press('x')
            keyboard.release('x')
            keyboard.press('z')
            keyboard.release('z')
        if key == Key.esc:
                return False

with Listener(on_press=on_press) as listener:
        listener.join()
        
