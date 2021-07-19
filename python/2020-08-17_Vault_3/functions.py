import argparse
import base64
import errno
import getpass
import hashlib
import logging
import os
import secrets
import sys
import tempfile
from urllib.parse import urlsplit
try:
    import winreg
except ImportError:
    pass
import zipfile

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import requests

import windows
import pyotp
import re
from PIL import Image
import io
import settings

__PROG__ = 'vault'
__AUTHORS__ = ('TriG-Tbh', 'Dogeek')
__version__ = (1, 0, 0)


RURL = re.compile('https?:\/\/(?:www\.)?.+')


logger = logging.getLogger(__name__)


def ask_password():
    confirm = ''
    password = '0'
    use2fa = False
    key = pyotp.random_base32()
    while confirm != password:
        passwordwindow = windows.CreatePassword()
        if passwordwindow.password == "" and passwordwindow.confirmpw == "":
            sys.exit(0)
        elif passwordwindow.password == "" or passwordwindow.confirmpw == "":
            continue
        password = passwordwindow.password
        confirm = passwordwindow.confirmpw
        use2fa = passwordwindow.use2fa
    
    if use2fa:
        mfasetup = windows.MfaWindow(login=False, code=key)
        if not mfasetup.logged_in:
            use2fa = False
    
    if use2fa:
        return password, key
    else:
        return password, None


def decrypt_mfa(password, salt, code):
    code = bytes(code, encoding="ascii")
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**12,
        r=8,
        p=1,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf8'))).decode('ascii')
    fernet = Fernet(key)
    return fernet.decrypt(code).decode("ascii")


def encrypt_mfa(password, salt, code):
    code = bytes(code, encoding="ascii")
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**12,
        r=8,
        p=1,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf8'))).decode('ascii')
    fernet = Fernet(key)
    return fernet.encrypt(code)

    


def create_new_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**12,
        r=8,
        p=1,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf8'))).decode('ascii')

    if sys.platform.startswith('win'):
        key_path = 'SOFTWARE\\' + __PROG__.capitalize()
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_path,
                0, winreg.KEY_WRITE,
            )
            winreg.SetValueEx(registry_key, 'key', 0, winreg.REG_SZ, key)
        except WindowsError:
            raise
    else:
        key_path = os.path.join(os.path.expanduser('~/.config'), __PROG__.capitalize())
        with open(os.path.join(key_path, 'key'), 'w') as file_handler:
            file_handler.write(key)


def create_new_password(generate_key=False):
    password, mfakey = ask_password()
    salt = secrets.token_bytes(16)

    mfapw = ""

    if mfakey is not None:
        mfapw = password + mfakey
        mfapw = hashlib.blake2b(
            mfapw.encode('utf8'), salt=salt,
            person=getpass.getuser().encode('utf8'),
        ).hexdigest()
        mfakey = encrypt_mfa(password, salt, mfakey)
    else:
        mfakey = ""


    if isinstance(mfakey, bytes):
        mfakey = mfakey.decode('ascii')
    password = hashlib.blake2b(
        password.encode('utf8'), salt=salt,
        person=getpass.getuser().encode('utf8'),
    ).hexdigest()
    salt = base64.b64encode(salt).decode('ascii')

    if sys.platform.startswith('win'):
        pass_path = 'SOFTWARE\\' + __PROG__.capitalize()
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, pass_path)
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, pass_path,
                0, winreg.KEY_WRITE,
            )
            winreg.SetValueEx(registry_key, 'password', 0, winreg.REG_SZ, password)
            winreg.SetValueEx(registry_key, 'mfapw', 0, winreg.REG_SZ, mfapw)
            winreg.SetValueEx(registry_key, 'mfakey', 0, winreg.REG_SZ, mfakey)
            winreg.SetValueEx(registry_key, 'salt', 0, winreg.REG_SZ, salt)
        except WindowsError:
            raise
    else:
        pass_path = os.path.join(os.path.expanduser('~/.config'), __PROG__.capitalize())
        os.makedirs(pass_path, exist_ok=True)
        with open(os.path.join(pass_path, 'password'), 'w') as f:
            f.write(password)
        with open(os.path.join(pass_path, 'mfapw'), 'w') as f:
            f.write(mfapw)
        with open(os.path.join(pass_path, 'mfakey'), 'w') as f:
            f.write(mfakey)
        with open(os.path.join(pass_path, 'salt'), 'w') as f:
            f.write(salt)

    if generate_key:
        if mfapw != "":
            create_new_key(mfapw, base64.b64decode(salt))
        else:
            create_new_key(password, base64.b64decode(salt))

    return password, mfapw, mfakey, salt, True


