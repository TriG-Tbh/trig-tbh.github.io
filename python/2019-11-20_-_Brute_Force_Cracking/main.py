from itertools import product
import hashlib
import sys
import string as s
import os

chars = s.printable

code = input("Enter code: ")

code_hash_object = hashlib.md5(bytes(str(code), "utf-8"))
code_hex_dig = code_hash_object.hexdigest()


length = 1
breakloop = False

while True:
    to_attempt = product(chars, repeat=length)
    for attempt in to_attempt:
        #os.system("clear")
        string = "".join(attempt)
        hash_object = hashlib.md5(bytes(string, "utf-8"))
        hex_dig = hash_object.hexdigest()
        print(string + "\r")
        if code_hex_dig == hex_dig:
            breakloop = True
            break
    length += 1
    if breakloop:
        break

print("\n\n{}".format(string))