print ('Welcome to the arcade!')
while True:
	game = raw_input('What do you want to play? (Bubble Blaster, Number Guess, Lottery or Maze, updates soon!) ')
	if str(game) == 'Maze':
		# Ghost Game
		from random import randint
		from time import sleep
		sleep(1)
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
			door = input('1, 2 or 3?')
			door_num = int(door)
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
				print ('Your score is now ' + str(score))
				sleep(1)
		print ('YOU DIED!')
		sleep(1)
		print ('Game over! Your score was ' + str(score))
		sleep(1)
	if str(game) == 'Bubble Blaster':
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
		def key_stuff(event):
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
			elif event.keysym == 'Space':
				break_all	
		c.bind_all('<Key>', key_stuff)	
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
		c.create_text(400, 10, text='Press the spacebar to stop.', fill='white')
		time_text = c.create_text(50, 50, fill='white')
		score_text = c.create_text(150, 50, fill='white')
		stop_text = c.create_text(400, 30, fill='white')
		def show_score(score):
			c.itemconfig(score_text, text=str(score))
		def show_time(time_left):
			c.itemconfig(time_text, text=str(time_left))
		def show_stop(stop):
			c.itemconfig(stop, text = str(stop))									
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
		number = input("Pick a number from 1 through 10!")
		while int(number) not in range(1, 10):
			number = input("No, no, pick a number from 1 through 10!")
		idk_5 = input("Is your number 5? yes or no.") 
		if idk_5 == "yes":
			print ("Your number is 5!")			
		if idk_5 == "no":	 	
			h_or_l_5 = input("Is your number higher than 5? yes or no.")
			if h_or_l_5 == "yes":
				h_l_7 = input("Is your number higher than 7? yes or no.")
				if h_l_7 == "no":
					is_6_7 = input("Is your number 6? yes or no.")
					if is_6_7 == "yes":
						print ("Your number is 6!")
					if is_6_7 == "no":
						print ("Your number is 7!")	 	
				if h_l_7 == "yes":
					num_8_or_9 = input("Is your number 8? yes or no.")
					if num_8_or_9 == "yes":
						print ("Your number is 8!")
					if num_8_or_9 == "no":
						print ("Your number is 9!")	
			if h_or_l_5 == "no":
				h_l_3 = input("Is your number greater than 3? yes or no.")
				if h_l_3 == "yes":
					print ("Your number is 4!")
				if h_l_3 == "no":
					num_1_or_2_or_3 = input ("Is your number 1? yes or no.")
					if num_1_or_2_or_3 == "yes":
						print ("Your number is 1!")
					if num_1_or_2_or_3 == "no":
						num_2_or_3 = input("Is your number 2? yes or no.")
						if num_2_or_3 == "yes":
							print ("Your number is 2!")
						if num_2_or_3 == "no":
							print ("Your number is 3!")		 				
	if str(game) =='Lottery':
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
			print ("Your picked door was: " + player_answer)
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

