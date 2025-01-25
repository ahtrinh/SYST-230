import turtle as t
import random

world_size = 500
step_size = 5

def draw_world(size):
    t.penup()
    t.goto(-size // 2, -size // 2)
    t.pendown()

    for i in range(4):
        t.forward(size)
        t.left(90)
    t.penup()
    t.home()
    t.pendown()

def step(step_size):
    cardinal_directions= ['north', 'south', 'east', 'west']
    dir = random.choice(cardinal_directions)

    if dir == 'north':
        t.setheading(90)
    elif dir == 'south':
        t.setheading(270)
    elif dir == 'east':
        t.setheading(0)
    elif dir == 'west':
        t.setheading(180)

    t.forward(step_size)

def walk(limit):
    while abs(t.xcor()) < limit and abs(t.ycor()) < limit:
        step(step_size)

def main():
    draw_world(world_size)
    walk(world_size // 2)
    t.done()
    
main()