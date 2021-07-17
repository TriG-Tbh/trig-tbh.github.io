import math
import time
num1 = ""
action = ""
operation = ""
num2 = ""
result = ""
current_string = ""
while action != "end":
	action = raw_input("ENTER AN ACTION \n"
	"\"calculator\": standard calculator (+, -, *, /, etc.) \n"
	"\"pemdas\": order of operations calculator \n"
	"\"factor\": prime/composite and factor calculator \n"
	"\"end\": stops the program \n"
	"Please make a selection: ")
	action = action.lower()
	if action == "calculator":
		num1 = raw_input("Please type in the first number: ")
		num1 = float(num1)
		operation = input("Enter an operation: \n"
		"Standard: \"add\" (+), \"sub\" (-), \"mul\" (*), \"div\" (/) \n"
		"Secondary: \"power\" (x^y), \"squared\", \"sqrt\" (square root) \n"  
		"Trigonometry: \"sin\", \"cos\", \"tan\" \n"
		"Please make a selection: ")
		if 
	elif action == "pemdas":
		num1 = ""
		current_string = ""
		while num1 != "end":
			num1 = raw_input("The current string is " + current_string + ". Please type in the next character (\"end\" to end): ")
			if num1 == "+":
				current_string = current_string + "+"
			elif num1 == "-":
				current_string = current_string + "-"
			elif num1 == "*":
				current_string = current_string + "*"
			elif num1 == "/":
				current_string = current_string + "/"
			elif num1 == "^":
				current_string = current_string + "**"
			elif num1 == "end":
				pass
			elif num1 != "_" and num1 != ".":
				num1 = str(num1)
				current_string = current_string + num1
		current_string = str(current_string)
		result = eval(current_string)
		print("The answer is " + int(result))
	elif action == "factor":
		from time import sleep
		import math
		import pdb

		full_check = 0
		factor_show = 0
		verdict_show = 0

		verdict = ""

		mod_number = 0


		
		(factors_list) = []
		
		number = input("\n" + "Please type in a number for the machine to calculate: " + "\n\n")

		method = input("\n" + "Type in the preset you want to use for calculating - " + "\n"
	"1: Normal (all smaller numbers, factors and verdict)" + "\n"
	"2: Speed/BigFix (less precise, no factors, quicker verdict, numbers greater than 1000000000 require this)" + "\n"
	"3: NoVerdict (used to find the factors of a number)" + "\n"
	"Please type in a preset: ")

		if method == 1:
			full_check = 1
			factor_show = 1
			verdict_show = 1

		if method == 2:
			full_check = 0
			factor_show = 0
			verdict_show = 1

		if method == 3:
			full_check = 1
			factor_show = 1
			verdict_show = 0
		
		print("\n" + "Calculating...")
			
		div_num = 1

		if full_check == 1:
			for i in xrange(1, number + 1):
				mod_number = int(int(number) % int(div_num))
				if mod_number != 0:
					div_num = div_num + 1
				else:
					factors_list.insert(len(factors_list), div_num)
					div_num = div_num + 1
					
		else:
			for i in xrange(1, int(math.sqrt(number + 1))):
				mod_number = int(int(number) % int(div_num))
				if mod_number != 0:
					div_num = div_num + 1
				else:
					factors_list.insert(len(factors_list), div_num)
					div_num = div_num + 1
	 
		if factor_show == 1:
			print("\n" + "The factors of " + str(number) + " are: ")
			sleep(1)
			print '%s' % ', '.join(map(str, factors_list))
			sleep(3)


		if verdict_show == 1:
			print("\n" + "So, " + str(number) + " is a...")
			sleep(1)
			for i in xrange(1, 4):
				print("." + "\n")
				sleep(0.5)
			if len((factors_list)) > 2:
				verdict = "composite"
			else:
				verdict = "prime"
			print(verdict + " number.")
		
			sleep(1)

	elif action == "end":
		print("Bye")
		pass
	else:
		print("Please enter a valid action")
		pass
	
