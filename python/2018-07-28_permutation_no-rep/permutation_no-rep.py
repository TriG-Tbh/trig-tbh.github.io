n = 0
number = input(">")
num2 = input(">>")
if num2 > number:
	break
n = number
x = number
for i in range(1, num2):
	n = n * (x - 1)
	x = x - 1
print(n)