def get_stored_password():
    if sys.platform.startswith('win'):
        pass_path = 'SOFTWARE\\' + __PROG__.capitalize()
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, pass_path,
                0, winreg.KEY_READ,
            )
            password, regtype = winreg.QueryValueEx(registry_key, 'password')
            mfapw, regtype = winreg.QueryValueEx(registry_key, 'mfapw')
            mfakey, regtype = winreg.QueryValueEx(registry_key, 'mfakey')
            salt, regtype = winreg.QueryValueEx(registry_key, 'salt')
            salt = base64.b64decode(salt)
            winreg.CloseKey(registry_key)
            return password, mfapw, mfakey, salt, False
        except FileNotFoundError:
            return create_new_password(generate_key=True)
    else:
        pass_path = os.path.join(os.path.expanduser('~/.config'), __PROG__.capitalize())
        try:
            with open(os.path.join(pass_path, 'password'), 'r') as f:
                password = f.read()

            with open(os.path.join(pass_path, 'mfapw'), 'r') as f:
                mfapw = f.read()
            with open(os.path.join(pass_path, 'mfakey'), 'r') as f:
                mfakey = f.read()
            with open(os.path.join(pass_path, 'salt'), 'r') as f:
                salt = f.read()
                salt = base64.b64decode(salt)
            return password, mfapw, mfakey, salt, False
        except FileNotFoundError:
            return create_new_password(generate_key=True)


def get_encryption_key():
    global key
    if sys.platform.startswith('win'):
        key_path = 'SOFTWARE\\' + __PROG__.capitalize()
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path,
            0, winreg.KEY_READ,
        )
        key, regtype = winreg.QueryValueEx(registry_key, 'key')
        winreg.CloseKey(registry_key)
    else:
        key_path = os.path.join(os.path.expanduser('~/.config'), __PROG__.capitalize())
        with open(os.path.join(key_path, 'key'), 'r') as f:
            temp = f.read()
    
        key = temp.encode('ascii')
    return key


def get_version():
    return f"{__PROG__} by {', '.join(a for a in __AUTHORS__)} v{'.'.join(str(v) for v in __version__)}"


def login(password=None):
    stored_pass, mfapw, mfakey, salt, logged_in = get_stored_password()
    global fernet, key
    if logged_in:
        fernet = Fernet(key)
        return True
    if password is None:
        password = windows.PasswordWindow().password
    hashedpw = hashlib.blake2b(
        password.encode('utf8'), salt=salt,
        person=getpass.getuser().encode('utf8'),
    ).hexdigest()
    if secrets.compare_digest(hashedpw, stored_pass):
        if mfakey != "":
            code = decrypt_mfa(password, salt, mfakey)
            accepted = windows.MfaWindow(code=code).logged_in
            if accepted:
                fernet = Fernet(get_encryption_key())
                return True
            else:
                return False
        fernet = Fernet(get_encryption_key())
        
        return True
    return False



