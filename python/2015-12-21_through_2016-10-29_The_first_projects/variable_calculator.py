calculator_passage = raw_input('Does this involve calculus? y/n: ')
if str(calculator_passage) == 'y':
	print ('Go find your professor!')
else:
	print ('It is not guaranteed that this follows Order of Operations, please try with a real calculator afterwards.')
	variables = input('How many variables will this involve? (min. 2): ')
	if variables == '2':
		var1 = input('Please type in your first	variable name: ')
		
