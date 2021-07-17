import hashlib, bcrypt

password = input("Password to hash: ")
print("\nSHA1:\n")
for _ in range(3):
    setpass = bytes(password, "utf-8")
    hash_object = hashlib.sha1(setpass)
    guess_pw = hash_object.hexdigest()
    print(guess_pw)

print("\nMD5:\n")
for _ in range(3):
    setpass = bytes(password, "utf-8")
    hash_object = hashlib.md5(setpass)
    guess_pw = hash_object.hexdigest()
    print(guess_pw)

print("\nBCRYPT:\n")
for _ in range(3):
    hashed = bcrypt.hashpw(setpass, bcrypt.gensalt(10))
    print(hashed)