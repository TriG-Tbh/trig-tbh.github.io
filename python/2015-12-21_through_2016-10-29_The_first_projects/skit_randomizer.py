from time import sleep
from random import randint
print('courtesy to Boy Scout Trail')
while True:
	sleep(1)
	scouts = input('Type in the number of scouts needed for skit (number): ')
	if int(scouts) < 2 or int(scouts) > 5:
		print('Sorry, try again.')
		continue
	else:
		if int(scouts) == 2:
			broken_finger = 1
			skit = randint(broken_finger, broken_finger)
			if skit == 1:
				broken_finger_skit = '''
Scout 1: Hey, (fill in scout's name), you're good with first aid. I need your help.
Scout 2: OK, what's the problem?
Scout 1: When I touch my forehead with my finger, it really hurts. When I push on my jaw, it's also painful. When I press on my stomach, I almost cry. What can it be?
(does each thing as he says them, always pushing with the tip of the same finger)
Scout 2 looks in his ears, listens to his heart, has him open his mouth, ...)
Scout 2: Man, I don't know. You'd better go see the doctor right away.
Scout 1: OK, I'll be right back.
(Scout 1 runs offstage and returns right back.)
Scout 2: So, what did the doctor say? What's wrong with you?
Scout 1: He says I have a broken finger.
Now copy this and paste this in a writer, and print it.'''
				print(broken_finger_skit)
				sleep(1)
