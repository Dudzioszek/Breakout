import turtle
import time

# set up the screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Breakout Clone")
screen.tracer(0)

# create a paddle class
class Paddle(turtle.Turtle):
    def __init__(self):
        super().__init__(shape="square")
        self.penup()
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.goto(0, -250)
        self.speed(0)
        self.dx = 10
        
    def move_left(self):
        x = self.xcor()
        if x > -280:
            x -= self.dx
        self.setx(x)
        
    def move_right(self):
        x = self.xcor()
        if x < 280:
            x += self.dx
        self.setx(x)

class Ball(turtle.Turtle):
    def __init__(self, paddle):
        super().__init__(shape="circle")
        self.penup()
        self.color("white")
        self.goto(0, 0)
        self.speed(0)
        self.dx = 0.4
        self.dy = 0.4
        self.paddle = paddle
        
    def move(self):
        x = self.xcor()
        y = self.ycor()
        x += self.dx
        y += self.dy
        self.goto(x, y)
        
        # check for collision with walls
        if x > 290 or x < -290:
            self.dx *= -1
        if y > 290 or y < -290:
            self.dy *= -1
    
    def bounce(self):
        paddle_center = self.paddle.xcor()
        ball_distance = self.distance(self.paddle)
        if ball_distance > 0:
            # calculate percentage value of how far the ball is from the center of the paddle
            percentage = (self.xcor() - paddle_center) / ball_distance
            if percentage < -0.5:
                self.dx = -0.5
            elif percentage < 0:
                self.dx = -0.3
            elif percentage < 0.5:
                self.dx = 0.3
            else:
                self.dx = 0.5
        self.dy *= -1




        
# create a brick class
class Brick(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__(shape="square")
        self.penup()
        self.color("white")
        self.goto(x, y)
        self.shapesize(stretch_wid=0.5, stretch_len=5)
        self.speed(0)

# create a game class
class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.scoreboard = turtle.Turtle()
        self.scoreboard.hideturtle()
        self.scoreboard.penup()
        self.scoreboard.goto(-280, 260)
        self.update_scoreboard()
        
    def create_bricks(self):
        for i in range(-200, 200, 50):
            for j in range(150, 250, 25):
                brick = Brick(i, j)
                self.bricks.append(brick)
        
    def update_scoreboard(self):
        self.scoreboard.clear()
        self.scoreboard.write(f"Score: {self.score}   Lives: {self.lives}", align="left", font=("Courier", 14, "normal"))
        
    def start(self):
        self.create_bricks()
        
        turtle.listen()
        turtle.onkeypress(self.paddle.move_left, "Left")
        turtle.onkeypress(self.paddle.move_right, "Right")

        # move the ball
        while True:
            self.ball.move()
            self.scoreboard.clear()
            self.update_scoreboard()
            screen.update() # add this line
            self.scoreboard.showturtle()
            
            # check for collision with paddle
            if self.ball.distance(self.paddle) < 50 and self.ball.ycor() < -240:
                self.ball.bounce()
            
            # check for collision with bricks
            for brick in self.bricks:
                if self.ball.distance(brick) < 120:
                    self.ball.bounce()
                    brick.goto(1000, 1000)
                    self.bricks.remove(brick)
                    self.score += 10
                    self.update_scoreboard()
            
            # check for game over
            if self.ball.ycor() < -290:
                self.lives -= 1
                self.update_scoreboard()
                self.ball.goto(0, 0)
                self.ball.dy *= -1
                
            # check for game win
            if not self.bricks:
                self.scoreboard.clear()
                self.scoreboard.write("You Win!", align="center", font=("Courier", 24, "normal"))
                time.sleep(3)
                turtle.bye()
        


# create the game instance
game = Game()

# call the start method to start the game
game.start()

