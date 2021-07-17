print("I'm going to guess a number between 1 and 10!")
number = input("Pick a number from 1 through 10! ")
while int(number) not in range(1, 10):
	number = input("No, no, pick a number from 1 through 10!")
idk_5 = input("Is your number 5? yes or no. ") 
if idk_5 == "yes":
	print ("Your number is 5!")			
if idk_5 == "no":	 	
	h_or_l_5 = input("Is your number higher than 5? yes or no. ")
	if h_or_l_5 == "yes":
		h_l_7 = input("Is your number higher than 7? yes or no. ")
		if h_l_7 == "no":
			is_6_7 = input("Is your number 6? yes or no. ")
			if is_6_7 == "yes":
				print ("Your number is 6!")
			if is_6_7 == "no":
				print ("Your number is 7!")	 	
		if h_l_7 == "yes":
			num_8_or_9 = input("Is your number 8? yes or no. ")
			if num_8_or_9 == "yes":
				print ("Your number is 8!")
			if num_8_or_9 == "no":
				print ("Your number is 9!")	
	if h_or_l_5 == "no":
		h_l_3 = input("Is your number greater than 3? yes or no. ")
		if h_l_3 == "yes":
			print ("Your number is 4! ")
		if h_l_3 == "no":
			num_1_or_2_or_3 = input ("Is your number 1? yes or no. ")
			if num_1_or_2_or_3 == "yes":
				print ("Your number is 1!")
			if num_1_or_2_or_3 == "no":
				num_2_or_3 = input("Is your number 2? yes or no. ")
				if num_2_or_3 == "yes":
					print ("Your number is 2!")
				if num_2_or_3 == "no":
					print ("Your number is 3!")		 				
