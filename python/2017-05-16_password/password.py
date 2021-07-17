password_finished = 0
BBH = 0
game_in_play = 0
disclaimer = 1
while disclaimer == 1:
	print('Please make sure that this is running on Python3 or else it won\'t work. You can do so by holding the "ctrl" button and hitting the "c" button, then open a terminal window and do "python3 password.py".')
	disclaimer_read = input('Do you understand? y/n: ')
	if disclaimer_read == 'y':
		disclaimer = 0
	elif disclaimer_read == 'n':
		continue
	else:
		print('Please type in either y or n!')
		continue	
from time import sleep
print('HALT!')
sleep(1)
print('To get in, you need to say the password!')
sleep(1)
failed_attempts = 0
while failed_attempts < 3:
	game_in_play = 1
	krabby_password = input('What was the one thing needed to make a Krabby Patty? ')
	if krabby_password == 'wuzzawuzza':
		failed_attempts = 3
		password_finished = 1
	elif krabby_password != 'the secret formuler' and krabby_password != 'wuzzawuzza':
		print('Nope!')
		sleep(1)
		failed_attempts = failed_attempts + 1
		continue
	elif krabby_password == 'the secret formuler':
		dragon_password = input('In my fan-fiction "DragonCraft", what was the name of the first earth dragon? ')
		if dragon_password != 'Brick':
			print('Try Again!')
			sleep(1)
			failed_attempts = failed_attempts + 1
			continue
		elif dragon_password == 'Brick':
			password_finished = 1
			failed_attempts = 3
if password_finished == 1:
	failed_attempts = 0
	game_in_play = 0 			
elif failed_attempts == 3:
	print('Sorry, but you\'ve failed the maximum amount of times!')
	sleep(2)
	print('And now you won\'t be able to do anything!')
	game_in_play = 0
	while True:
		game_in_play = 1
print ('Welcome to the arcade!')
sleep(1)
def start_game():
	game_in_play = 1
def end_game():
	game_in_play = 0 	
