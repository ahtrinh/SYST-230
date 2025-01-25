"""
SYST 230: Mod 4- OO Programming
Lab 4: 2D Random Walk with Enhancements
Author: Alex Trinh
"""

import turtle as t
from random import choice

# World and step parameters and center
WORLDSIZE = 250
STEPSIZE = 5
CENTERS = (-200, 0), (200, 0)

'''
Data and methods for setting and drawing boundaries
for random walk
'''
class World:

    def __init__(self, size, center=(0, 0), pen=None):
        # World dimensions given by size x size
        self.size = size

        # Center of world
        self.center = center

        # Takes turtle object or creates if None is given
        self.pen = pen if pen else t.Turtle()

    def draw_world(self):
        """Draws a square with size given by world's size
        centered around worlds center point"""
        # Lift the pen up
        self.pen.penup()

        # Get the lower left corner of the world as a starting point
        start_x = self.center[0] - self.size / 2
        start_y = self.center[1] - self.size / 2

        # Move the turtle to the starting point
        self.pen.goto(start_x, start_y)

        # Drop the pen to start drawing
        self.pen.pendown()

        # Draw the square by going straight and then turn left 90 degrees
        for _ in range(4):
            self.pen.forward(self.size)
            self.pen.left(90)

        # Move the turtle back to the center starting position
        self.pen.penup()
        self.pen.goto(self.center[0], self.center[1])

    def get_limits(self):
        """Return coordinates of the world's bottom left
        and top right corners as a 4-tuple in order xll, yll, xul, yul
          respectively i.e. lower limit and upper limit coordinates"""
        #calculate the half step
        half_size = self.size / 2

        #Calculates all of the half steps in each direction for the boundary to be tested
        x_center, y_center = self.center
        xll = x_center - half_size
        yll = y_center - half_size
        xul = x_center + half_size
        yul = y_center + half_size
        return xll, yll, xul, yul

class Walker:
    """Data and methods for implementing and tracing a Random walk"""

    def __init__(self, step_size, world, color=None, pen=None, **pen_attributes):
        """:param step_size: Distance taken by walker each step
        :param world: A reference to the walker's world
        :param color: Color of the walker's turtle
        :param pen: A reference to Turtle object for tracing steps in the walk
            if no pen is given the given World object's pen is used instead
        :param pen_attributes: Optional parameters such as speed to be set on
            the Walker's pen at initialization"""
        # Assign the step size attribute of the Walker object to the value passed as step_size
        self.step_size = step_size

        # Assign the world attribute of the Walker object to the World object passed as world
        self.world = world

        # Assign the pen attribute of the Walker object to the pen object passed as pen.
        # If no pen object is provided, use the pen object associated with the Walker's world.
        self.pen = pen if pen else self.world.pen
        if pen_attributes:
            self.pen.set(**pen_attributes)
        if color:
            self.pen.color(color)

        # Set the shape of the Walker's pen to a turtle shape
        self.pen.shape("turtle")
    def step(self):
        """Implements a single step in the random walk.
        Walker's Pen is moved by step_size in a randomly chosen direction
        i.e. either North, South, East or West """
        # All possible east, north, west, south
        directions = [0, 90, 180, 270]

        # Draw the line in that direction
        self.pen.pendown()
        self.pen.setheading(choice(directions))
        self.pen.forward(self.step_size)

    def next_step(self):
        """First invokes get_limits method of walker's world object
        If walker's pen coordinates are within the given limits
            the step method is invoked. The method must return True
            in this case i.e. the Walker is still within bounds.
        Otherwise, the function must return false (i.e. step is not invoked in this case) """
        xll, yll, xul, yul = self.world.get_limits()
        x, y = self.pen.position()
        heading = self.pen.heading()

        # Calculate the change in x and y based on the heading
        if 0 <= heading < 90:
            dx = self.step_size
            dy = self.step_size * (heading / 90)
        elif 90 <= heading < 180:
            dx = -self.step_size * ((180 - heading) / 90)
            dy = self.step_size
        elif 180 <= heading < 270:
            dx = -self.step_size
            dy = -self.step_size * ((270 - heading) / 90)
        else:
            dx = self.step_size * ((360 - heading) / 90)
            dy = -self.step_size

        # This will calculate the next position
        next_x, next_y = x + dx, y + dy

        # This checks if the next position is within the world boundaries or near them
        if (xll <= next_x <= xul and yll <= next_y <= yul) or \
                (abs(next_x - xll) < self.step_size / 2 or abs(next_x - xul) < self.step_size / 2) or \
                (abs(next_y - yll) < self.step_size / 2 or abs(next_y - yul) < self.step_size / 2):
            self.step()
            return True
        return False
def main():
    """GIVEN AS PART OF TEMPLATE DO NOT CHANGE"""
    t.bgcolor("#252525")
    t.title('2D RANDOM WALK WITH ENHANCEMENTS')

    # Initialize Worlds and Walkers
    colors = 'green', 'gold'
    worlds = [World(WORLDSIZE, c) for c in CENTERS]
    walkers = [Walker(STEPSIZE, w, color=c) for w, c in zip(worlds, colors)]

    # Draw world boundaries
    for w in worlds:
        w.draw_world()

    # PAUSE FOR DRAMA
    t.textinput("ENTER TO CONTINUE", "SERIOUSLY PRESS <ENTER>")

    while walkers:
        for w in walkers:
            if not w.next_step():  # done walking if next_step returns false/None
                walkers.remove(w)


if __name__ == '__main__':
    main()
    t.exitonclick()