while True:	
	from time import sleep
	print('Please type in a number in word form between 1 and 1000 (no space, no hyphen, no \'and\'): ')
	algorized_num = input()
	algorized_num = number
	print algorized_num
	def find_length(algorized_num):
		if len(algorized_num) == 3:
			a = 'three'
		elif len(algorized_num) == 4:
			a = 'four'
		elif len(algorized_num) == 5:
			a = 'five'
		elif len(algorized_num) == 6:
			a = 'six'
		elif len(algorized_num) == 7:
			a = 'seven'
		elif len(algorized_num) == 8:
			a = 'eight'
		elif len(algorized_num) == 9:
			a = 'nine'
		elif len(algorized_num) == 10:
			a = 'ten'
		elif len(algorized_num) == 11:
			a = 'eleven'
		elif len(algorized_num) == 12:
			a = 'twelve'
		elif len(algorized_num) == 13:
			a = 'thirteen'	
		elif len(algorized_num) == 14:
			a = 'fourteen'	
		elif len(algorized_num) == 15:
			a = 'fifteen'
		elif len(algorized_num) == 16:
			a = 'sixteen'
		elif len(algorized_num) == 17:
			a = 'seventeen'
		elif len(algorized_num) == 18:
			a = 'eighteen'
		elif len(algorized_num) == 19:
			a = 'nineteen'
		elif len(algorized_num) == 20:
			a = 'twenty'
		elif len(algorized_num) == 21:
			a = 'twentyone'
		elif len(algorized_num) == 22:
			a = 'twentytwo'
		elif len(algorized_num) == 23:
			a = 'twentythree'
		elif len(algorized_num) == 24:
			a = 'twentyfour'	
		return a
	if algorized_num == 'four':
		print ('four = four.')
	while algorized_num != 'four':	
		algorized_num2 = find_length(algorized_num)
		print (algorized_num, '=', algorized_num2)
		sleep(1)
		algorized_num = algorized_num2	
	print ('four = four!')
	sleep(1)
