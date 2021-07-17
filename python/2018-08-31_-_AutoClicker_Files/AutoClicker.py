from pynput.mouse import Button, Controller
import time

mouse = Controller()

for i in range(5):
    print(str(6 - i) + " seconds remaining...")
    time.sleep(1)

for i in range(100):
    mouse.click(Button.left)
    time.sleep(0.001)
