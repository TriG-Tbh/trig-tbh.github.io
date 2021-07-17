diviser_num = 1
div_nums = 0
prime = 1
num_i_q = raw_input('Type in a number to see if it is a prime or composite: ')
num_i_q = int(num_i_q)
for i in range(1, num_i_q):
	diviser_num = diviser_num + 1
	num_ans = int(int(num_i_q) % int(diviser_num))
	if int(num_ans) != 0:
		continue 
	elif num_ans == 0:
		div_nums = div_nums + 1
		if div_nums > 3 or div_nums == 3:
			print int(num_i_q), "is a composite number"
			prime = 0
		break
if prime == 1:
	print int(num_i_q), 'is a prime number.'
