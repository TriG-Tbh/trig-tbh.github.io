import t_savefile
from time import sleep

t = t_savefile

def open_shop():
	while True:
		import t_savefile
		shop_request = raw_input("What would you like to buy:\n"
		"1) Food \n"
		"2) Water \n"
		"3) Cleaning supplies \n"
		"Please select an option (1-3), or \"leave\" to exit: ")
		if (len(shop_request)) == 1:
			shop_request = int(shop_request)
		if shop_request == "leave":
			break
		else:
			if shop_request == 1:
				confirm_purchase = raw_input("(Y/N) You currently have " + str(t.food) + " food. Would you like to buy 15 food for 10 T-Bucks? ")
				confirm_purchase.lower()
				if t.t_bucks > 9:
					if confirm_purchase == "y":
						save = open("t_savefile.py", "a")
						save.write("t_bucks = t_bucks - 15\n")
						save.write("food = food + 15\n")
						t.food = t.food + 15
						save.close()
						print("Transaction completed.")
						sleep(1)
				else:
					print("You do not have enough T-Bucks!")
					sleep(1)
			elif shop_request == 2:
				confirm_purchase = raw_input("(Y/N) You currently have " + str(t.water) + " water. Would you like to buy 15 water for 5 T-Bucks? ")
				confirm_purchase.lower()
				if t.t_bucks > 4:
					if confirm_purchase == "y":
						save = open("t_savefile.py", "a")
						save.write("t_bucks = t_bucks - 5\n")
						save.write("water = water + 15\n")
						t.water = t.water + 15
						save.close()
						print("Transaction completed.")
						sleep(1)
				else:
					print("You do not have enough T-Bucks!")
					sleep(1)
			elif shop_request == 3:
				confirm_purchase = raw_input("(Y/N) You currently have " + str(t.cleaning_supplies) + " cleaning_supplies. Would you like to buy 15 cleaning supplies for 15 T-Bucks? ")
				confirm_purchase.lower()
				if t.t_bucks > 14:
					if confirm_purchase == "y":
						save = open("t_savefile.py", "a")
						save.write("t_bucks = t_bucks - 15\n")
						save.write("cleaning_supplies = cleaning_supplies + 15\n")
						t.cleaning_supplies = t.cleaning_supplies + 15
						save.close()
						print("Transaction completed.")
						sleep(1)
				else:
					print("You do not have enough T-Bucks!")
					sleep(1)
