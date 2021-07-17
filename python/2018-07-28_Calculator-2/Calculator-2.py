from time import sleep
import math

stored_var1 = 0
stored_var2 = 0
stored_var3 = 0

one_number_operation = 0
while True:
	num1 = raw_input("Type in your first number" + "\n" + "(Note: you can enter \'var1\' through \'var3\' to make the variable the first number): ")
	if num1 == "var1":
		num1 = stored_var1
	if num1 == "var2":
		num1 = stored_var2
	if num1 == "var3":
		num1 = stored_var3	
	
	operation = input("\n" + "Type in your operation: " + "\n"
	"Basic operations: add, sub, mul, div" + "\n"
	"Secondary operations: squared, sqrt, circum, mod" + "\n"
	"Trig: sin, cos, tan" + "\n"
	"Other: var (updates variable to the number you typed in)" + "\n\n"
	"Please make a selection: ")

