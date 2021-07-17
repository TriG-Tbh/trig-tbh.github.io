while True:
	x = ""
	current_string = ""
	while x != "end" and x != "endall":
		x = raw_input("The current string is " + current_string + ". Please type in the next character (\"end\" to calculate, \"endall\" to end): ")
		if x == type(int):
			x = float(x)
		if x == "+":
			current_string = current_string + "+"
		elif x == "-":
			current_string = current_string + "-"
		elif x == "*":
			current_string = current_string + "*"
		elif x == "/":
			current_string = current_string + "/"
		elif x == "^":
			current_string = current_string + "**"
		elif x == "(":
			current_string = current_string + "("
		elif x == ")":
			current_string = current_string + ")"
		elif x == "end":
			pass
		elif x != "_" and x != "&" and x != "@":
			x = str(x)
			current_string = current_string + x
	if x == "endall":
		break
		current_string = current_string + x
		parentheses = parentheses - 1
	current_string = str(current_string)
	result = float(eval(current_string))
	print("The answer is " + str(result))
