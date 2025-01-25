'''
Alex Trinh
G01310551
SYST 230
Lab 7
'''

import tkinter as tk
import turtle
import random
from tkinter import ttk, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2D Random Walk")
        self.geometry("1024x768")

        # Reset variables
        self.reset_vars()

        # Create the widgets
        self.create_widgets()

    def reset_vars(self):
        # World and step parameters
        self.WORLDSIZE = 250
        self.STEPSIZE = 50
        self.NUM_WALKERS = 1

        # Initialize states
        self.total_step = [0, 0, 0, 0]
        self.walkers = []
        self.playing = False
        self.state = 'init'

    def show_warning(self):
        messagebox.showwarning("Warning", "STEP SIZE must be a multiple of WORLD SIZE! Change either value.")

    def create_widgets(self):
        self.settings_frame = tk.Frame(self)
        self.settings_frame.pack(fill=tk.X, padx=5, pady=5)

        # Use the grid geometry manager
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.settings_frame.grid_columnconfigure(2, weight=1)
        self.settings_frame.grid_columnconfigure(3, weight=1)
        self.settings_frame.grid_columnconfigure(4, weight=1)

        # Number of Worlds
        number_of_worlds_label = tk.Label(self.settings_frame, text="Number of Worlds:")
        number_of_worlds_label.grid(row=0, column=0, sticky='w')
        self.number_of_worlds_var = tk.IntVar(value=1)
        self.number_of_worlds_combo = ttk.Combobox(self.settings_frame,
                                                   textvariable=self.number_of_worlds_var,
                                                   values=[1, 2, 3, 4],
                                                   state="readonly")
        self.number_of_worlds_combo.grid(row=0, column=1, sticky='w')
        self.number_of_worlds_combo.bind("<<ComboboxSelected>>", self.combobox_selected)

        # World Size
        world_size_label = tk.Label(self.settings_frame,
                                    text="World Size:")
        world_size_label.grid(row=0, column=2, sticky='w')
        self.world_size_entry = tk.Entry(self.settings_frame)
        self.world_size_entry.insert(0, 250)
        self.world_size_entry.grid(row=0, column=3, sticky='w')

        # Step Size
        step_size_label = tk.Label(self.settings_frame,
                                    text="Step Size:")
        step_size_label.grid(row=0, column=4, sticky='w')
        self.step_size_entry = tk.Entry(self.settings_frame)
        self.step_size_entry.grid(row=0, column=5, sticky='w')
        self.step_size_entry.insert(0, 5)

        # Control frame
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Start button
        self.toggle_button = tk.Button(self.control_frame,
                                      text = "Play",
                                      command = self.toggle_play_pause,
                                      font = ("Arial", 14))
        self.toggle_button.grid(row=0, column=0, padx=10)

        # Stop button
        self.stop_button = tk.Button(self.control_frame,
                                     text="Stop",
                                     command=self.stop_simulation,
                                     font=("Arial", 14))
        self.stop_button.grid(row=0, column=2, padx=10)

        # Reset button
        self.reset_button = tk.Button(self.control_frame,
                                      text="Reset",
                                      command=self.reset_simulation,
                                      font=("Arial", 14))
        self.reset_button.grid(row=0, column=3, padx=10)

        # Create a label for step counters
        self.step_counter_label = tk.Label(self.control_frame,
                                           text="Step Counters:     ")
        self.step_counter_label.grid(row=0, column=4, padx=10)

        # Create a frame for the turtle canvas
        self.turtle_frame = tk.Frame(self)
        self.turtle_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Turtle canvas and embed it in the Tkinter frame
        self.canvas = tk.Canvas(self.turtle_frame, width=1024, height=768)
        self.canvas.pack(fill=tk.BOTH, expand=True)


        # Create a Turtle screen and set its background color
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.screensize(1024, 768)
        # Turn off animation for instant updates
        self.turtle_screen.tracer(0)

    def combobox_selected(self, event):
        print(f"Combobox selected: {self.number_of_worlds_combo.get()}")
        self.NUM_WALKERS = int(self.number_of_worlds_combo.get())


    def toggle_play_pause(self):
        # Toggle the playing state
        self.playing = not self.playing

        if self.state == 'init':
            self.WORLDSIZE = int(self.world_size_entry.get())
            self.STEPSIZE = int(self.step_size_entry.get())

            if (self.WORLDSIZE % self.STEPSIZE == 0):
                self.init_turtle()
                self.state = 'play'
            else:
                self.show_warning()

        # Update the button text based on the new state
        if self.playing:
            self.toggle_button.config(text="Pause")
            self.state = 'pause'
        else:
            self.toggle_button.config(text="Play")
            self.state = 'play'

        # Move the turtle(s)
        self.move_turtle()

    def stop_simulation(self):
        # Stop playing
        self.playing = False

        print("Stop simulation")
        self.init_turtle()

        # Reset the Play button
        self.toggle_button.config(text="Play")
        self.state = 'play'

    def update_step_counters(self):
        print("Update step counters")


    def reset_simulation(self):
        print("Reset simulation")
        # Clear the canvas
        self.turtle_screen.clear()

        # Reset the buttons
        self.toggle_button.config(text="Play", state=tk.ACTIVE)
        self.reset_vars()

    def draw_world(self, size, center=(0, 0), pen=turtle):
        """Draws a square with the given size
         around a given starting point (i.e. center parameter).
         Use given pen object from turtle or the turtle module as default"""
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


    def step(self, step_size=None, pen=turtle):
        """Implements a single step in the random walk.
        Move the given pen (default is turtle module) by
        given step_size (default is global STEPSIZE) in a randomly
        chosen direction i.e. North, South, East or West"""
        if step_size is None:
            step_size = self.STEPSIZE

        direction = random.choice(['N', 'S', 'E', 'W'])

        pen.pendown()

        if direction == 'N':
            pen.setheading(90)
        elif direction == 'S':
            pen.setheading(270)
        elif direction == 'E':
            pen.setheading(0)
        elif direction == 'W':
            pen.setheading(180)

        pen.forward(step_size)


    def gen_walker(self, s, pen, xll, yll, xul, yul):
        """This is a generator function that iteratively invokes step
        with given step size s and pen parameters to implement the random walk
        until a boundary is reached.
        The boundary box is defined by the parameters xll, yll, xul, yul
        i.e. lower limit and upper limit, x y coordinates respectively"""
        while True:
            pen.pendown()
            self.step(s, pen)
            x, y = pen.pos()
            if not (xll <= x <= xul and yll <= y <= yul):
                break
            yield


    def get_limits(self, size, center):
        """For a square of given size and center returns the coordinates
        of the bottom left and top right corners as a 4-tuple in order
        xll, yll, xul, yul respectively i.e. lower limit and upper limit coordinates"""
        half_size = size / 2
        xll = center[0] - half_size
        yll = center[1] - half_size
        xul = center[0] + half_size
        yul = center[1] + half_size
        return xll, yll, xul, yul


    def init_turtle(self):
        # Clear the canvas
        self.turtle_screen.clear()

        if self.NUM_WALKERS == 1:
            self.CENTERS = [(0, 0)]
        elif self.NUM_WALKERS == 2:
            self.CENTERS = [(-self.WORLDSIZE / 2, 0), (self.WORLDSIZE / 2, 0)]
        elif self.NUM_WALKERS == 3:
            self.CENTERS = [(self.WORLDSIZE / 2, self.WORLDSIZE / 2), (-self.WORLDSIZE / 2, self.WORLDSIZE / 2),
                       (-self.WORLDSIZE / 2, -self.WORLDSIZE / 2)]
        elif self.NUM_WALKERS == 4:
            self.CENTERS = [(self.WORLDSIZE / 2, self.WORLDSIZE / 2), (-self.WORLDSIZE / 2, self.WORLDSIZE / 2),
                       (-self.WORLDSIZE / 2, -self.WORLDSIZE / 2), (self.WORLDSIZE / 2, -self.WORLDSIZE / 2)]

        # Create pens based on number of worlds
        pens = [turtle.RawTurtle(self.turtle_screen) for _ in self.CENTERS]
        cols = 'green', 'gold', 'red', 'blue'
        for i, p in enumerate(pens):
            p.color(cols[i % 4])

        # Draw world and create Walker generators
        self.walkers = []
        for center, pen in zip(self.CENTERS, pens):
            self.draw_world(self.WORLDSIZE, center, pen)
            limits = self.get_limits(self.WORLDSIZE, center)
            # Create and append a walker generator to walkers list
            self.walkers.append(self.gen_walker(self.STEPSIZE, pen, *limits))

    def move_turtle(self):
        # Loop moves each walker in walkers list by 1 step iteratively
        # A walker is removed from the list if it reaches the world boundary
        # i.e. when a StopIteration exception is triggered
        if self.playing and self.state != 'finish':
            try:
                counter_str = ""
                for i, w in enumerate(self.walkers):
                    self.total_step[i] += 1
                    counter_str += f"Walker{i+1}: {self.total_step[i]}     "
                    next(w)
                self.step_counter_label.config(text=f"Step Counters:     {counter_str}")
                self.turtle_screen.update()
            except StopIteration:
                self.walkers.remove(w)

            if len(self.walkers) == 0:
                self.state = 'finish'
                self.toggle_button.config(state=tk.DISABLED)

            # Re-run the movement loop
            self.after(100, self.move_turtle())

if __name__ == "__main__":
    app = App()
    app.mainloop()