import time
import os
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk  # Pillow library (pip install pillow)
from bouncingboard import BouncingBoard
from ball import Ball
from blocks import Blocks, Block
from tkinter import font

SCREEN_W = 1390
SCREEN_H = 980
GAME_SCREEN_W = 1390
GAME_SCREEN_H = 850
BOARD_LOCATION = -(GAME_SCREEN_H // 2) + 80

class BreakOutApp:
    def __init__(self):
        self.running = True
        self.root = tk.Tk()
        self.root.title('BreakOut Game')
        # fix root size
        self.root.geometry(f'{SCREEN_W}x{SCREEN_H}')
        self.root.resizable(False, False)
        # set color
        self.root.configure(bg='black')
        # attach on_closing to window manager close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.set_up_logo_frame()
        self.set_up_game_frame()
        self.set_up_game_canvas()

        # bind keys to root (Tkinter)
        self.root.bind("<Right>", lambda e: (self.bouncing_board.right(), self.screen.update()))
        self.root.bind("<Left>", lambda e: (self.bouncing_board.left(), self.screen.update()))


    def set_up_logo_frame(self):
        # Top frame for game logo and title
        robo_img = Image.open("robot.png").resize((64, 64))
        self.photo = ImageTk.PhotoImage(robo_img)
        # Frame to hold everything
        self.logo_frame = tk.Frame(self.root, bg="black")
        self.logo_frame.pack(pady=30)
        # left logo
        self.left_label = tk.Label(self.logo_frame, image=self.photo, bg="black")
        self.left_label.grid(row=0, column=0, padx=30, pady=30)
        # set a logo
        self.game_logo = tk.Label(
            self.logo_frame,
            text='BreakOut Game',
            font=('Press Start 2P', 54),
            fg='yellow',
            bg='black',
            anchor='center'
        )
        self.game_logo.grid(row=0, column=1, padx=30, pady=30)
        # right logo
        self.right_label = tk.Label(self.logo_frame, image=self.photo, bg="black")
        self.right_label.grid(row=0, column=2, padx=30, pady=30)

    def set_up_game_frame(self):
        # main frame for playing a game
        # Frame to hold the game area
        self.game_frame = tk.Frame(self.root, bg="black")
        self.game_frame.pack(pady=10)
        # Create PLAY button (place it in the centre of the game_frame)
        self.play_button = tk.Button(
            master=self.game_frame,
            text='PLAY',
            font=('Press Start 2P', 32),
            width=8,
            height=5,
            fg='black',
            bg='white',
            activebackground='blue',
            activeforeground='yellow',
            command=self.start_game
        )
        self.play_button.pack(pady=200)
        self.play_button.focus_set()
        self.play_button.bind('<Return>', lambda e: self.start_game())

    def set_up_game_canvas(self):
        # create canvas where the game appears
        self.canvas = ScrolledCanvas(
            self.game_frame,
            width=GAME_SCREEN_W,
            height=GAME_SCREEN_H
        )

    def on_closing(self):
        """ not let anything running when closing the screen with x """
        running = False   # stop loop
        self.root.quit()
        self.root.destroy()

    def start_game(self):
        """ delete PLAY button and start playing a game """
        self.play_button.pack_forget()   # hide the play button after clicking
        self.canvas.pack(fill=BOTH, expand=True) # show the game canvas

        # game screen with all the components
        self.screen = TurtleScreen(self.canvas)
        self.screen.bgcolor('black')
        self.screen.tracer(0)
        self.turtle = RawTurtle(self.screen)

        # place paddle slightly above the bottom edge
        self.bouncing_board = BouncingBoard(self.screen, (0, BOARD_LOCATION), GAME_SCREEN_W)

        # a ball to appear
        self.ball = Ball(self.screen)

        # bricks to appear
        self.bricks = Blocks(self.screen, GAME_SCREEN_W)

        # force initial draw
        self.screen.update()
        self.ball.reset_position()        # reset ball to start
        self.game_play()

    def game_play(self):
        """functionarity of the game"""
        if not self.running or not self.root.winfo_exists():
            return  # stop if the window was closed

        self.ball.move()

        # ball bounces back when hitting the ceiling
        if self.ball.ycor() > (GAME_SCREEN_H // 2) - 60:
            self.ball.bounce_y()
        # ball bounces back when hitting the wallls - both sides
        if self.ball.xcor() > (GAME_SCREEN_W // 2) - 24 or self.ball.xcor() < -(GAME_SCREEN_W // 2) + 24:
            self.ball.bounce_x()
        # Bounce off paddle
        if self.ball.ycor() < BOARD_LOCATION + 20 and self.ball.distance(self.bouncing_board) < 160:
            self.ball.bounce_y()

        if self.ball.ycor() < BOARD_LOCATION - 20:
            self.game_over()

        # check block collisions
        for block in self.bricks.blocks[:]:
            if (block.left_wall < self.ball.xcor() < block.right_wall and
                block.bottom_wall < self.ball.ycor() < block.upper_wall):
                block.hideturtle()
                self.bricks.blocks.remove(block)
                self.ball.bounce_y()
                break

        self.screen.update()

        self.root.after(int(self.ball.move_speed * 1000), self.game_play)

    def run(self):
        self.root.mainloop()

    def game_over(self):
        """stops game when board didn't hit the ball"""
        self.running = False  # stop the game loop
        # dim the game screen
        overlay = tk.Frame(self.game_frame, bg='black')
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.attributes = {}
        try:
            overlay.tk.call('tk', 'canvas', 'create', 'rectangle')
        except Exception:
            pass

        dim_label = tk.Label(
            overlay,
            bg='black',
            width=GAME_SCREEN_W,
            height=GAME_SCREEN_H
        )
        dim_label.pack(fill='both', expand=True)
        dim_label.configure(bg='#000000', highlightthickness=0)
        dim_label.lower() # keep it behind text

        game_overLabel = tk.Label(
            overlay,
            text='Game Over',
            font=('Press Start 2P', 42, 'bold'),
            fg='yellow',
            bg='black'
        )
        game_overLabel.place(relx=0.5, rely=0.28, anchor='center')

        play_againButton = tk.Button(
            overlay,
            text='PLAY AGAIN',
            font=('Press Start 2P', 24),
            width=12,
            height=3,
            fg='white',
            bg='grey',
            activebackground='blue',
            activeforeground='yellow',
            command=lambda: self.restart_game(overlay)
        )
        play_againButton.place(relx=0.36, rely=0.58, anchor='center')

        exitButton = tk.Button(
            overlay,
            text='EXIT',
            font=('Press Start 2P', 24),
            width=8,
            height=3,
            fg='white',
            bg='grey',
            activebackground='blue',
            activeforeground='yellow',
            command=self.exit_game
        )
        exitButton.place(relx=0.7, rely=0.58, anchor='center')


        self.screen.update()

    def restart_game(self, overlay):
        overlay.destroy()
        self.running=True
        self.start_game()

    def exit_game(self):
        """exit the game and close the window."""
        self.running = False  # stop the game loop if running
        try:
            self.root.destroy()  # close the Tkinter window
        except tk.TclError:
            pass  # ignore if window already closed

