import time

print(time.time())
starting_text = '''Python 2.7.9 (default, ''' + Time + ''') 
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.'''
print (starting_text)
while True:
	action = raw_input('>>> ')
	troll_text = 'Traceback (most recent call last): \
										   File "<Ssundee.py>", line 1, in <module> \
				        NameError: name \'' + action + '\' is not defined'
	if action == '^C':
		print ('KeyboardInterrupt')
		break
	else:	
		print (troll_text)				
	
