import os
import getpass
import functions

"""if __name__ == "__main__":
    functions.clear()
    password = getpass.getpass("Password: ")
    if not functions.login(password):
        import sys
        print("Invalid password")
        sys.exit(1)
"""

basedir = os.path.dirname(os.path.realpath(__file__))
imgpath = os.path.join(basedir, "Images")
files = [os.path.join(imgpath, f) for f in os.listdir(
    imgpath) if os.path.isfile(os.path.join(imgpath, f))]
files = sorted(files)

i = 0
for file in files:
    """with open(file) as f:
        content = f.read()
    if content.endswith("|.enc.png"):
        with open(file, "w") as f:
            f.write(content[:-9])
    with open(file) as f:
        content = f.read()
    if not content.endswith("|.png"):
        with open(file, "a") as f:
            f.write("|.png")"""
    path = os.path.join(imgpath, "image{}.enc".format(i))
    os.rename(file, path)
    i += 1

print("Done")
