[Back to main page](/)

# Annoying Delete

## Date: 2018-12-16

Using Pynput, this would press the delete key whenever a key is pressed.

This would cause the pressed key to get deleted, as delete would be "pressed" immediately afterwards.

It should be noted that this does work, if on_release=on_release at line 30 is deleted.

-----

## Files

[Annoying Delete.py](Annoying Delete.py)