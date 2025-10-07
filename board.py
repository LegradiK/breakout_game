from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.shape('square')
        self.color('blue')
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.goto(position)

    def right(self):
        new_x = self.xcor() + 20
        if new_x > 400:
            new_x = 400
        self.goto(new_x, self.ycor())

    def left(self):
        new_x = self.xcor - 20
        if new_x < -400:
            new_x = -250
        self.goto(new_x, self.ycor())