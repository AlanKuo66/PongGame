import turtle
import tkinter as tk
import threading

# Options
PLAY_AUDIO = True
PLAY_AUDIO_THREAD = True
PLAY_LIB_PYDUB = False
PLAY_LIB_PYGAME = True

if PLAY_LIB_PYGAME:
    import pygame
    pygame.mixer.init()
    pygame.mixer.set_num_channels(20)
elif PLAY_LIB_PYDUB:
    from pydub import AudioSegment
    from pydub.playback import play as pyduplay
else:
    import simpleaudio as sa

# Ball
BALL_W = 21
BALL_H = 21

# Turtle Graphics Stamp Size
STAMP_SIZE = 20

# Game Table
GAMETABLE_W = 800
GAMETABLE_H = 600
GAMETABLE_MARGIN_X1 = GAMETABLE_W / 2
GAMETABLE_MARGIN_X2 = -GAMETABLE_MARGIN_X1
GAMETABLE_MARGIN_Y1 = GAMETABLE_H / 2
GAMETABLE_MARGIN_Y2 = -GAMETABLE_MARGIN_Y1
GAMETABLE_MARGIN_BALL_X1 = (GAMETABLE_W - BALL_W) / 2
GAMETABLE_MARGIN_BALL_X2 = -GAMETABLE_MARGIN_BALL_X1
GAMETABLE_MARGIN_BALL_Y1 = (GAMETABLE_H - BALL_H) / 2
GAMETABLE_MARGIN_BALL_Y2 = -GAMETABLE_MARGIN_BALL_Y1

# Maximum Balls
BALL_NUM = 5

# Pads
PAD_1_X = -350
PAD_1_Y = 0
PAD_1_W = 21
PAD_1_H = 101
PAD_1_MOV_X = 0
PAD_1_MOV_Y = 50

PAD_2_X = 350
PAD_2_Y = 0
PAD_2_W = 21
PAD_2_H = 101
PAD_2_MOV_X = 0
PAD_2_MOV_Y = 50

# Sounds
SOUND_FILE_PADDLE   = 'paddle.wav'
SOUND_FILE_WALL     = 'wall.wav'
SOUND_FILE_SCORE    = 'score.wav'

audio_play_list = []
def audio_play(audio_obj):
    if PLAY_LIB_PYGAME:
        # force to find a free channel and stop the longest 1 if no free channel
        channel = pygame.mixer.find_channel()
        if channel is not None:
            channel.play(audio_obj)
    elif PLAY_LIB_PYDUB:
        th = threading.Thread(target=pyduplay, args=(audio_obj,))
        th.start()
        audio_play_list.append(th)
    elif PLAY_AUDIO_THREAD:
        th = threading.Thread(target=lambda audio_obj:
            audio_obj.play().wait_done() , args=(audio_obj,))
        th.start()
        audio_play_list.append(th)
    else:
        audio_play_list.append(audio_obj.play())
        audio_play_list[-1].wait_done()

def audio_maintain():
    global audio_play_list
    if PLAY_LIB_PYGAME:
        pass
    elif PLAY_LIB_PYDUB or PLAY_AUDIO_THREAD:
        audio_play_list_remained = []
        for player in audio_play_list:
            if player.is_alive() is True:
                audio_play_list_remained.append(player)
            else:
                pass
        audio_play_list = audio_play_list_remained
        print("remained players thread: ", len(audio_play_list))
    else:
        audio_play_list_remained = []
        for player in audio_play_list:
            if player.is_playing() is True:
                audio_play_list_remained.append(player)
            else:
                player.wait_done()
        audio_play_list = audio_play_list_remained
        print("remained players: ", len(audio_play_list))

def audio_stop():
    global audio_play_list
    if PLAY_LIB_PYGAME:
        pygame.mixer.stop()
    if PLAY_LIB_PYDUB or PLAY_AUDIO_THREAD:
        for player in audio_play_list:
            player.join()
    else:
        sa.stop_all()
        audio_maintain()

