skips = 0
from time import sleep
tutorial = 'y'
while tutorial == 'y':
	tutorial = raw_input('Do you want to read the tutorial? y/n: ')
	if tutorial == 'y':
		print('Hi. Welcome to Math Flash.')
		sleep(1)
		print('This is a program that is supposed to help with your math skills.') 
		sleep(2)
		print('It will ask you what you want the operator, number to (fill in operator here) and the biggest number you want to "operate" with.')
		sleep(4)
		print('Essentialy, it\'s really a table maker.')
		sleep(1)
		print('When it asks you a question, there are 3 ways to answer it:')
		sleep(2)
		print('A: You can answer it directly.')
		sleep(1)
		print('It will ask the question, and say whether or not the answer is correct and give the real answer.')
		sleep(3)
		print('B: You can type in \'skip\' which skips the current question.')
		sleep(1)
		print('C: You can type in \'break\' which restarts the table and asks for a new one. ') 
		sleep(3)
		print('Or you can hit the ctrl or comm button, then hit c if you want to exit the program completely.')
		sleep(3)
		print('Now let\'s do some math!')
		sleep(1)
while True:
	operator = raw_input('Please type in the operator (type in: add, subtract, multiply or divide): ')
	table = raw_input('Please type in the number you want to ' + str(operator) + ' with: ')
	range_of_table = raw_input('Please type in the bigest number you want to ' + str(operator) + ' ' + str(table) + ' ' + 'by: ')
	if str(operator) == 'add':
		table_operator = '+'
		table_operator2 = 'plus'
	elif str(operator) == 'subtract':
		table_operator = '-'
		table_operator2 = 'minus'
	elif str(operator) == 'multiply':
		table_operator = '*'
		table_operator2 = 'by'
	elif str(operator) == 'divide':
		table_operator = '/'
		table_operator2 = 'divided by'		
	for i in range(1, (int(range_of_table) + 1)):
		print('What\'s ' + int(table) + str(table_operator2) + int(i) + '?')
		guess = input()	
		if str(guess) == 'stop':
			quit
		if str(guess) == 'skip':
			if int(skips) < 3:
				skips = skips + 1	
				print('Skipping...')
				sleep(1)
				continue	
			else:
				print ('Sorry, but you\'ve used the maximum amount of skips.')
				question()	
		ans = eval(str(i)+table_operator+str(table))
		if int(guess) == int(ans):
			print ('Yes! You\'re correct!')
			sleep(1)
		elif int(guess) != int(ans):
			print ('No, it\'s ' + str(ans) + '.')
			sleep(1)

