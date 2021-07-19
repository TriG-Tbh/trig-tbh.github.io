import os
import shutil

directory = os.path.dirname(os.path.realpath(__file__))
serverdir = directory + "/Servers"
print(directory)
directories = [x[0] for x in os.walk(serverdir)]
directories.remove(serverdir)
for dir in directories:
    print(dir)

input()
print("Cleaning up empty directories...")
for dir in directories:
	if not os.listdir(dir):
		shutil.rmtree(dir)
from webptojpg import convert
print("Converting...")
for dir in directories:
	print(dir)
	convert(dir)
print("Done")