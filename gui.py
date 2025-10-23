import json
import os
import webbrowser
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from CTkMenuBar import *
from PIL import Image, ImageTk  # Pillow library (pip install pillow)
from bouncingboard import BouncingBoard
from ball import Ball
from blocks import Blocks


SCREEN_W = 1390
SCREEN_H = 980
GAME_SCREEN_W = 1390
GAME_SCREEN_H = 850
BOARD_LOCATION = -(GAME_SCREEN_H // 2) + 80
LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)


class BreakOutApp():
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
        self.player_name = 'Guest'
        self.speed_increase_milestones = set()
        # pause
        self.paused = False
        self.pause_overlay = None  # placeholder for pause label
        # ball's xcor and ycor / location
        self.ball_xcor = None
        self.ball_ycor = None

        self.game_loop_id = None

        # Tkinter menu bar
        self.menu_bar = tk.Menu(self.root)

        # "Menu" dropdown
        menu_dropdown = tk.Menu(self.menu_bar, tearoff=0)
        menu_dropdown.add_command(label="Play", command=lambda: self.start_game(self.nameEntry.get()))
        menu_dropdown.add_command(label="Exit", command=self.exit_game)
        self.menu_bar.add_cascade(label="Menu", menu=menu_dropdown)

        # "Help" dropdown
        help_dropdown = tk.Menu(self.menu_bar, tearoff=0)
        help_dropdown.add_command(label="Help - GitHub", command=self.open_github)
        help_dropdown.add_command(label="About", command=self.open_about)
        self.menu_bar.add_cascade(label="Help", menu=help_dropdown)

        # attach menu bar to root
        self.root.config(menu=self.menu_bar)

        self.set_up_logo_frame()
        self.set_up_score_frame()
        self.set_up_game_frame()
        self.set_up_game_canvas()

        self.start_pause.config(image=self.start_pause_photo, command=self.toggle_pause_unpause)


    def set_up_logo_frame(self):
        # Top frame for game logo and title
        robo_img = Image.open("assets/robot.png").resize((64, 64))
        self.photo = ImageTk.PhotoImage(robo_img)
        # Frame to hold everything
        self.logo_frame = tk.Frame(self.root, bg="black")
        self.logo_frame.pack(pady=30)
        # left logo
        self.left_label = tk.Label(self.logo_frame, image=self.photo, bg="black")
        self.left_label.grid(row=0, column=0, padx=30, pady=10)
        # set a logo
        self.game_logo = tk.Label(
            self.logo_frame,
            text='BreakOut Game',
            font=('Press Start 2P', 54),
            fg='yellow',
            bg='black',
            anchor='center'
        )
        self.game_logo.grid(row=0, column=1, padx=30, pady=10)
        # right logo
        self.right_label = tk.Label(self.logo_frame, image=self.photo, bg="black")
        self.right_label.grid(row=0, column=2, padx=30, pady=10)

    def set_up_score_frame(self):
        """score frame where life/score/player name appear"""
        self.score_frame = tk.Frame(self.root, bg='black')
        self.score_frame.pack(pady=5)

        self.playerLabel = tk.Label(
            self.score_frame,
            text='PLAYER: ',
            font=('Press Start 2P', 14),
            fg='white',
            bg='black'
        )
        self.playerLabel.grid(padx=20, row=0, column=0)

        self.player_name_var = tk.StringVar(value=self.player_name)
        self.player_name = tk.Label(
            self.score_frame,
            textvariable=self.player_name_var,
            font=('Press Start 2P', 14),
            fg='white',
            bg='black'
        )
        self.player_name.grid(padx=5, row=0, column=1)

        start_pause_img = Image.open("assets/pause-play.png").resize((52, 40))
        self.start_pause_photo = ImageTk.PhotoImage(start_pause_img)
        self.start_pause = tk.Button(
            self.score_frame,
            image=self.start_pause_photo,
            fg='black',
            highlightthickness=0,
            command=self.toggle_pause_unpause
            )
        self.start_pause.grid(padx=200, row=0, column=2)

        self.score_value = 0
        self.score_label = tk.Label(
            self.score_frame,
            text=f"SCORE: {self.score_value}",
            font=('Press Start 2P', 14),
            fg='white',
            bg='black'
            )
        self.score_label.grid(padx=100, row=0, column=3)

        empty_heart_img = Image.open('assets/empty_heart.png').resize((40, 40))
        self.empty_heart_photo = ImageTk.PhotoImage(empty_heart_img)
        red_heart_img = Image.open('assets/red_heart.png').resize((48, 48))
        self.red_heart_photo = ImageTk.PhotoImage(red_heart_img)

        # Lives setup
        self.lives = 3
        self.life_labels = []
        for i in range(3):
            label = tk.Label(
                self.score_frame,
                image=self.red_heart_photo,
                bg='black'
                )
            label.grid(padx=5, row=0, column=4 + i)
            self.life_labels.append(label)

    def life_update(self):
        """Update heart icons based on remaining lives."""
        for i, label in enumerate(self.life_labels):
            if i < self.lives:
                label.config(image=self.red_heart_photo)
            else:
                label.config(image=self.empty_heart_photo)

    def set_up_game_frame(self):
        # main frame for playing a game
        # Frame to hold the game area
        self.game_frame = tk.Frame(self.root, bg="black")
        self.game_frame.pack(pady=10)
        # ask user name
        self.user_nameLabel = tk.Label(
            master=self.game_frame,
            text='Player Name:',
            font=('Press Start 2P', 22),
            fg='white',
            bg='black'
        )
        self.user_nameLabel.pack(pady=50)
        self.nameEntry = tk.Entry(
            master=self.game_frame,
            width=15,
            font=('Press Start 2P', 22),
            fg='black',
            bg='white',
            justify='center'
        )
        self.nameEntry.pack(padx=50, ipady=10)
        self.nameEntry.focus_set()
        # bind Enter on name entry → moves focus to PLAY button
        self.enter_binding = self.nameEntry.bind("<Return>", lambda e: self.play_button.focus_set())

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
            command=lambda: self.start_game(self.nameEntry.get())
        )
        self.play_button.pack(pady=200)
        self.play_button.focus_set()
        self.play_button.bind('<Return>', lambda e: self.start_game(self.nameEntry.get()))

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

    def start_game(self, player_name=None):
        # Unbind Enter key so it no longer works once the game starts
        if hasattr(self, "enter_binding") and self.enter_binding:
            self.nameEntry.unbind("<Return>", self.enter_binding)
            self.enter_binding = None
        self.play_button.unbind('<Return>')

        """ delete PLAY button and start playing a game """
        self.user_nameLabel.pack_forget()
        self.nameEntry.pack_forget()
        self.play_button.pack_forget()   # hide the play button after clicking
        self.canvas.pack(fill=BOTH, expand=True) # show the game canvas

        # Only update player name if a new one is provided
        if player_name:
            self.player_name = player_name
        else:
            self.player_name = 'Guest'

        # update visible player name in the score frame
        if hasattr(self, 'player_name_var'):
            self.player_name_var.set(self.player_name)

        # game screen with all the components
        self.screen = TurtleScreen(self.canvas)
        self.screen.bgcolor('black')
        self.screen.tracer(0)
        self.turtle = RawTurtle(self.screen)

        # place paddle slightly above the bottom edge
        self.bouncing_board = BouncingBoard(self.screen, (0, BOARD_LOCATION), GAME_SCREEN_W)

        # bind keys to root (Tkinter)
        self.root.bind("<Right>", lambda e: (self.bouncing_board.right(), self.screen.update()))
        self.root.bind("<Left>", lambda e: (self.bouncing_board.left(), self.screen.update()))

        self.root.bind("<space>", self.toggle_pause_unpause)

        # Always create new ball and blocks for a new game
        if hasattr(self, 'ball'):
            self.ball.hideturtle()
            del self.ball
        if hasattr(self, 'bricks'):
            for block in self.bricks.blocks:
                block.hideturtle()
            del self.bricks

        self.ball = Ball(self.screen)
        self.bricks = Blocks(self.screen, GAME_SCREEN_W)

        # force initial draw
        self.screen.update()

        # Only reset if starting fresh (no saved coordinates)
        if self.ball_xcor is None and self.ball_ycor is None:
            self.ball.reset_position()
        else:
            self.ball.goto(self.ball_xcor, self.ball_ycor)
            if hasattr(self, 'paused_heading') and self.paused_heading is not None:
                self.ball.setheading(self.paused_heading)

        # Start the game loop immediately
        self.game_play()
        self.canvas.focus_set()

    def game_play(self):
        if self.paused or not self.running or not self.root.winfo_exists():
            return  # stop loop if paused

        self.ball.move()

        # ball bounces back when hitting the ceiling
        if self.ball.ycor() > (GAME_SCREEN_H // 2) - 60:
            self.ball.bounce_y()
        # ball bounces back when hitting the wallls - both sides
        if self.ball.xcor() > (GAME_SCREEN_W // 2) - 24 or self.ball.xcor() < -(GAME_SCREEN_W // 2) + 24:
            self.ball.bounce_x()

        if self.ball.ycor() < BOARD_LOCATION - 20:
            self.lives -= 1
            self.life_update()
            if self.lives <= 0:
                self.game_over()
            else:
                self.ball.reset_position()
                self.ball.bounce_y()
                self.game_loop_id = self.root.after(int(self.ball.move_speed * 1000), self.game_play)
            return

        # Bounce off paddle
        if self.ball.ycor() < BOARD_LOCATION + 17 and self.ball.distance(self.bouncing_board) < 160:
            self.ball.bounce_y()

        if self.ball.ycor() > (GAME_SCREEN_H // 2) - 60:
            self.win()

        # check block collisions
        for block in self.bricks.blocks[:]:
            if (block.left_wall < self.ball.xcor() < block.right_wall and
                block.bottom_wall < self.ball.ycor() < block.upper_wall):
                block.hideturtle()
                self.bricks.blocks.remove(block)
                self.ball.bounce_y()

                # update score
                self.score_value += 5
                self.score_label.config(text=f"SCORE: {self.score_value}")

                # increase ball speed at certain score milestones
                if self.score_value in (200, 400, 600) and self.score_value not in self.speed_increase_milestones:
                    self.ball.ball_speed_up()
                    self.speed_increase_milestones.add(self.score_value)
                break

        self.screen.update()

        # Prevent overlapping scheduled loops:
        if self.game_loop_id:
            try:
                self.root.after_cancel(self.game_loop_id)
            except Exception:
                pass
            self.game_loop_id = None

        self.game_loop_id = self.root.after(int(self.ball.move_speed * 1000), self.game_play)

    def run(self):
        self.root.mainloop()

    def update_leaderboard(self):
        leaderboard = load_leaderboard()
        # Add current player
        leaderboard.append({"name": self.player_name, "score": self.score_value})
        # Sort descending by score
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        # Keep top 3
        leaderboard = leaderboard[:3]
        save_leaderboard(leaderboard)
        return leaderboard

    def get_leaderboard_text(self):
        leaderboard = load_leaderboard()
        if not leaderboard:
            return "No scores yet"
        text = "* Leaderboard Ranking *\n\n\n"
        for i, entry in enumerate(leaderboard, 1):
            text += f"{i}. Name: {entry['name']} Score:{entry['score']}\n\n"
        return text

    def win(self):
        """stops game as player won"""
        self.running = False  # stop the game loop
        # save score/player name in leaderboard if the score is in the top 3 in history
        self.update_leaderboard()

        # on top of the game screen
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
            text='You Won!',
            font=('Press Start 2P', 42, 'bold'),
            fg='yellow',
            bg='black'
        )
        game_overLabel.place(relx=0.5, rely=0.12, anchor='center')
        game_overLabel = tk.Label(
            overlay,
            text=f'\nYour final score: {self.score_value}',
            font=('Press Start 2P', 24, 'bold'),
            fg='orange',
            bg='black'
        )
        game_overLabel.place(relx=0.5, rely=0.22, anchor='center')

        leaderboard_text = self.get_leaderboard_text()
        leader_board = tk.Label(
            overlay,
            text=leaderboard_text,
            font=('Press Start 2P', 20),
            fg='white',
            bg='black',
            justify='left',   # left-align multiple lines
            anchor='nw'       # anchor top-left
        )
        leader_board.place(relx=0.5, rely=0.52, anchor='center')

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
        play_againButton.place(relx=0.36, rely=0.80, anchor='center')

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
        exitButton.place(relx=0.7, rely=0.80, anchor='center')


        self.screen.update()

    def game_over(self):
        """stops game when board didn't hit the ball"""
        self.running = False  # stop the game loop
        # save score/player name in leaderboard if the score is in the top 3 in history
        self.update_leaderboard()

        # on top of the game screen
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
        game_overLabel.place(relx=0.5, rely=0.22, anchor='center')

        leaderboard_text = self.get_leaderboard_text()
        leader_board = tk.Label(
            overlay,
            text=leaderboard_text,
            font=('Press Start 2P', 20),
            fg='white',
            bg='black',
            justify='left',   # left-align multiple lines
            anchor='nw'       # anchor top-left
        )
        leader_board.place(relx=0.5, rely=0.5, anchor='center')

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
        play_againButton.place(relx=0.36, rely=0.80, anchor='center')

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
        exitButton.place(relx=0.7, rely=0.80, anchor='center')

        self.screen.update()

    def restart_game(self, overlay):
        overlay.destroy()
        self.running=True
        self.lives = 3
        self.life_update()
        self.score_value = 0
        self.score_label.config(text=f"SCORE: {self.score_value}")
        self.start_game()

    def exit_game(self):
        """exit the game and close the window."""
        self.running = False  # stop the game loop if running
        try:
            self.root.destroy()  # close the Tkinter window
        except tk.TclError:
            pass  # ignore if window already closed

    def open_about(self):
        """open 'About' popup page to show the copyright"""
        about = tk.Toplevel(self.root)
        about.title('About')
        about.geometry('700x250')
        about.resizable(False, False)
        about.configure(bg='black')

        label = tk.Label(
            about,
            text='BreakOut Game App\n\n'
            'Created with Python, tkinter, Pillow, Turtle and CustomTkinter\n'
            'copyright 2025 LegradiK',
            font=('Arial', 16),
            fg='white',
            bg='black',
            justify='center'
        )
        label.pack(expand=True, padx=20, pady=20)
        close_button = tk.Button(
            about,
            text='Close',
            font=('Arial', 14),
            fg='white',
            bg='grey',
            command=about.destroy
        )
        close_button.pack(pady=10)

    def open_github(self):
        """Open Github project page in default browser"""
        webbrowser.open_new("https://github.com/LegradiK/breakout_game.git")

    def toggle_unpause(self, event=None):
        if not self.running or not hasattr(self, 'ball'):
            return

        if self.paused:
            # Resume the game
            self.paused = False
            self.unpaused = True

            # Remove pause overlay
            if self.pause_overlay:
                self.pause_overlay.destroy()
                self.pause_overlay = None
            if hasattr(self, 'pause_frame') and self.pause_frame:
                self.pause_frame.destroy()
                self.pause_frame = None

            self.screen.update()
            # Continue game loop
            self.game_play()


    def pause(self):
        if not self.paused and self.running and hasattr(self, 'ball'):
            self.paused = True
            # Save ball position and heading
            self.ball_xcor = self.ball.xcor()
            self.ball_ycor = self.ball.ycor()
            self.paused_heading = self.ball.heading()
            # Cancel scheduled loop so ball stops moving
            if self.game_loop_id:
                try:
                    self.root.after_cancel(self.game_loop_id)
                except Exception:
                    pass
                self.game_loop_id = None
            # Dimmed overlay
            self.pause_frame = tk.Frame(self.game_frame, bg='black')
            self.pause_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pause_overlay = tk.Label(
                self.pause_frame,
                text='PAUSED',
                font=('Press Start 2P', 72, 'bold'),
                fg='white',
                bg='black'
            )
            self.pause_overlay.place(relx=0.5, rely=0.5, anchor='center')

    def unpause(self):
        if self.paused and self.running and hasattr(self, 'ball'):
            self.paused = False
            # Remove pause overlay
            if self.pause_overlay:
                self.pause_overlay.destroy()
                self.pause_overlay = None
            if hasattr(self, 'pause_frame') and self.pause_frame:
                self.pause_frame.destroy()
                self.pause_frame = None
            # Restore ball position and heading
            if self.ball_xcor is not None and self.ball_ycor is not None:
                self.ball.goto(self.ball_xcor, self.ball_ycor)
            if hasattr(self, 'paused_heading') and self.paused_heading is not None:
                self.ball.setheading(self.paused_heading)
            self.screen.update()
            # Continue game loop
            self.game_play()

    def toggle_pause_unpause(self, event=None):
        if self.paused:
            self.unpause()
        else:
            self.pause()