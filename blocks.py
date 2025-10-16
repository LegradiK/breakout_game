from turtle import RawTurtle
import random


COLOR_LIST = ['#FCC737', '#F26B0F', '#E73879', '#7E1891',
              '#E4004B', '#134686']

class Block(RawTurtle):
    def __init__(self, screen, x_cor, y_cor, color):
        super().__init__(screen)
        self.penup()
        self.shape('square')
        self.shapesize(stretch_wid=1.5, stretch_len=3)
        self.color(color)
        self.goto(x=x_cor,y=y_cor)

        # define borders of the brick
        self.left_wall = self.xcor() - 30
        self.right_wall = self.xcor() + 30
        self.upper_wall = self.ycor() + 15
        self.bottom_wall = self.ycor() - 15


class Blocks:
    def __init__(self, screen, game_screen_w):
        self.screen = screen
        self.y_start = 50
        self.y_end = 375
        self.blocks = []
        self.game_frame_wall_right = - game_screen_w // 2 + 30
        self.game_frame_wall_left = game_screen_w // 2 - 30
        self.create_all_lanes()

    def create_lane(self, y_cor):
        col_index = 0
        color_count = len(COLOR_LIST)

        for i in range(self.game_frame_wall_right, self.game_frame_wall_left, 63):
            # pick colour by column index cycling through COLOR_LIST
            color = COLOR_LIST[col_index % color_count]

            block = Block(self.screen, i, y_cor, color)
            self.blocks.append(block)

            col_index += 1

    def create_all_lanes(self):
        for i in range(self.y_start, self.y_end, 32):
            self.create_lane(i)
