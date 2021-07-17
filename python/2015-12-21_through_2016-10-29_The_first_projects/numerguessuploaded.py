from time import sleep
print ('I can guess your number!')
number = input('Type in a number between 1 and 100! ')
while int(number) not in range(1, 100):
	number = input('No, no, pick a number from 1 through 100!')
50_yes_no = input('Is your number 50? yes/no ')

