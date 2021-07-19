import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.fernet import Fernet

import os
import hashlib
from getpass import getpass as gp
import platform

import datetime

path = os.path.dirname(os.path.realpath(__file__))

def join(filepath):
    return os.path.join(path, filepath)

def readfile(key):
    if os.path.exists(join(".message")):
        with open(join(".message"), "rb") as f:
            encrypted = f.read()
    else:
        with open(join(".message"), "w") as f:
            f.write("")
    with open(join(".message"), "r") as f:
        if f.read() == "":
            return ""
    f =  Fernet(key)
    decrypted = f.decrypt(encrypted).decode()
    return decrypted.strip() + "\n"

def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        if platform.system() == "Darwin" and platform.machine().startswith("iP"):
            try:
                import console
                console.clear()
            except ImportError:
                pass

clear()
password_provided = gp("Password: ")
clear()
hash_object = hashlib.md5(str.encode(password_provided))
hashed = hash_object.hexdigest()
if hashed != "a592f8b138ef0a3897f0e2d83967b5c4":
    import sys
    sys.exit(1)
password = password_provided.encode()

salt = b'\xe2\x8b\x1c\x86F\x8b8\xf7\x124:R!\xcf\xa9\x8d'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend = default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
while True:
    clear()
    command = input("""Commands:
"add": Adds a line of text to the message
"view": Views the entire message
"delete": Deletes a line of text from the message
Choose a command: """)

    command = command.strip().lstrip().lower()
    if command == "add":
        clear()
        line = input("Line of text to append: ")
        text = readfile(key)
        text = (text + line).encode()
        f = Fernet(key)
        encrypted = f.encrypt(text)
        with open(join('.message'), "wb") as f:
            f.write(encrypted)
    elif command == "view":
        clear()
        text = readfile(key)
        print(text)
        input("Press enter to continue. ")