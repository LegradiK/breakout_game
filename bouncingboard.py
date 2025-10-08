from turtle import RawTurtle

class BouncingBoard(RawTurtle):
    def __init__(self, screen, position, game_screen_w):
        super().__init__(screen)
        self.penup()
        self.shape('square')
        self.color('#d3d3d3')
        self.shapesize(stretch_wid=1, stretch_len=15)
        self.goto(position)
        self.half_screen_size = game_screen_w // 2

    def right(self):
        new_x = self.xcor() + 20
        if new_x > self.half_screen_size - 150:
            new_x = self.half_screen_size - 150
        self.goto(new_x, self.ycor())

    def left(self):
        new_x = self.xcor() - 20
        if new_x < - (self.half_screen_size) + 150:
            new_x = - (self.half_screen_size) + 150
        self.goto(new_x, self.ycor())