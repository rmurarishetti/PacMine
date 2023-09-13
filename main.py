import random
import time
import threading
from turtle import *
import colorsys

## Interface ##
## function to generate field
def gen_field(size):
    n = (size*2+1)
    f = [0]*n
    for i in range(n):
        f[i] = [0]*n

    for y in range(1,n,2):
        for x in range(1,n,2):
            f[y][x] = 2
    return f

def walk(field, start):
    size = len(field)
    prev = []
    while field[truestart[0]][truestart[1]] != 1 or start != truestart :
        steps = [[start[0]-2,start[1]], [start[0]+2,start[1]], [start[0],start[1]-2], [start[0],start[1]+2]]
        remove = []
        for step in steps:
            if step[0] < 1 or step[0] >= size-1:
                remove.append(step)
            elif step[1] < 1 or step[1] >= size-1:
                remove.append(step)
        for r in remove:
            steps.remove(r)
        open = []
        for i in steps:
            if field[i[0]][i[1]] == 1:
                open.append(i)
        if len(open) == len(steps):
            field[start[0]][start[1]] = 1
            start = prev[-1]
            prev.remove(start)

        else:
            for k in open:
                steps.remove(k)
            dir = random.randint(0,len(steps)-1)
            next = steps[dir]
            u = [start[0]-2,start[1]]
            d = [start[0]+2,start[1]]
            l = [start[0],start[1]-2]
            r = [start[0],start[1]+2]
            ## draw the line from start - next
            if next == u:
                field[next[0]+1][next[1]] = 1
            elif next == d:
                field[next[0]-1][next[1]] = 1
            elif next == l:
                field[next[0]][next[1]+1] = 1
            else:
                field[next[0]][next[1]-1] = 1

            field[start[0]][start[1]] = 1
            prev.append(start)
            start = next
    return field

def display(field):
    for y in range(len(field)):
        for x in range(len(field)):
            print(field[y][x], end = ' ')
        print()

