m = input("Type in slope: ")
b = input("Type in y-intercept: ")
exponent = input("Type in exponent: ")

m = float(m)
b = float(b) * 10

import turtle
turtle.speed(10)
turtle.penup()
turtle.setpos(-100, 100)
turtle.pendown()
for i in range(1, 5):
    turtle.forward(200)
    turtle.right(90)
    
turtle.penup()
for i in range(1, 10):
    turtle.forward(10)
    turtle.right(90)
    turtle.pendown()
    turtle.forward(200)
    turtle.right(180)
    turtle.penup()
    turtle.forward(200)
    turtle.right(90)

turtle.pencolor("red")
turtle.forward(10)
turtle.right(90)
turtle.pendown()
turtle.forward(200)
turtle.right(180)
turtle.penup()
turtle.forward(200)
turtle.right(90)

turtle.pencolor("black")
for i in range(1, 10):
    turtle.forward(10)
    turtle.right(90)
    turtle.pendown()
    turtle.forward(200)
    turtle.right(180)
    turtle.penup()
    turtle.forward(200)
    turtle.right(90)

turtle.penup()
turtle.setpos(-100, -100)
for i in range(1, 10):
    turtle.seth(90)
    turtle.forward(10)
    turtle.right(90)
    turtle.pendown()
    turtle.forward(200)
    turtle.right(180)
    turtle.penup()
    turtle.forward(200)

turtle.pencolor("red")
turtle.seth(90)
turtle.forward(10)
turtle.right(90)
turtle.pendown()
turtle.forward(200)
turtle.right(180)
turtle.penup()
turtle.forward(200)

turtle.pencolor("black")
for i in range(1, 10):
    turtle.seth(90)
    turtle.degrees(360)
    turtle.forward(10)
    turtle.right(90)
    turtle.pendown()
    turtle.forward(200)
    turtle.right(180)
    turtle.penup()
    turtle.forward(200)
    
turtle.penup()
turtle.setpos(-100, 0)
turtle.right(180)
turtle.penup()
turtle.pencolor("green")

while (m * ((turtle.xcor() / 10 ) ** int(exponent)) + b) >= 99:
	print((m * ((turtle.xcor() / 10 ) ** int(exponent)) + b))
	turtle.forward(10)
print((m * ((turtle.xcor() / 10 ) ** int(exponent)) + b))
target = ((turtle.xcor()+1 / 10 ) ** int(exponent)) + b
turtle.setpos(turtle.xcor(), (m * ((turtle.xcor() / 10 ) ** int(exponent)) + b))
while turtle.xcor() <= 100 and turtle.ycor() <= 100:
	target = ((turtle.xcor()+10 / 10 ) ** int(exponent)) + b
	turtle.setheading(turtle.towards(turtle.xcor()+10, target))
	turtle.forward(1)
