import sys
from time import sleep

function = raw_input("Type in a function (\"linear\" or \"quadratic\"): ")

if function == "linear":
    m = raw_input("Type in slope: ")
    b = raw_input("Type in y-intercept: ")

    m = eval(m)
    b = eval(b)

    m = float(m)
    b = float(b) * 10
elif function == "quadratic":
    exponent = raw_input("What is the exponent of x? ")
    m = raw_input("Type in slope: ")
    b = raw_input("Type in y-intercept: ")

    m = eval(m)
    b = eval(b)
    exponent = eval(exponent)
    
    exponent = int(exponent)
    m = float(m) * 1 
    b = float(b) * 10
else:
    sys.exit("Please type in a recognized function!")

import turtle
turtle.speed(100)
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

turtle.setpos(-101, 0)
turtle.right(180)
turtle.penup()
correct_position = True
turtle.pencolor("green")
turtle.hideturtle()
if function == "linear":
    while turtle.xcor() <= 100 and turtle.ycor() <= 100:
        if turtle.xcor() < -100 or turtle.ycor() < -100:
            turtle.penup()
            turtle.forward(1)
            turtle.sety(m*turtle.xcor() + b)
        else:
            turtle.pendown()
            turtle.forward(0.5)
            turtle.goto(turtle.xcor(), m*turtle.xcor() + b)
else:
    turtle.setpos(-100, 0)
    while correct_position:
        #print((m * ((turtle.xcor() / 10 ) ** int(exponent)) + b), turtle.xcor())
        
        if ((m * ((turtle.xcor() ** int(exponent)) / 10) + b)) > 100:
            turtle.setheading(turtle.towards(0, 0))
            turtle.forward(0.5)
        else:
            correct_position = False
turtle.speed("fastest")
if function == "quadratic":
    turtle.goto(turtle.xcor(), (m * ((turtle.xcor() ** int(exponent)) / 10) + b))
    turtle.pendown()
    turtle.setpos(turtle.xcor(), (m * ((turtle.xcor() ** int(exponent)) / 10) + b))
    while turtle.xcor() <= 100 and turtle.ycor() <= 100 and turtle.xcor() >= -100 and turtle.ycor() >= -100:
        turtle.forward(0.1)
        target = (m * ((turtle.xcor() ** int(exponent)) / 10) + b)
        '''turtle.setheading(turtle.towards(turtle.xcor(), target))
        turtle.forward(1)'''
        turtle.goto(turtle.xcor(), target)
turtle.hideturtle()
sleep(15)
