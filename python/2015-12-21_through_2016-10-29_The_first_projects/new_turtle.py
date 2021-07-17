from turtle import *
def turtle_controller(do, val):
	do = do.upper()
	if do == 'F':
		forward(val)
	elif do == 'B':
		backward(val)
	elif do == 'R':		
		right(val)
	elif do == 'L':
		left(val)
	elif do == 'D':
		pendown()
	elif do == 'U':
		penup()
	elif do == 'N':
		reset()
	else:
		print ('Unrecognizable pattern; please try again.')
def string_artist(program):
	cmd_list = program.split('-')
	for command in cmd_list:						
		cmd_len = len(command)
		if cmd_len == 0:
			continue
		cmd_type = command[0]
		num = 0
		if cmd_len > 1:
			num_string = command[1:]
			num = int(num_string)
		print (command, ':', cmd_type, num)
		turtle_controller(cmd_type, num)
instructions = '''Enter a program for the turtle to follow:
eg F100-R45-U-F100-L45-D-F100-R90-B50
N = New Drawing
U/D = Pen Up/Down
F100 = Move Forward 100
B50	= Move Backwards 50
R90 = Turn Right 90 Degrees
L45 = Turn Left 45 Degrees
It is better to draw on paper first'''
screen = getscreen()
while True:
	t_program = screen.textinput('Drawing Machine', instructions)
	print(t_program)
	if t_program == None or t_program.upper() == 'END':
		break
	string_artist(t_program)
	
