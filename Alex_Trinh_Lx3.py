'''
Alex Trinh
G01310551
SYST 230 Lab Lx3
'''

import turtle as t
from random import choice

WORLDSIZE = 250
STEPSIZE = 5
CENTERS = (-200, 0), (200, 0)

'''
Draws a square with the given size
around a given starting point (i.e. center parameter).
Use given pen object from turtle or the turtle module as default
'''
def draw_world(size, center=(0, 0), pen=t):
    # Lift the pen up
    pen.penup()

    # Get the lower left corner of the world as a starting point
    start_x = center[0] - size / 2
    start_y = center[1] - size / 2

    # Move the turtle to the starting point
    pen.goto(start_x, start_y)

    # Drop the pen to start drawing
    pen.pendown()

    # Draw the square by going straight and then turn left 90 degrees
    for _ in range(4):
        pen.forward(size)
        pen.left(90)

    # Move the turtle back to the center starting position
    pen.penup()
    pen.goto(center[0], center[1])

'''
Implements a single step in the random walk.
Move the given pen (default is turtle module) by
given step_size (default is global STEPSIZE) in a randomly
chosen direction i.e. North, South, East or West
'''
def step(step_size=STEPSIZE, pen=t):
    # All possible east, north, west, south
    directions = [0, 90, 180, 270]

    # Draw the line in that direction
    pen.pendown()
    pen.setheading(choice(directions))
    pen.forward(step_size)

'''
This is a generator function that iteratively invokes step
with given step size s and pen parameters to implement the random walk
until a boundary is reached.
The boundary box is defined by the parameters xll, yll, xul, yul
i.e. lower limit and upper limit, x y coordinates respectively"""
'''
def gen_walker(s, pen, xll, yll, xul, yul):
    while True:
        x = pen.xcor()
        y = pen.ycor()
        #if the turtle is not within the correct x and y ranges of the upper and lower limits then break
        if not (xll <= x <= xul and yll <= y <= yul):
           break
        step(s, pen)
        yield

'''
For a square of given size and center returns the coordinates
of the bottom left and top right corners as a 4-tuple in order
xll, yll, xul, yul respectively i.e. lower limit and upper limit coordinates"""
'''
def get_limits(size, center):
    #calculate the half step
    half_size = size / 2

    #Calculates all of the half steps in each direction for the boundary to be tested
    x_center, y_center = center
    xll = x_center - half_size
    yll = y_center - half_size
    xul = x_center + half_size
    yul = y_center + half_size
    return xll, yll, xul, yul


def main():
    """GIVEN AS PART OF TEMPLATE DO NOT CHANGE"""
    t.bgcolor("#252525")
    t.title('2D RANDOM WALK WITH ENHANCEMENTS')

    # Create pens based on number of worlds
    pens = [t.Turtle('turtle') for _ in CENTERS]
    cols = 'green', 'gold'
    for i, p in enumerate(pens):
        p.color(cols[i % 2])

    # Draw world and create Walker generators
    walkers = []
    for center, pen in zip(CENTERS, pens):
        draw_world(WORLDSIZE, center, pen)
        limits = get_limits(WORLDSIZE, center)
        # Create and append a walker generator to walkers list
        walkers.append(gen_walker(STEPSIZE, pen, *limits))

    # PAUSE FOR DRAMA
    t.textinput("ENTER TO CONTINUE", "SERIOUSLY PRESS <ENTER>")

    # Loop moves each walker in walkers list by 1 step iteratively
    # A walker is removed from the list if it reaches the world boundary
    # i.e. when a StopIteration exception is triggered
    while walkers:
        for w in walkers[:]:  # Using [:] to create a copy of walkers list
            try:
                next(w)
            except StopIteration:
                walkers.remove(w)


if __name__ == '__main__':
    main()
    t.exitonclick()