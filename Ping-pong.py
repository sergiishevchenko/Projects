'''
Ping-pong game
'''

import simplegui
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
SIDE = LEFT

def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) / 60, -(random.randrange(60, 180) /60)]
    else:
        ball_vel = [-(random.randrange(120, 240) / 60), -(random.randrange(60, 180) / 60)]


def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    global SIDE
    paddle1_pos, paddle2_pos = (HEIGHT - PAD_HEIGHT)/2, (HEIGHT - PAD_HEIGHT)/2
    paddle1_vel = paddle2_vel = 0
    score1, score2 = 0, 0
    SIDE = not SIDE
    spawn_ball(SIDE)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos <= ball_pos[1] <= (paddle1_pos+PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score2 += 1
    if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if paddle2_pos <= ball_pos[1] <= (paddle2_pos+PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            spawn_ball(LEFT)
            score1 += 1
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    canvas.draw_circle(ball_pos, BALL_RADIUS, 0.1, "White", "White")
    
    if 0 <= (paddle1_pos + paddle1_vel) <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if 0 <= (paddle2_pos + paddle2_vel) <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    canvas.draw_line([PAD_WIDTH / 2, paddle1_pos],[PAD_WIDTH / 2, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH / 2, paddle2_pos],[WIDTH- PAD_WIDTH / 2, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_text(str(score1), (185, 40), 40, "White")
    canvas.draw_text(str(score2), (400, 40), 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 3
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
        
def game_restart():
    new_game()

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", game_restart, 100)

new_game()
frame.start()
