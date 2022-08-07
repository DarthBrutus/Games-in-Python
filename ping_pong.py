import turtle as t

#Screen
win = t.Screen()
win.title("Krishna")
win.bgcolor('blue')
win.setup(width=800, height=600)

#Left paddle
left_paddle = t.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color("#00FF00")
left_paddle.shapesize(stretch_wid=5, stretch_len=1)
left_paddle.penup()
left_paddle.goto(-350, 0)

#Right paddle
right_paddle = t.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color("#00FF00")
right_paddle.shapesize(stretch_wid=5, stretch_len=1)
right_paddle.penup()
right_paddle.goto(350, 0)

#Ball
ball = t.Turtle()
ball.speed(40)
ball.shape("circle")
ball.shapesize(stretch_wid=2, stretch_len=2)
ball.color('yellow')
ball.penup()
ball.goto(0, 0)
ball.dx = 7
ball.dy = -7

# Displays the score
left_player = 0
right_player = 0
sketch = t.Turtle()
sketch.speed(0)
sketch.color("red")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left Player : 0  |  Right Player: 0", align="center", font=("Times New Roman", 25, "bold"))


# Functions to move paddle vertically
def paddleaup():
	y = left_paddle.ycor()
	y += 20
	left_paddle.sety(y)


def paddleadown():
	y = left_paddle.ycor()
	y -= 20
	left_paddle.sety(y)


def paddlebup():
	y = right_paddle.ycor()
	y += 20
	right_paddle.sety(y)


def paddlebdown():
	y = right_paddle.ycor()
	y -= 20
	right_paddle.sety(y)


# Keyboard bindings
win.listen()
win.onkeypress(paddleaup, "w")
win.onkeypress(paddleadown, "s")
win.onkeypress(paddlebup, "Up")
win.onkeypress(paddlebdown, "Down")


while True:
	win.update()

	ball.setx(ball.xcor()+ball.dx)
	ball.sety(ball.ycor()+ball.dy)

	if ball.ycor() > 290:
		ball.sety(290)
		ball.dy *= -1

	if ball.ycor() < -290:
		ball.sety(-290)
		ball.dy *= -1

	if ball.xcor() > 390:
		ball.goto(0, 0)
		ball.dy *= -1
		left_player += 1
		sketch.clear()
		sketch.write("Left Player : {}  |  Right Player: {}".format(left_player, right_player), align="center",font=("times New Roman", 25, "bold"))

	if ball.xcor() < -500:
		ball.goto(0, 0)
		ball.dy *= -1
		right_player += 1
		sketch.clear()
		sketch.write("Left Player : {}  |  Right Player: {}".format(left_player, right_player), align="center",font=("Times New Roman", 25, "bold"))

	# Paddle ball meeting
	if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < right_paddle.ycor()+50 and ball.ycor() > right_paddle.ycor()-50):
		ball.setx(340)
		ball.dx*=-1
		
	if (ball.xcor()<-340 and ball.xcor()>-350) and (ball.ycor()<left_paddle.ycor()+50 and ball.ycor()>left_paddle.ycor()-50):
		ball.setx(-340)
		ball.dx *=-1