# Load Sounds
if PLAY_LIB_PYGAME:
    audio_paddle        = pygame.mixer.Sound(SOUND_FILE_PADDLE)
    audio_wall_paddle   = pygame.mixer.Sound(SOUND_FILE_WALL)
    audio_score_paddle  = pygame.mixer.Sound(SOUND_FILE_SCORE)
elif PLAY_LIB_PYDUB:
    audio_paddle        = AudioSegment.from_wav(SOUND_FILE_PADDLE)
    audio_wall_paddle   = AudioSegment.from_wav(SOUND_FILE_WALL)
    audio_score_paddle  = AudioSegment.from_wav(SOUND_FILE_SCORE)
else:
    audio_paddle        = sa.WaveObject.from_wave_file(SOUND_FILE_PADDLE)
    audio_wall_paddle   = sa.WaveObject.from_wave_file(SOUND_FILE_WALL)
    audio_score_paddle  = sa.WaveObject.from_wave_file(SOUND_FILE_SCORE)
    audio_play(audio_paddle) # buggy, need to play a dummy sound

# Window
wn = turtle.Screen()
wn.title("pong")
wn.bgcolor("black")
wn.setup(width=GAMETABLE_W, height=GAMETABLE_H)
wn.tracer(0)

closed = False
def on_close():
    global closed
    closed = True

# Register hander for close event
tk._default_root.protocol("WM_DELETE_WINDOW", on_close)

# Socre
score_a = 0
score_b = 0

# Build Paddles
# Paddle A
paddle_a=turtle.Turtle()
paddle_a.speed=0
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(PAD_1_H / STAMP_SIZE, PAD_1_W / STAMP_SIZE)
paddle_a.penup()
paddle_a.goto(PAD_1_X,PAD_1_Y)

# Paddle B
paddle_b=turtle.Turtle()
paddle_b.speed=0
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(PAD_2_H / STAMP_SIZE, PAD_2_W / STAMP_SIZE)
paddle_b.penup()
paddle_b.goto(PAD_2_X,PAD_2_Y)

# Balls Control Table
balls = []
balls_delta_init = [[0.2, 0.2], [0.1, 0.1], [0.2, -0.2], [-0.1, 0.2], [-0.2,-0.2]]
balls_speed = [-1.5, -2, -1.5, -2, -1.5]
balls_speed_limited = [7.6, 6.4, 6.4, 6.4, 6.4]

# Instance Balls
for i in range(min(len(balls_delta_init), BALL_NUM)):
    ball = turtle.Turtle()
    ball.speed=0
    ball.shape("square")
    ball.color("white")
    ball.penup()
    ball.goto(0,0)
    ball.dx=balls_delta_init[i][0]
    ball.dy=balls_delta_init[i][1]
    balls.append(ball)

# Pen
pen=turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("player 1: 0  player 2: 0", align="center", font=("Courier", 24, "normal"))

# Key Map Functions
def paddle_a_up():
    y=paddle_a.ycor()
    distanceY = paddle_a.distance(paddle_a.xcor(), GAMETABLE_MARGIN_Y1)
    if distanceY - PAD_1_MOV_Y < (PAD_1_H / 2):
        y = GAMETABLE_MARGIN_Y1 - (PAD_1_H / 2)
    else:
        y+=PAD_1_MOV_Y
    paddle_a.sety(y)

def paddle_a_down():
    y=paddle_a.ycor()
    distanceY = paddle_a.distance(paddle_a.xcor(), GAMETABLE_MARGIN_Y2)
    if distanceY - PAD_1_MOV_Y < (PAD_1_H / 2):
        y = GAMETABLE_MARGIN_Y2 + (PAD_1_H / 2)
    else:
        y-=PAD_1_MOV_Y
    paddle_a.sety(y)

def paddle_b_up():
    y=paddle_b.ycor()
    distanceY = paddle_b.distance(paddle_b.xcor(), GAMETABLE_MARGIN_Y1)
    if distanceY - PAD_2_MOV_Y < (PAD_2_H / 2):
        y = GAMETABLE_MARGIN_Y1 - (PAD_2_H / 2)
    else:
        y+=PAD_2_MOV_Y
    paddle_b.sety(y)

