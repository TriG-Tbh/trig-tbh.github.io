import os
while True:
	os.system('clear')
	action = raw_input("Commands: \n"
	"\"insert\": manually insert cells \n"
	"\"load\": load a premade grid \n"
	"\"start\": start the simulation \n"
	"\"stop\" (can be used at any time): stop the simulation \n"
	">")
	if action == "start":
		import read_screen
	if action == "insert":
		import manual_insert
		manual_insert.insert()
		
