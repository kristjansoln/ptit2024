# The Snake Game
#
# Tutorial
# https://medium.com/@wepypixel/step-by-step-guide-python-code-for-snake-game-development-3e0ec9f7522e

import turtle
import time
import random
import socket
# import getch

# SPREMENLJIVKE
step_size = 20
screen_width = 600
screen_height = 400
wall_width = 300
wall_height = 250
score = 0
high_score = 0
delay_initial = 0.2
delay = delay_initial
# mark timer
timer = time.time()
mark_interval = 10

headstones = ["☠", "⛧", "✟", "✝", "♱"]
colors = ["red", "blue", "green", "orange", "cyan", "yellow", "brown", "black"]

UDP_IP = "127.0.0.1"
UDP_PORT = 15005

segments = []


# FUNKCIJE


def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():  # Funkcija za premik v trenutni smeri
    # Get current head coordinates
    y = head.ycor()
    x = head.xcor()

    # Calculate new coordinates
    if head.direction == "up":
        y = y + step_size
    elif head.direction == "left":
        x = x - step_size
    elif head.direction == "down":
        y = y - step_size
    elif head.direction == "right":
        x = x + step_size
    elif head.direction == "stop":
        pass

    # Update head coordinates
    head.setx(x)
    head.sety(y)


def reset_game():
    # Ponastavi igro
    global delay, score, segments, screen

    # Ustavi kaco
    head.direction = "stop"
    scoreboard.clear()
    scoreboard.write(
        "Oh no!",
        align="center",
        font=("Courier", 24, "normal"),
    )

    # Draw a tombstone
    head.write(
        random.choice(headstones),
        align="center",
        font=("Arial", 14, "normal"),
    )

    # Flash screen
    screen.bgcolor("red")
    screen.update()
    time.sleep(2)
    screen.bgcolor("white")
    screen.update()

    # Clear the scoreboard
    scoreboard.clear()
    scoreboard.write(
        "Anyway",
        align="center",
        font=("Courier", 24, "normal"),
    )

    # Odstrani segmente
    for index in range(len(segments)):
        segments[index].goto(screen_width + 30, screen_height + 30)
    segments = []

    # Ponastavi polozaj, hitrost in score
    head.goto(0, 0)
    delay = delay_initial
    score = 0
    screen.update()


# SETUP

# SETUP - izvedemo enkrat
# Screen
screen = turtle.Screen()
screen.title("Piton")
screen.bgcolor("white")
screen.setup(width=screen_width, height=screen_height)
screen.tracer(0, 0)  # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.shape("square")
head.color("black")
head.penup()
head.speed(0)
head.direction = "stop"
head.goto(0, 0)

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.penup()
scoreboard.speed(0)
scoreboard.goto(0, screen_height / 2 - 50)
scoreboard.hideturtle()
scoreboard.write(
    f"Score: {score}, High Score: {high_score}",
    align="center",
    font=("Courier", 24, "normal"),
)

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("brown")
food.penup()
food.speed(0)
food.goto(30, -130)

# Listen to keyboard input
screen.listen()
screen.onkeypress(go_up, "w")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_right, "d")

# Extra: draw the wall
wall = turtle.Turtle()
wall.speed(0)
wall.hideturtle()
wall.penup()
wall.goto(wall_width / 2 + step_size, wall_height / 2 + step_size)
wall.pendown()
wall.goto(-wall_width / 2 - step_size, wall_height / 2 + step_size)
wall.goto(-wall_width / 2 - step_size, -wall_height / 2 - step_size)
wall.goto(wall_width / 2 + step_size, -wall_height / 2 - step_size)
wall.goto(wall_width / 2 + step_size, wall_height / 2 + step_size)

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM,
)  # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

# LOOP


while True:
    # Preveri ce smo zadeli hrano
    if head.distance(food) < 20:
        # Premakni hrano na nakljucno lokacijo
        # x = random.randint(-screen_width / 2, screen_width / 2)
        # y = random.randint(-screen_height / 2, screen_height / 2)
        x = random.randint(-wall_width / 2, wall_width / 2)
        y = random.randint(-wall_height / 2, wall_height / 2)
        food.goto(x, y)

        # Povecaj rezultat in posodobi napis
        score = score + 1
        if score > high_score:
            high_score = score
        scoreboard.clear()
        scoreboard.write(
            f"Score: {score}, High Score: {high_score}",
            align="center",
            font=("Courier", 24, "normal"),
        )

        # Dodaj segment
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color(random.choice(colors))
        new_segment.penup()
        new_segment.speed(0)
        segments.append(new_segment)

        # Pohitri igro
        delay = delay * 0.95

    # Preveri ce smo zadeli steno
    hx = head.xcor()
    hy = head.ycor()
    left_wall = -wall_width / 2
    right_wall = wall_width / 2
    top_wall = wall_height / 2
    bottom_wall = -wall_height / 2
    # Za debug
    # print(f"glava: ({hx}, {hy}), zidovi: {left_wall}, {right_wall}, {top_wall}, {bottom_wall}")

    if hx < left_wall or hx > right_wall or hy > top_wall or hy < bottom_wall:
        # print("Izven igrisca")
        reset_game()

        # Ustavi kaco
        # head.direction = "stop"
        # scoreboard.clear()
        # scoreboard.write(
        #    "Oh no!",
        #    align="center",
        #    font=("Courier", 24, "normal"),
        # )
        # head.write(
        #    random.choice(headstones),
        #    align="center",
        #    font=("Arial", 14, "normal"),
        # )
        # time.sleep(2)
        # scoreboard.clear()
        # scoreboard.write(
        #    "Anyway",
        #    align="center",
        #    font=("Courier", 24, "normal"),
        # )

        # Ponastavi polozaj, hitrost in score
        # head.goto(0, 0)
        # delay = delay_initial
        # score = 0

    # mark every 5 to 15 seconds
    if abs(timer - time.time()) > mark_interval:
        head.write("ඞ", font=("Arial", 8, "normal"))
        timer = time.time()

    # Move the segments
    for index in range(len(segments) - 1, 0, -1):
        # print(f"len(segments): {len(segments)}, index: {index}")
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is, because it was not handled yet
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    # Make the head move forward in the current direction
    move()
    screen.update()

    # Check for collision with body
    # We skip the first segment (neck always touches the head)
    for index in range(1, len(segments)):
        if head.distance(segments[index]) < step_size:
            # print(f"Collision with body on segment {index}")
            reset_game()
            break  # Koncaj for loop

    # Better delay and network listener
    start = time.time()
    next_move = None
    while abs(start - time.time()) < delay:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            next_move = bytes.decode(data, "ascii")
            print(f"got {next_move}, from {addr}")
        except BlockingIOError:
            # Throws BlockingIOError when no data is available
            pass

    # The last received valid character is used to determine new direction
    if next_move is not None:
        if next_move == "w":
            go_up()
        elif next_move == "a":
            go_left()
        elif next_move == "s":
            go_down()
        elif next_move == "d":
            go_right()
