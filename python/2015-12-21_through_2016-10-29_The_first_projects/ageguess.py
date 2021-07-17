print ('I can guess your age!')
birth_year = input('Please type in your birth year: ')
present_year = input('Type in the year it is now: ')
birth_month = input('Type in your birth month in number form (Jan. = 1, Feb. = 2, etc.): ')
present_month = input('Type in the number month it is of the year ' + str(present_year) + ': ')
if present_month == '1':
	appendix = 'st'
elif present_month == '2':
	appendix = 'nd'
elif present_month == '3':
	appendix = 'rd'		 
birth_day = input('Please type in your birth day (1, 2, 3, etc.): ')
present_day = input('Type in the number day it is of the ' + str(present_month) + str(appendix) + ' month: ')
if int(present_month) > int(birth_month):
	present_year = int(present_year) + 1
elif 	int(present_month) == int(birth_month):
	if int(present_day) < int(birth_day):
		present_year = int(present_year) - 1
elif int(present_month) < int(birth_month):
	present_year = int(present_year) - 1				 
age = int(present_year) - int(birth_year) 
print ('Your age is ' + str(age) + '! Did I get it correct?')
