print ('I wonder if it is your birthday!')
print ('Type in the following dates in this format: month/day (year will always make thetest fail).')
birthday = raw_input('Write in your birthday (check format above): ')
date = raw_input('Write in the date (check format above): ')
if str(birthday) != str(date):
	print ('Aww, you have to wait!')
if str(birthday) == str(date):
	print ('Happy birthday!')
	
