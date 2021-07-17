from time import sleep
print ('Hi. Welcome to Math Flash 2.0!')
sleep(1)
print ('This is a program that is supposed to help with your math skills.')
sleep(2)
print ('It will pick a number out of a random of 1-100, a random operator and a second number also a random of 1-100.')
sleep(6)
print ('So, you have no idea what question is next.')
sleep(1)
print ('It will ask the question, and say whether or not the answer is correct and give the real answer.')
sleep(5)
print ('If the  real answer is lower than 0, type in skip and it will skip that question.') 
sleep(2)
print ('Now let\'s do some math!')
sleep(1)
from random import randint
while True:
	add = 1
	subtract = 2
	multiply = 3
	divide = 4
	question_operator = randint(int(add), int(divide)+1)
	if str(question_operator) == '1':
		real_question_operator = '+'
	elif str(question_operator) == '2':
		real_question_operator = '-'
	elif str(question_operator) == '3':
		real_question_operator = '*'
	elif str(question_operator) == '4':
		real_question_operator = '/'
	first_num = randint(1, 100)
	second_num = randint(1, 100)
	print 'What\'s ', int(first_num), real_question_operator, int(second_num), '?'
	real_answer = eval(str(first_num)+str(real_question_operator)+str(second_num))
	if str(real_answer) <= '0':
		print ('Oops, it\'s lower than zero! We\'re going to skip this one!')
		continue
	elif str(real_answer) == type(float):
		print ('Oops, it\'s a decimal! We\'re going to skip this one!')	
	answer_idk = input()
	if int(answer_idk) == int(real_answer):
		print ('Yes! You got that correct!')
	else:
		print ('No, it\'s ' + str(real_answer))	 				
