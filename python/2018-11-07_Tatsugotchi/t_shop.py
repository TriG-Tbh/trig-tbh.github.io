import t_savefile
from time import sleep

t = t_savefile

def open_shop():
	while True:
		import t_savefile
		shop_request = input("What would you like to buy:\n"
		"1) Food \n"
		"2) Water \n"
		"3) Cleaning supplies \n"
		"Please select an option (1-3), or \"exit\" to exit: ")
		if shop_request == "exit":
			break
		else:
			if option == 1:
				confirm_purchase = input("(Y/N) Would you like to buy 15 food for 10 T-Bucks? ")
				confirm_purchase.lower()
				if t.t_bucks > 9:
					save = open("t_savefile.py", "a")
					save.write("t_bucks = t_bucks - 15")
					save.write("food = food + 15")
					t.food = t.food + 15
					if t.food > 100:
						save.write("food = 100")
						t.food = 100
					save.close()
				else:
					print("You do not have enough T-Bucks!")
					sleep(1)
			elif option == 2:
				confirm_purchase = input("(Y/N) Would you like to buy 15 water for 5 T-Bucks? ")
				confirm_purchase.lower()
				if t.t_bucks > 4:
					save = open("t_savefile.py", "a")
					save.write("t_bucks = t_bucks - 5")
					save.write("water = water + 15")
					t.water = t.water + 15
					if t.water > 100:
						save.write("water = 100")
						t.water = 100
					save.close()
				else:
					print("You do not have enough T-Bucks!")
					sleep(1)
			elif option == 3:
				confirm_purchase = input("(Y/N) Would you like to buy 15 cleaning supplies for 15 T-Bucks? ")
				confirm_purchase.lower()
				if t.t_bucks > 14:
					save = open("t_savefile.py", "a")
					save.write("t_bucks = t_bucks - 15")
					save.write("cleaning_supplies = cleaning_supplies + 15")
					t.cleaning_supplies = t.cleaning_supplies + 15
					if t.cleaning_supplies > 100:
						save.write("cleaning_supplies = 100")
						t.cleaning_supplies = 100
					save.close()
				else:
					print("You do not have enough T-Bucks!")
					sleep(1)
