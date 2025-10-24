# 🕹️ BreakOut Game

**Day 87 – Portfolio Project**

A Python implementation of the classic **Breakout** arcade game — built with **Tkinter** and **Turtle Graphics**, featuring pixel art design, leaderboard tracking, and dynamic speed challenges.

---

## 🎮 Features

- 🧱 **Classic Breakout gameplay** – bounce the ball to break blocks to reach the ceiling!
- 🕹️ **Keyboard control** – move the paddle with arrow keys.
- 🧍 **Player name entry** – personalise your session.
- ❤️ **Lives system** – with pixel-art hearts.
- ⚡ **Speed increases** – ball moves faster as your score rises.
- 🏆 **Leaderboard** – saves and displays top 3 high scores (`leaderboard.json`).
- 👾 **Retro design** – pixel-art robot and 8-bit inspired “Press Start 2P” font.

---

## 🖼️ Assets & Credits

- 🤖 **Robot icon**:
  [Robot icons created by YardenG – Flaticon](https://www.flaticon.com/free-icon/robot_8254111?term=robot&page=2&position=88&origin=search&related_id=8254111)

- 🧡 **Heart pixel art**:
  Created by ChatGPT.

- **Start/Pause button**:
  ['Pause Play free icon created by Angelo Trolano](https://www.flaticon.com/free-icon/pause-play_5725942?term=pause&page=1&position=23&origin=search&related_id=5725942)

- 🎨 **Font**:
  [“Press Start 2P”](https://fonts.google.com/specimen/Press+Start+2P) from Google Fonts.


---

## 🧩 Project Structure
``` breakout_game/
├── main.py # Main application file
├── gui.py
├── ball.py # Ball class (movement, bounce, speed)
├── bouncingboard.py # Paddle control and movement
├── blocks.py # Block and block-lane creation
├── leaderboard.json # Stores top 3 scores
├── assets
    ├── robot.png # Logo icon
    ├── red_heart.png # Full heart icon
    ├── empty_heart.png # Empty heart icon
    ├── pause-play.png # Pause/Play icon
├── documentations
    ├── OFL.txt # documentation for 'Press Start 2P'
├── LICENSE # MIT license
├── PressStart2P-Regular.ttf # special retro stype font
└── README.md # This file
```

## Requirements
This project was developed with **Python 3.8.10**

Install dependencies with:
``` bash
pip install pillow
```
**Built-in libraries used:**
- tkinter
- turtle
- json
- os

## How to Play
1. Clone or download the project
   ``` bash
   git clone https://github.com/LegradiK/breakout_game.git
   cd breakout_game
   ```
2. Run the game:
   ``` bash
   python3 main.py
3. Enter your **player name** and press **Enter** or click **Play**.
4. Use **Left arrow ←** and **Right arrow →** keys to move the bouncing board.
5. Use **Space key** or click **Play/Pause button** to pause the game when needed.
6. Break the bricks to reach the top ceiling to win!
7. Check your score and ranking on the leaderboard.

## 🧠 Game Logic Summary

- The ball bounces off:
  - Walls
  - The bouncing board
  - Blocks/Bricks (which get destroyed once ball touches it)
- If the ball drops below the paddle:
  - You lose a life.
- Lose all 3 lives → **Game Over**
- Ball touchs the top ceiling → **You Win!**
- Your score and name are stored in leaderboard.json. if the score is in top 3

## 📜 License
MIT License

## Author
LegradiK - [Github](https://github.com/LegradiK)
Day 87 portfolio project - creating BreakOut Game
Created using **Python (Tkinter, Pillow, Turtle Graphics)**