while game_in_play == 0:
	game = input('What do you want to play? (Bubble Blaster, Number Guess, Lottery, Maze or Calculator.) Type in "Goodbye!" to leave. ')
	if str(game) == 'Maze':
		game_in_play = 1
		# Ghost Game
		from random import randint
		from time import sleep
		feeling_brave = True
		score = 0
		while feeling_brave:			
			guess = input('Do you want to stop? yes/no: ')
			if guess == 'yes':
				break
			ghost_door = randint(1, 3)
			print ('Three doors lie ahead...')
			sleep(1)
			print ('A ghost lies behind one.')
			sleep(1)
			print ('Which door do you open?')
			sleep(1)
			door = input('1, 2 or 3? ')
			door_num = int(door)
			if int(door) not in range(1, 4):
				break
			if door_num == ghost_door:
				sleep(1)
				print ('GHOST!')
				feeling_brave = False
				sleep(1)
			else:
				sleep(1)
				print ('No ghost!')
				sleep(1)
				print ('You go to the next room.')
				sleep(1)
				score = score + 1
				print ('Your score is now ' + str(score) + '.')
				sleep(1)
		print ('YOU DIED!')
		sleep(1)
		print ('Game over! Your score was ' + str(score) + '.')
		sleep(1)
		game_in_play = 0
	if str(game) == 'Bubble Blaster':
		print('After the game is over, you need to delete the window with the game. The program will continue to run.')
		sleep(5)
		game_in_play = 1
		from tkinter import *
		HEIGHT = 500
		WIDTH = 800
		window = Tk()
		window.title('Bubble Blaster')
		c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
		c.pack()
		ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
		ship_id2 = c.create_oval(0, 0, 30, 30, outline='red')
		SHIP_R = 15
		MID_X = WIDTH / 2		
		MID_Y = HEIGHT / 2
		c.move(ship_id, MID_X, MID_Y)
		c.move(ship_id2, MID_X, MID_Y)
		SHIP_SPD = 10
		def move_ship(event):
			if event.keysym == 'Up':
				c.move(ship_id, 0, -SHIP_SPD)
				c.move(ship_id2, 0, -SHIP_SPD)
			elif event.keysym == 'Down':
				c.move(ship_id, 0, SHIP_SPD)
				c.move(ship_id2, 0, SHIP_SPD)
			elif event.keysym == 'Left':
				c.move(ship_id, -SHIP_SPD, 0)
				c.move(ship_id2, -SHIP_SPD, 0)
			elif event.keysym == 'Right':
				c.move(ship_id, SHIP_SPD, 0)
				c.move(ship_id2, SHIP_SPD, 0)
		c.bind_all('<Key>', move_ship)	
		from random import randint
		bub_id = list()
		bub_r = list()
		bub_speed = list()
		MIN_BUB_R = 10
		MAX_BUB_R = 30
		MAX_BUB_SPEED = 10
		GAP = 100
		def create_bubble():
			x = WIDTH + GAP
			y = randint(0, HEIGHT)
			r = randint(MIN_BUB_R, MAX_BUB_R)
			id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
			bub_id.append(id1)
			bub_r.append(r)
			bub_speed.append(randint(1, MAX_BUB_SPEED))
		def move_bubbles():
			for i in range(len(bub_id)):
				c.move(bub_id[i], -bub_speed[i], 0)
		def get_coords(id_num):
			pos = c.coords(id_num)
			x = (pos[0] + pos[2])/2
			y = (pos[1] + pos[3])/2
			return x, y
		def del_bubble(i):
			del bub_r[i]
			del bub_speed[i]
			c.delete(bub_id[i])
			del bub_id[i]
		def clean_up_bubs():
			for i in range(len(bub_id)-1, -1, -1):
				x, y = get_coords(bub_id[i])
				if x < -GAP:
					del_bubble(i)
		from math import sqrt
		def distance(id1, id2):
			x1, y1 = get_coords(id1)
			x2, y2 = get_coords(id2)
			return sqrt((x2 - x1)**2 + (y2 - y1)**2)
		def collision():
			points = 0
			for bub in range(len(bub_id)-1, -1, -1):
				if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
					points += (bub_r[bub] +bub_speed[bub])
					del_bubble(bub)
			return points
		c.create_text(50, 30, text='TIME', fill='white')
		c.create_text(150, 30, text='SCORE', fill='white')
		time_text = c.create_text(50, 50, fill='white')
		score_text = c.create_text(150, 50, fill='white')
		def show_score(score):
			c.itemconfig(score_text, text=str(score))
		def show_time(time_left):
			c.itemconfig(time_text, text=str(time_left))									
		from time import sleep, time
		BUB_CHANCE = 10
		TIME_LIMIT = 30
		BONUS_SCORE = 1000
		score = 0
		bonus = 0
		end = time() + TIME_LIMIT
		#MAIN GAME LOOP
		while time() < end:
			if randint(1, BUB_CHANCE) == 1:
				create_bubble()
			move_bubbles()
			clean_up_bubs()
			score += collision()
			if (int(score / BONUS_SCORE)) > bonus:
				bonus += 1
				end += TIME_LIMIT
			show_score(score)
			show_time(int(end - time()))	
			window.update()
			sleep(0.01)
		c.create_text(MID_X, MID_Y, 
			text='GAME OVER!', fill='white', font=('Helvetica',30))
		c.create_text(MID_X, MID_Y + 30, 
			text='Score: '+ str(score), fill='white')
		c.create_text(MID_X, MID_Y + 45, 
			text='Bonus time: '+ str(bonus*TIME_LIMIT), fill='white')
	if str(game) == 'Number Guess':
		game_in_play = 1
		number = input("Pick a number from 1 through 10!")
		while int(number) not in range(1, 10):
			number = input("No, no, pick a number from 1 through 10!")
		idk_5 = input("Is your number 5? yes or no.") 
		if idk_5 == "yes":
			print ("Your number is 5!")	
			end_game()		
		if idk_5 == "no":	 	
			h_or_l_5 = input("Is your number higher than 5? yes or no.")
			if h_or_l_5 == "yes":
				h_l_7 = input("Is your number higher than 7? yes or no.")
				if h_l_7 == "no":
					is_6_7 = input("Is your number 6? yes or no.")
					if is_6_7 == "yes":
						print ("Your number is 6!")
						end_game()
					if is_6_7 == "no":
						print ("Your number is 7!")
						end_game()
				if h_l_7 == "yes":
					num_8_or_9 = input("Is your number 8? yes or no.")
					if num_8_or_9 == "yes":
						print ("Your number is 8!")
						end_game()
					if num_8_or_9 == "no":
						print ("Your number is 9!")	
						end_game()
			if h_or_l_5 == "no":
				h_l_3 = input("Is your number greater than 3? yes or no.")
				if h_l_3 == "yes":
					print ("Your number is 4!")
					end_game()
				if h_l_3 == "no":
					num_1_or_2_or_3 = input ("Is your number 1? yes or no.")
					if num_1_or_2_or_3 == "yes":
						print ("Your number is 1!")
						end_game()
					if num_1_or_2_or_3 == "no":
						num_2_or_3 = input("Is your number 2? yes or no.")
						if num_2_or_3 == "yes":
							print ("Your number is 2!")
							end_game()
						if num_2_or_3 == "no":
							print ("Your number is 3!")	
							end_game() 				
	if str(game) == 'Lottery':
		from time import sleep
		import random 
		print ("Welcome to Jack Potts Lottery!")
		sleep(1.5)
		print ("Behind 1 virtual door is the chance to say, 'I survived Jack Potts Lottery!' to your friends!")
		sleep(2)	
		print ("Behind the other is the dreaded island of 'Happyland!'")
		sleep(2)
		player_answer = input("So, what will it be? 1 or 2? ")
		real_answer = random.randint(1, 2) 
		while int(player_answer) not in range(1, 3):
			player_answer = input("No, no, you have to pick, 1 or 2? ")
		print ("Importing pick...")
		sleep(5)
		print ("Decoding pick...")
		sleep(6)
		print ("Recalling algorithms...")
		sleep(4)
		print ("Calculating probability algorithms...")
		sleep(7)
		print ("Solving probability algorithms...")
		sleep(6)
		print ("Double-checking answer...")
		sleep(4)
		print ("Downloading rewards...")
		sleep(4)
		print ("Exporting answer...")
		sleep(3)
		if player_answer != str(real_answer):     
			print ("Your picked door was: " + int(player_answer))
			sleep(1)
			print ("The computer-generated pick was: " + str(real_answer))
			sleep(1)
			print ("Oops, better luck next time! But you win a world full of beautiful flowers and frogs and trolls and all the things you would find in Happyland!")
		if player_answer == str(real_answer):
			print ("Your picked door was: " + player_answer)
			sleep(1)
			print ("The computer-generated pick was: " + str(real_answer))
			sleep(1)
			print ("Aww, I hate it when I lose! You can go and say you survived my lottery!")
			end_game()
	if str(game) == 'Calculator':
		start_game()
		num1 = input('Please type in your first number: ')
		operator = input('Please type in your operator (+, -, *, /): ')
		num2 = input('Please type in your second number: ')
		if str(operator) == '+':
			final_answer = int(num1) + int(num2)
		elif str(operator) == '-':
			final_answer = int(num1) - int(num2)
		elif str(operator) == '*':
			final_answer = int(num1) * int(num2)
		elif str(operator) == '/':
			final_answer = int(num1) / int(num2)
		else:
			final_answer = 'Unrecognizable Operator'
		print (str(num1) + ' ' + str(operator) + ' ' + str(num2) + ' = ' + str(final_answer))
		sleep(2)
		end_game()
	if str(game) == '4 Algorithm':
		start_game()
		from time import sleep
		print('Please type in a number in word form between 1 and 100 (no space, no hyphen): ')
		algorized_num = input()
		#algorized_num = number
		#print algorized_num
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
			return a
		while algorized_num != 'four':	
			algorized_num2 = find_length(algorized_num)
			print (algorized_num, '=', algorized_num2)
			sleep(1)
			algorized_num = algorized_num2 
		print ('And four = four!')
		end_game()
		sleep(1)
	if str(game) == 'Math Flash':
		start_game()
		tutorial = 'y'
		while tutorial == 'y':
			tutorial = input('Do you want to read the tutorial? y/n: ')
			if tutorial == 'y':
				print ('Hi. Welcome to Math Flash.')
				sleep(1)
				print ('This is a program that is supposed to help with your math skills.') 
				sleep(2)
				print ('It will ask you what you want the operator, number to (fill in operator here) and the biggest number you want to "operate" with.')
				sleep(4)
				print ('Essentialy, it\'s really a table maker.')
				sleep(1)
				print ('When it asks you a question, there are 3 ways to answer it:')
				sleep(2)
				print ('A: You can answer it directly.')
				sleep(1)
				print ('It will ask the question, and say whether or not the answer is correct and give the real answer.')
				sleep(3)
				print ('B: You can type in \'skip\' which skips the current question.')
				sleep(1)
				print ('C: You can type in \'break\' which restarts the table and asks for a new one. ') 
				sleep(3)
				print ('Or you can hit the ctrl or comm button, then hit c if you want to exit the program completely.')
				sleep(3)
				print ('Now let\'s do some math!')
				sleep(1)
				continue
			else:	
				skips = 0
				math_flash_points = 0
				from time import sleep
				operator = input('Please type in the operator (type in: add, subtract, multiply or divide): ')		
				table = input('Please type in the number you want to ' + str(operator) + ' with: ')
				range_of_table = input('Please type in the bigest number you want to ' + str(operator) + ' ' + str(table) + ' ' + 'by: ')
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
					print ('What\'s', int(table), str(table_operator2), int(i), '?')
					guess = input()
					if str(guess) == 'stop':
						break
					if str(guess) == 'skip':
						if int(skips) < 3:
							skips = skips + 1	
							print ('Skipping...')
							sleep(1)
							continue	
						else:
							print ('Sorry, but you\'ve used the maximum amount of skips.')	
					ans = eval(str(i)+table_operator+str(table))
					if int(guess) == int(ans):
						print ('Yes! You\'re correct!')
						sleep(1)
						math_flash_points = math_flash_points + 1
						print('Your score is now ' + str(math_flash_points) + '.')
						sleep(1)
					elif str(guess) != int(ans):
						print ('No, it\'s ' + str(ans) + '.')
						sleep(1)
				end_game()
	if str(game) == 'Turtle':
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
		Type END to end the program
		It is better to draw on paper first'''
		screen = getscreen()
		while True:
			t_program = screen.textinput('Drawing Machine', instructions)
			print(t_program)
			if t_program == None or t_program.upper() == 'END':
				break
			string_artist(t_program)
	if str(game) == 'Age Guess':
		print ('I can guess your age!')
		sleep(1)
		birth_year = input('Please type in your birth year: ')
		present_year = input('Type in the year it is now: ')
		birth_month = input('Type in your birth month in number form (Jan. = 1, Feb. = 2, etc.): ')
		present_month = input('Type in the number month it is of the year ' + str(present_year) + ': ')
		if present_month == '1':
			suffix = 'st'
		elif present_month == '2':
			suffix = 'nd'
		elif present_month == '3':
			suffix = 'rd'		 
		elif present_month <= '4':
			suffix = 'th'	
		present_day = input('Type in the number day it is of the ' + str(present_month) + str(suffix) + ' month: ')
		birth_day = input('Please type in your birth day (1, 2, 3, etc.): ')
		if int(present_month) > int(birth_month):
			present_year = int(present_year) + 1
		elif int(present_month) == int(birth_month):
			if int(present_day) < int(birth_day):
				present_year = int(present_year) - 1
		elif int(present_month) < int(birth_month):
			present_year = int(present_year) - 1				 
		age = int(present_year) - int(birth_year) 
		print ('Your age is ' + str(age) + '! Did I get it correct?')	
	if str(game) == 'Highscore':
		game_highscore = 'Bubble Blaster: ' + BBH						
	if str(game) == 'Goodbye!':
		print('Goodbye!')
		sleep(2)
		break
