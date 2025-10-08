import time
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk  # Pillow library (pip install pillow)
from bouncingboard import BouncingBoard

screen_w = 1390
screen_h = 980
game_screen_w = 1390
game_screen_h = 850

# create Tk app
root = Tk()
root.title('BreakOut Game')
# fix root size
root.geometry(f'{screen_w}x{screen_h}')
root.resizable(False, False)
# set color
root.configure(bg='black')

# Load PNGs
robo_img = Image.open("robot.png").resize((64, 64))

photo = ImageTk.PhotoImage(robo_img)

# Frame to hold everything
logo_frame = tk.Frame(root, bg="black")
logo_frame.pack(pady=30)
# left logo
left_label = tk.Label(logo_frame, image=photo, bg="black")
left_label.grid(row=0, column=0, padx=30, pady=30)
# set a logo
game_logo = tk.Label(
    logo_frame,
    text='BreakOut Game',
    font=('Press Start 2P', 54),
    fg='yellow',
    bg='black',
    anchor='center'
)
game_logo.grid(row=0, column=1, padx=30, pady=30)
# right logo
right_label = tk.Label(logo_frame, image=photo, bg="black")
right_label.grid(row=0, column=2, padx=30, pady=30)

# Frame to hold the game area
game_frame = tk.Frame(root, bg="black")
game_frame.pack(pady=10)

# create canvas where the game appears
canvas = ScrolledCanvas(
    game_frame,
    width=game_screen_w,
    height=game_screen_h
    )
canvas.pack(fill=BOTH, expand=True)


screen = TurtleScreen(canvas)
screen.bgcolor('black')
screen.tracer(0)
turtle = RawTurtle(screen)

# place paddle slightly above the bottom edge
paddle_y = -(game_screen_h // 2) + 80
bouncing_board = BouncingBoard(screen, (0, paddle_y), game_screen_w)

# force initial draw
screen.update()

# bind keys to root (Tkinter)
root.bind("<Right>", lambda e: (bouncing_board.right(), screen.update()))
root.bind("<Left>", lambda e: (bouncing_board.left(), screen.update()))


root.mainloop()