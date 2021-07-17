from time import sleep
import math
import pdb

full_check = 0
factor_show = 0
verdict_show = 0

verdict = ""

mod_number = 0

print("Hello. Welcome to the Prime/Composite Machine v. 1.0")
sleep(1.5)
print("This machine is used to calculate a number's factors and if they are prime")
sleep(3)
calculating = True
while calculating:
	
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
		sleep(5)


	if verdict_show == 1:
		print("\n" + "So, " + str(number) + " is a...")
		sleep(1)
		for i in xrange(1, 4):
			print("." + "\n")
			sleep(1)
		if len((factors_list)) > 2:
			verdict = "composite"
		else:
			verdict = "prime"
		print(verdict + " number.")
	
		sleep(1)

	k_o_c = raw_input("\n" + "Would you like to try again? y/n ")
	
	if k_o_c == "y":
		continue
	else:	
		break
