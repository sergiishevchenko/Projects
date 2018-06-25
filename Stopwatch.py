'''
Stopwatch game
'''

import simplegui

IsRunning = False
Counter, GoodStop, TotalStop = 0, 0, 0

def format(t):
    D, t = t % 10, t / 10
    C, t = t % 10, t / 10
    B, A = t % 6, t / 6
    return str(A) + ":" + str(B) + str(C) + "." + str(D)

def score():
    return str(GoodStop) + "/" + str(TotalStop)
    
def start():
    global IsRunning
    timer.start()
    IsRunning = True

def stop():
    global IsRunning, GoodStop, TotalStop
    timer.stop()
    if IsRunning:
        TotalStop += 1
        if Counter % 10 == 0:
            GoodStop += 1
    IsRunning = False

def reset():
    global IsRunning, GoodStop, TotalStop, Counter
    timer.stop()
    IsRunning = False
    Counter, GoodStop, TotalStop = 0, 0, 0

def tick():
    global Counter
    Counter += 1

def draw(canvas):
    canvas.draw_text(format(Counter), [60, 85], 36, "White")
    canvas.draw_text(score(), [155, 25], 26, "Green")
    
frame = simplegui.create_frame("Stopwatch", 200, 150)

frame.add_button("Start", start, 120)
frame.add_button("Stop", stop, 120)
frame.add_button("Reset", reset, 120)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)

frame.start()
