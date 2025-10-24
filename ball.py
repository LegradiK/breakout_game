from turtle import RawTurtle
import random

class Ball(RawTurtle):
    def __init__(self, screen):
        super().__init__(screen)
        self.shape('circle')
        self.color('white')
        self.penup()
        self.setposition(x=0, y=-300)
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.04

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, -250)
        self.x_move = random.choice([-10, 10])
        self.y_move = abs(self.y_move)

    def ball_speed_up(self):
        if self.move_speed > 0.02:
            self.move_speed -= 0.01
        else:
            self.move_speed = 0.02