def encrypt(path=None, delete=True, silent=False):
    logger.info('Starting to encrypt %s...', str(path))
    if RURL.match(path):
        logger.info('URL flag passed, trying to download the file...')
        try:
            data = requests.get(path).content
        except requests.RequestException as e:
            logger.exception(str(e))
            raise
        name = urlsplit(path).path.split('/')[-1]
        path = os.path.join(os.getcwd(), name)
        if silent:
            encrypted = fernet.encrypt(data)
            return encrypted

    elif os.path.isdir(path):
        logger.info('Directory detected, zipping the directory to encrypt it...')
        delete = True
        filename = os.path.split(path)[-1] + '.zip'

        file_handler = zipfile.ZipFile(
            os.path.join(path, filename), 'w',
            compression=zipfile.ZIP_LZMA,
        )
        for root, dirs, files in os.walk(path):
            for file_ in files:
                file_handler.write(os.path.join(root, file_))
        file_handler.close()
        path = os.path.join(path, filename)
        with open(path, 'rb') as file_handler:
            data = filehandler.read()
        name = os.path.split(path)[-1]
    else:
        with open(path, 'rb') as file_handler:
            data = file_handler.read()
        filename = os.path.split(path)[-1]
        name = os.path.split(path)[-1]

    directory = os.path.dirname(path)
    if directory:
        os.chdir(directory)

    
    try:
        extension = "." + ".".join(name.split(".")[1:])
    except:
        extension = ""
    directory = os.path.dirname(os.path.realpath(path))
    os.chdir(directory)
    savepath = os.path.join(directory, name)
    savepath = savepath[:-len(extension)] + ".enc"

    encrypted = fernet.encrypt(data)


    with open(savepath, "wb") as f:
        f.write(encrypted)

    with open(savepath, "a") as f:
        f.write("|" + extension)

    with open(savepath, "rb") as f:
        encrypted_bytes = f.read()
    double_encrypted = fernet.encrypt(encrypted_bytes)
    with open(savepath, "wb") as f:
        f.write(double_encrypted)


    if delete and os.path.exists(path):
        logger.info('Delete flag passed, deleting %s', path)
        os.remove(path)
    return savepath

def decrypt(path=None, delete=True, silent=False):
    if not path.endswith('.enc'):
        return errno.EBADF

    directory = os.path.dirname(path)
    if directory:
        os.chdir(directory)

    with open(path, "rb") as f:
        double_encrypted = f.read()
    single_encrypted = fernet.decrypt(double_encrypted)
    text = single_encrypted.decode('utf-8')


    name = os.path.split(path)[-1]

    name = name[:-4]

    if "|" not in text:
        savepath = os.path.join(directory, name)
    else:
        extension = text.split("|")[-1][1:]
        savepath = os.path.join(directory, name)
        savepath = savepath + extension
    
    text = text[:-5]
    data = text.encode()
    
    decrypted = fernet.decrypt(data)

    
    if silent:
        return decrypted
    with open(savepath, "wb") as f:
        f.write(decrypted)

    if delete and os.path.exists(path):
        os.remove(path)

    return savepath
    




def change_password(fernet=None, generate_key=False):
    if generate_key:
        confirm = input('This will render your already encrypted files undecypherable.\nAre you sure you want to proceed (y/n)? ')
        if confirm.lower().startswith('n') or not confirm:
            generate_key = False
            logger.info('Key will not be regenerated.')
    try:
        create_new_password(generate_key=generate_key)
    except Exception as e:
        logger.exception(str(e))
        raise

def validate_image(obj):
    try:
        Image.open(obj)
    except Exception as e:
        return False
    return True


def get_image(path):
    name = ""
    if RURL.match(path):
        firstpos = path.rfind("/")
        lastpos = len(path)
        name = path[firstpos+1:lastpos]
        try:
            data = requests.get(path).content
        except requests.RequestException as e:
            return None, None
        file = io.BytesIO(data)
    else:
        name = os.path.basename(os.path.realpath(path))
        if os.path.isfile(path):
            if path.endswith(".enc"):
                try:
                    data = decrypt(path, silent=True)
                except Exception as e:
                    print(str(e))
                    return None, None
                file = io.BytesIO(data)
            else:
                with open(path, "rb") as f:
                    file = io.BytesIO(f.read())
        else:
            return None, None
    if validate_image(file):
        return name, Image.open(file)
    else:
        return None, None
