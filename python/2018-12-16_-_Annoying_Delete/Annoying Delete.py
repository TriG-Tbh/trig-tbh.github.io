from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller
from time import sleep

delete = True

board = Controller()

def exit_menu():
	delete = False
	board.press(Key.esc)
	sleep(0.01)
	board.release(Key.esc)
	delete = True

def on_press(key):
	if key == Key.cmd:
		exit_menu()
	if delete == True:
		if (key) != (Key.backspace) and delete == True:
			sleep(0.01)
			board.press(Key.backspace)
			board.release(Key.backspace)

	

# Collect events until released
with keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
	listener.join()



def on_move(x, y):
	print('Pointer moved to {0}'.format(
		(x, y)))

def on_click(x, y, button, pressed):
	print('{0} at {1}'.format(
		'Pressed' if pressed else 'Released',
		(x, y)))
	if not pressed:
		# Stop listener
		return False

def on_scroll(x, y, dx, dy):
	print('Scrolled {0} at {1}'.format(
		'down' if dy < 0 else 'up',
		(x, y)))

# Collect events until released
with mouse.Listener(
		on_move=on_move,
		on_click=on_click,
		on_scroll=on_scroll) as listener:
	listener.join()
