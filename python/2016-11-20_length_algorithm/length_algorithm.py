algorized_num2 = 0
number = raw_input('Please type in a number in word form between 1 and 100 (no space, no hyphen): ')
algorized_num = number
print algorized_num
def find_length(algorized_num, number, algorized_num2):
	if len(number) == 3 or len(algorized_num) == 3 or len(algorized_num2) == 3:
		algorized_num2 = 'three' 
		algorized_num = 'three'
	elif len(number) == 4 or len(algorized_num) == 4 or len(algorized_num2) == 4:
		algorized_num = 'four'
		algorized_num2 = 'four'
	elif len(number) == 5 or len(algorized_num) == 5 or len(algorized_num2) == 5:
		algorized_num = 'five'
		algorized_num2 = 'five'
	elif len(number) == 6 or len(algorized_num) == 6 or len(algorized_num2) == 6:
		algorized_num = 'six'
		algorized_num2 = 'six'
	elif len(number) == 7 or len(algorized_num) == 7 or len(algorized_num2) == 7:
		algorized_num2 = 'seven'
		algorized_num = 'seven'
	elif len(number) == 8 or len(algorized_num) == 8 or len(algorized_num2) == 8:
		algorized_num2 = 'eight'
		algorized_num = 'eight'
	elif len(number) == 9 or len(algorized_num) == 9 or len(algorized_num2) == 9:
		algorized_num2 = 'nine'
		algorized_num = 'nine'
	elif len(number) == 10 or len(algorized_num) == 10 or len(algorized_num2) == 10:
		algorized_num2 = 'ten'
		algorized_num = 'ten'
	elif len(number) == 11 or len(algorized_num) == 11 or len(algorized_num2) == 11:
		algorized_num2 = 'eleven'
		algorized_num = 'eleven'
	return len(algorized_num) and len(algorized_num2)		
while algorized_num or number or algorized_num2 != 'four':
	find_length(algorized_num, number, algorized_num2)
	algorized_num = len(algorized_num2) 
	print algorized_num, '=', len(algorized_num2) 
	find_length(algorized_num, number, algorized_num2)
	algorized_num2 = len(algorized_num) 
	print algorized_num2, '=', len(algorized_num)
