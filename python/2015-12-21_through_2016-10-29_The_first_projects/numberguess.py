print ("I can guess your number!")
var_a = input("Type a three digit number, then type it again, then press enter.")
while var_a not in range(100100, 1000000):
	var_a = input("Type a three digit number, then type it again, then press enter.")
var_b = var_a / 7
var_c = var_b / 11
var_d = var_c / 13
print ("Your number is: " + str(var_d))
