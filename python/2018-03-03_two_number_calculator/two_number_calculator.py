special_function = 0

from time import sleep
import math
while True:
	special_function = 0
	num1 = input('Please type in your first number: ')
	num1 = float(num1)
		
	operator = input('\n' + 'Please type in your operator:' + '\n' +
	'Basic functions: addition, subtraction, multiplication, division' + '\n' +
	'2nd functions: squared, circumference, sqrt' + '\n'+
	'Trigonometric functions: sin, cos, tan' + '\n')
	
	# Special functions
	if str(operator) == 'squared':
		special_function = 1
		final_answer = float(num1) * float(num1)
		  
	if str(operator) == 'circumference':
		special_function = 1
		print('The first number will be the diameter of the circle.')
		sleep(3)
		pi = float(3.14)
		if int(num1) != type(float):
			num1 = int(num1) + (.0)
		print(int(num1))	
		final_answer = float(int(num1)) * float(pi)
			
	if str(operator) == 'sqrt':
		special_function = 1
		final_answer = math.sqrt(int(num1))		
			
	# Trigonometric functions		
	if str(operator) == 'sin':
		special_function = 1
		final_answer = math.sin(math.radians(float(num1)))
		
	if str(operator) == 'cos':
		special_function = 1
		final_answer = math.cos(math.radians(float(num1)))
		
	if str(operator) == 'tan':
		special_function = 1
		final_answer = math.tan(math.radians(float(num1)))
				
	if int(special_function) != 1:	
	# Sees if the operator isn't circumfrence, squared or anything like that because they only need one number
		num2 = input('Please type in your second number: ')
			
	if int(special_function) != 1:				
		if str(operator) == 'addition':
			final_answer = eval(num1)+eval(num2)
		elif str(operator) == 'subtraction':
			final_answer = eval(num1)-eval(num2)
		elif str(operator) == 'multiplication':
			final_answer = eval(num1)*eval(num2)
		elif str(operator) == 'division':
			final_answer = eval(num1)/eval(num2)
	if special_function != 1:
 		print(num1 + ' ' + str(operator) + ' ' + num2 + ' = ' + str(final_answer))
	else:
		final_answer = "%2f" % final_answer
		if str(operator) == 'circumference':
			print('The circumference of ' + str(num1) + ' (being the diameter) is ' + str(final_answer) + '.') 	
		elif str(operator) == 'tan':
			if int(num1) >= 90:
				print('It is highly likely that the number will equal infinity because the number you  entered is greater than or equal to 90.')
				sleep(5)
				continue
			else:
				print(num1 + ' ' + str(operator) + ' = ' + str(final_answer) + '.')		
		else:
			print(num1 + ' ' + str(operator) + ' = ' + str(final_answer) + '. Please round if it is too long.')
	sleep(5)
