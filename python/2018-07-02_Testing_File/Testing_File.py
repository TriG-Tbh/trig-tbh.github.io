# This file is used to quickly be able to test Python code

# This file's main intention is to test Python code before it is run

# Please set up any variables and imports before running the code
from time import sleep
from random import randint
x = randint(1, 3)
while x != 3:
	print(x)
	if x == 1:
		print("fail")
	elif x == 2:
		print("wait")
	x = randint(1, 3)
print("done")