def paddle_b_down():
    y=paddle_b.ycor()
    distanceY = paddle_b.distance(paddle_b.xcor(), GAMETABLE_MARGIN_Y2)
    if distanceY - PAD_2_MOV_Y < (PAD_2_H / 2):
        y = GAMETABLE_MARGIN_Y2 + (PAD_2_H / 2)
    else:
        y-=PAD_2_MOV_Y
    paddle_b.sety(y)


# XXXX
bXXXEnable = False
def paddle_fn_z():
    global bXXXEnable
    bXXXEnable = ~bXXXEnable

# keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
wn.onkeypress(paddle_fn_z, "z")

# collision detection
def is_collided_with(a, b, w, h):
    distanceX = a.distance(b.xcor(), a.ycor())
    distanceY = a.distance(a.xcor(), b.ycor())
    return (distanceX < w / 2 and distanceY < h / 2)

# Main game loop
while True:
    try:
        wn.update()
    except:
        print("Turtle update error:", sys.exc_info()[0])

    if  closed is True:
        break

    # trap errors, closing exception...
    #try:
    # Walk for all balls
    for i in range(len(balls)):
        curBall = balls[i]
        
        # Move the ball
        curBall.setx(curBall.xcor()+curBall.dx)
        curBall.sety(curBall.ycor()+curBall.dy)

        # Border checking
        if curBall.ycor() > GAMETABLE_MARGIN_BALL_Y1:
            curBall.sety(GAMETABLE_MARGIN_BALL_Y1)
            curBall.dy *=-1
            if PLAY_AUDIO:
                audio_play(audio_wall_paddle)

        if curBall.ycor() < GAMETABLE_MARGIN_BALL_Y2:
            curBall.sety(GAMETABLE_MARGIN_BALL_Y2)
            curBall.dy *=-1
            if PLAY_AUDIO:
                audio_play(audio_wall_paddle)

        if curBall.xcor() > GAMETABLE_MARGIN_BALL_X1:
            curBall.goto(0,0)
            curBall.dx *=-1
            score_a +=1
            pen.clear()
            pen.write("player 1: {}  player 2: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
            curBall.dx=balls_delta_init[i][0]
            curBall.dy=balls_delta_init[i][1]
            if PLAY_AUDIO:
                audio_play(audio_score_paddle)
    
        if curBall.xcor() < GAMETABLE_MARGIN_BALL_X2:
            curBall.goto(0,0)
            curBall.dx *=-1
            score_b +=1
            pen.clear()
            pen.write("player 1: {}  player 2: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
            curBall.dx=balls_delta_init[i][0]
            curBall.dy=balls_delta_init[i][1]
            if PLAY_AUDIO:
                audio_play(audio_score_paddle)

        # Paddle and ball collisions
        # Paddle A
        if is_collided_with(curBall, paddle_a, PAD_1_W + BALL_W, PAD_1_H + BALL_H):
            curBall.setx(PAD_1_X + (PAD_1_W + BALL_W) / 2)
            offset = (curBall.ycor() - paddle_a.ycor()) / (PAD_1_H / 2)
            curBall.dx *=balls_speed[i]
            curBall.dy+=offset
            if PLAY_AUDIO:
                audio_play(audio_paddle)
            # XXX
            if bXXXEnable:
                curBall.dx = 15

        # Paddle B
        if is_collided_with(curBall, paddle_b, PAD_2_W + BALL_W, PAD_2_H + BALL_H):
            curBall.setx(PAD_2_X - (PAD_2_W + BALL_W) / 2)
            offset = (curBall.ycor() - paddle_b.ycor()) / (PAD_2_H / 2)
            curBall.dx *=balls_speed[i]
            curBall.dy+=offset
            if PLAY_AUDIO:
                audio_play(audio_paddle)

        # Speed limitation
        if curBall.dx > balls_speed_limited[i]:
            curBall.dx = balls_speed_limited[i] - 0.1

        # Audio resource maintain
        audio_maintain()
    #except:
    #    print("Unexpected error:", sys.exc_info()[0])

audio_stop()