game = 1
if game == 1:
	# Ghost Game
	from random import randint
	from time import sleep
	feeling_brave = True
	score = 0
	while feeling_brave:
		ghost_door = randint(1, 3)
		print ('Three doors lie ahead...')
		sleep(1)
		print ('A ghost lies behind one.')
		sleep(1)
		print ('Which door do you open? ')
		sleep(1)
		door = input('1, 2 or 3? ')
		door_num = int(door)
		if door_num == ghost_door:
			print ('GHOST!')
			feeling_brave = False
			sleep(1)
		else:
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
	game == 0
