import turtle
import tkinter as tk

class Pong:
    def __init__(self):
        self.sc = turtle.Screen()
        self.sc.title("Pong Game")
        self.sc.bgcolor("black")
        self.sc.setup(width=1000, height=600)

        self.left_pad = self.create_paddle(-400)
        self.right_pad = self.create_paddle(400)

        self.hit_ball = self.create_ball()
        self.hit_ball.dx = 5
        self.hit_ball.dy = -5

        self.left_player = 0
        self.right_player = 0

        self.sketch = turtle.Turtle()
        self.init_scoreboard()

        self.bind_keys()

    def create_paddle(self, x_pos):
        pad = turtle.Turtle()
        pad.speed(0)
        pad.shape("square")
        pad.color("cyan")
        pad.shapesize(stretch_wid=5, stretch_len=2)
        pad.penup()
        pad.goto(x_pos, 0)
        return pad

    def create_ball(self):
        ball = turtle.Turtle()
        ball.speed(40)
        ball.shape("circle")
        ball.color("cyan")
        ball.penup()
        ball.goto(0, 0)
        return ball

    def init_scoreboard(self):
        self.sketch.speed(0)
        self.sketch.color("yellow")
        self.sketch.penup()
        self.sketch.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.sketch.clear()
        self.sketch.goto(0, 260)
        self.sketch.write(f"Left Player: {self.left_player} Right Player: {self.right_player}", align="center", font=("Comic Sans MS", 20, "bold"))

    def bind_keys(self):
        self.sc.listen()
        self.sc.onkeypress(lambda: self.move_paddle(self.left_pad, 20), "w")
        self.sc.onkeypress(lambda: self.move_paddle(self.left_pad, -20), "s")
        self.sc.onkeypress(lambda: self.move_paddle(self.right_pad, 20), "Up")
        self.sc.onkeypress(lambda: self.move_paddle(self.right_pad, -20), "Down")

    def move_paddle(self, pad, y_change):
        y = pad.ycor()
        y += y_change
        pad.sety(y)

    def check_collision(self):
        if (self.hit_ball.xcor() > 360 and self.hit_ball.xcor() < 370) and (self.hit_ball.ycor() < self.right_pad.ycor() + 60 and self.hit_ball.ycor() > self.right_pad.ycor() - 60):
            self.hit_ball.setx(360)
            self.hit_ball.dx *= -1

        if (self.hit_ball.xcor() < -360 and self.hit_ball.xcor() > -370) and (self.hit_ball.ycor() < self.left_pad.ycor() + 60 and self.hit_ball.ycor() > self.left_pad.ycor() - 60):
            self.hit_ball.setx(-360)
            self.hit_ball.dx *= -1


    def update_game(self):
        self.sc.update()

        self.hit_ball.setx(self.hit_ball.xcor() + self.hit_ball.dx)
        self.hit_ball.sety(self.hit_ball.ycor() + self.hit_ball.dy)

        if abs(self.hit_ball.ycor()) > 280:
            self.hit_ball.dy *= -1

        if abs(self.hit_ball.xcor()) > 500:
            if self.hit_ball.xcor() > 0:
                self.left_player += 1
            else:
                self.right_player += 1
            self.hit_ball.goto(0, 0)
            self.update_scoreboard()



    def run_game(self):
        while True:
            self.update_game()
            self.check_collision()
            if self.left_player >= 5 or self.right_player >= 5:
                self.display_game_over()
                self.sc.bye()
                break
    

    def display_game_over(self):
        winner = "Left Player wins!" if self.left_player >= 5 else "Right Player wins!"
        if not hasattr(self, 'root_destroyed') or not self.root_destroyed:
            root = tk.Tk()
            root.title("Game Over")
            label = tk.Label(root, text=f"Game Over! {winner}", font=("Comic Sans MS", 20, "bold"))
            label.pack(pady=20, padx=20)

            def play_again():
                root.destroy()
                self.reset_game()

            def exit_game():
                root.destroy()
                self.sc.bye()
                self.root_destroyed = True

            play_again_button = tk.Button(root, text="Play Again", command=play_again)
            play_again_button.pack(side=tk.LEFT, padx=(20, 10), pady=10)
            exit_button = tk.Button(root, text="Exit", command=exit_game)
            exit_button.pack(side=tk.RIGHT, padx=(10, 20), pady=10)

            root.mainloop()
            self.root_destroyed = True

    def reset_game(self):
      self.left_player = 0
      self.right_player = 0
      self.hit_ball.goto(0, 0)
      self.hit_ball.dx = 5
      self.hit_ball.dy = -5
      self.update_scoreboard()
      self.run_game()
        
if __name__ == "__main__":
    pong_game = Pong()
    pong_game.run_game()