## knock walls:
def knock_walls(field):
    size = len(field)
    walls = []
    for y in range(1, size-1):
        for x in range(1, size-1):
            if field[y][x] == 0:
                walls.append([y,x])
    used = []
    count = 0
    while count < size + (size//2):
        index = random.randint(0,len(walls)-1)
        if index not in used:
            used.append(index)
            wall = walls[index]
            field[wall[0]][wall[1]] = 1
            count += 1
    return field

truestart = [1,1]

def gen_and_draw_map(t, truestart):
    map = gen_field(10)
    map = walk(map, truestart)
    map = knock_walls(map)
    draw_map(t, map)
    return map

## draw map on turtle
def draw_square(t, x, y):
    t.up()
    t.goto(x*12,-y*12)
    t.down()
    t.begin_fill()
    for i in range(4):
        t.forward(12)
        t.right(90)
    t.end_fill()

def draw_map(t,field):
    t.color('black')
    for y in range(len(field)):
        for x in range(len(field)):
            if field[y][x] == 0:
                draw_square(t, x, y)

def game_start():
    style = ('Courier', 120)
    style2 = ('Courier', 20)
    h_blue = 0.51 # constant: hue value of yellow green color.
    V_DARK = 0.2 # constant: brightness value of initial dark state
    V_BRIGHT = 1 # constant: brightness value of the brightest state
    v = V_BRIGHT
    wn.bgcolor('black')
    firefly.clear() # clear the current drawing
    score.clear()
    color = colorsys.hsv_to_rgb(h_blue,1,v) # use colorsys to convert HSV to RGB color
    firefly.color(color)
    firefly.penup()
    firefly.goto(2,-180)
    firefly.pendown()
    firefly.write('PAC-MINE\n', font=style, align='center')
    firefly.write('Please stand by', font=style2, align='center')
    # should_draw = False # just finished drawing, set should_draw to False # draw forever
    wn.update()
    time.sleep(5)

def game_over():
    global dead
    dead = True
    title.clear()
    title.write("Game over", font=("Arial", 18, "normal"))
    done()

def game_end():
    style = ('Courier', 120)
    style2 = ('Courier', 20)
    h_blue = 0.51 # constant: hue value of yellow green color.
    V_DARK = 0.2 # constant: brightness value of initial dark state
    V_BRIGHT = 1 # constant: brightness value of the brightest state
    v = V_BRIGHT
    wn.clear()
    wn.bgcolor('black')
     # clear the current drawing
    color = colorsys.hsv_to_rgb(h_blue,1,v) # use colorsys to convert HSV to RGB color
    firefly.color(color)
    firefly.penup()
    firefly.goto(2,-180)
    firefly.pendown()
    firefly.write('GAMEOVER\n', font=style, align='center')
    firefly.write(f"Score: {str(SCORE)} \n" , font = style2, align = 'center')
    firefly.write('Thank you for playing!', font=style2, align='center')
    # should_draw = False # just finished drawing, set should_draw to False # draw forever
    update()
    time.sleep(3)
    bye()

## Spawning ##
def spawn_items(field, num):
    size = len(field)
    paths = []
    for y in range(1, size-1):
        for x in range(1, size-1):
            if field[y][x] == 1:
                paths.append([y,x])
    items = []
    for i in range(num):
        x = random.randint(0,len(paths)-1)
        if paths[x] not in items:
            items.append(paths[x])
    return items

dead = False
def spawn_mines():
    global dead
    if dead:
        return
    global mines_pos
    global mines
    mines.clear()
    for i in mines_pos:
        map[i[0]][i[1]] = 1
    mines_pos = spawn_items(map, 12)
    for mine in mines_pos:
        map[mine[0]][mine[1]] = 2
        x = mine[1]*12 + 6
        y = -mine[0]*12 - 6
        mines.up()
        mines.goto(x,y)
        mines.dot(10, 'red')
    wn.ontimer(spawn_mines, 5000)

## Movement ##
def coord_convert(x,y):
    x = round((x-6)/12)
    y = round(-(y+6)/12)
    return [y,x]

def turtle_point(coord):
    x = coord[1]*12 + 6
    y = -(coord[0]*12) - 6
    return [x,y]
    
speed = 1
def pacman_travel(): # loops by itself using recursion
    if abs(ghost.position() - pacman.position()) < 12:
        game_over()
    else:
        if ghost.heading() == 0:
            valid = validate_right_move(ghost)
        elif ghost.heading() == 90:
            valid = validate_up_move(ghost)
        elif ghost.heading() == 180:
            valid = validate_left_move(ghost)
        else:
            valid = validate_down_move(ghost)

        if valid:
            ghost.clear()
            ghost.forward(1)
            ghost.dot(12, 'blue')

        else:
            for i in range(5):
                ghost.clear()
                ghost.forward(1)
                ghost.dot(12, 'blue')
            moves = []
            if validate_right_move(ghost):
                moves.append(0)
            if validate_up_move(ghost):
                moves.append(90)
            if validate_left_move(ghost):
                moves.append(180)
            if validate_down_move(ghost):
                moves.append(270)

            next = random.randint(0,len(moves)-1)
            ghost.setheading(moves[next])

    bool_valid = True
    if pacman.heading() == 0:
        if int(pacman.position()[0]) % 12 == 6:
            bool_valid = validate_right_move(pacman)
    elif pacman.heading() == 90:
        if pacman.position()[1] % 12 == 6:
            bool_valid = validate_up_move(pacman)
    elif pacman.heading() == 180:
        if pacman.position()[0] % 12 == 6:
            bool_valid = validate_left_move(pacman)
    elif pacman.heading() == 270:
        if pacman.position()[1] % 12 == 6:
            bool_valid = validate_down_move(pacman)

    if bool_valid:
        pacman.clear()
        pacman.forward(speed)
        pacman.dot(12, 'yellow')
        x, y = pacman.position()
        coord = coord_convert(x,y)
        if map[coord[0]][coord[1]] == 2:
            global start_time
            if abs(int(start_time - time.time())) % 5 != 1:
                game_over()

    wn.ontimer(pacman_travel, 10)

def validate_right_move(t):
    x, y = t.position()
    coord = coord_convert(x,y)
    coord[1] = coord[1] + 1
    if map[coord[0]][coord[1]] == 0:
        return False
    else:
        return True

def validate_up_move(t):
    x, y = t.position()
    coord = coord_convert(x,y)
    coord[0] = coord[0] - 1
    if map[coord[0]][coord[1]] == 0:
        return False
    else:
        return True

def validate_left_move(t):
    x, y = t.position()
    coord = coord_convert(x,y)
    coord[1] = coord[1] - 1
    if map[coord[0]][coord[1]] == 0:
        return False
    else:
        return True

def validate_down_move(t):
    x, y = t.position()
    if y%12 < 6:
        y = y - y%12
    coord = coord_convert(x,y)
    coord[0] = coord[0] + 1
    if map[coord[0]][coord[1]] == 0:
        return False
    else:
        return True

def pacman_movement():
    wn.onkeypress(lambda: turning(90), 'Up')
    wn.onkeypress(lambda: turning(180), 'Left')
    wn.onkeypress(lambda: turning(0), 'Right')
    wn.onkeypress(lambda: turning(270), 'Down')
    wn.onkeypress(lambda: game_end(), 'Escape')

def turning(nextheading):
    if abs(nextheading-pacman.heading()) == 180:
        pacman.setheading(nextheading)
    else:
        x,y = pacman.position()
        if nextheading == 0:
            if validate_right_move(pacman):
                pacman.setheading(nextheading)
        elif nextheading == 180:
            if validate_left_move(pacman):
                pacman.setheading(nextheading)
        elif nextheading == 90:
            if validate_up_move(pacman):
                pacman.setheading(nextheading)
        else:
            if validate_down_move(pacman):
                pacman.setheading(nextheading)

## Game rules ##
b = False
start_time = time.time()
def countdown_timer():
    global score
    global SCORE
    global start_time
    global dead
    while dead == False and b == False:
        min, seconds = divmod(time.time() - start_time, 60)
        timer = f"{round(min )} min {round(seconds)-5} sec"
        timer_title.clear()
        timer_title.write(timer, font=('Arial',10,'normal'))
        time.sleep(1)

    SCORE = round(min)*60 + round(seconds) - 5
    style = ('Courier', 120)
    style2 = ('Courier', 20)
    h_blue = 0.51 # constant: hue value of yellow green color.
    V_DARK = 0.2 # constant: brightness value of initial dark state
    V_BRIGHT = 1 # constant: brightness value of the brightest state
    v = V_BRIGHT
    #wn.clear(
    wn.bgcolor('black')
    pacman.clear()
    ghost.clear()
    mines.clear()
     # clear the current drawing
    color = colorsys.hsv_to_rgb(h_blue,1,v) # use colorsys to convert HSV to RGB color
    firefly.color(color)
    firefly.penup()
    firefly.goto(2,-180)
    firefly.pendown()
    firefly.write('GAMEOVER\n', font=style, align='center')
    firefly.write(f"Score: {str(SCORE)} \n" , font = style2, align = 'center')
    firefly.write('''Press 'Esc' to quit''', font=style2, align='center')
    # should_draw = False # just finished drawing, set should_draw to False # draw forever
    wn.update()

def fix_timer():
    timer_thread = threading.Thread(target = countdown_timer)
    timer_thread.start()

## Setup ##
wn = Screen()
# Initialise objects
firefly = Turtle()
firefly.hideturtle()
path = Turtle()
path.hideturtle()
pacman = Turtle()
pacman.hideturtle()
mines = Turtle()
mines.hideturtle()
title = Turtle()
title.hideturtle()
ghost = Turtle()
ghost.hideturtle()
score = Turtle()
score.hideturtle()
timer_title = Turtle()
timer_title.hideturtle()
tracer(False)
game_start()
firefly.clear()
wn.bgcolor("lightblue")
title.setposition(0,5)
title.write("Pacman game", font=('Arial', 18, 'normal'))
timer_title.setposition(180,5)
#generate map and starting position
map = gen_and_draw_map(path, truestart)
mines_pos = spawn_items(map, int(len(map)*0.4))
spawn_mines()
fix_timer()
ghost_pos = spawn_items(map,1)
while ghost_pos[0] == [1,1]:
    ghost_pos = spawn_items(map,1)
ghost.up()
ghost.goto(turtle_point(ghost_pos[0])[0],turtle_point(ghost_pos[0])[1])
ghost.dot(12, 'blue')
pacman.up()
pacman.goto(18,-18)
pacman.down()
pacman.dot(12,'yellow')
pacman.setheading(90)
listen()
pacman_movement()
pacman_travel()
wn.mainloop()