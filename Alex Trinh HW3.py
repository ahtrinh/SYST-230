'''
Alex Trinh
G01310551
SYST 230 HW3
'''

import tkinter as tk
import turtle
from hw2 import CellularAutomata, Pen

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set debugging level appropriately
        self.debug_level = 0

        # Game settings
        self.title("Conway's Game of Life: Glider")
        self.geometry("600x520")

        # Initialize the STM event
        self.event = 'START'

        # Initialize the gen counter
        self.play_counter = 0

        # Create the widgets
        self.create_widgets()

        # Initialize the game
        self.init_game()

        # Bind the mouse motion event to motion function to get (x,y) coordinates
        self.canvas.bind('<Motion>', self.motion)

        # Bind on clicking on world
        self.canvas.bind('<Button-1>', lambda event: self.window_click(event, self.canvas))
        self.canvas.focus_set()

    # Print debugging messages
    def debug(self, calling_method="", message=""):
        if self.debug_level:
            print(f"[{calling_method}][EV:{self.event}][ST:{self.state.upper()}] {message}")

    # Create the game widgets
    def create_widgets(self):
        # Control frame
        self.control_frame = tk.Frame(self, width=50)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Play/Pause toggle button
        self.toggle_button = tk.Button(self.control_frame,
                                      text = "Play",
                                      command = self.toggle_play_pause,
                                      font = ("Arial", 14))
        self.toggle_button.pack(side=tk.TOP, fill=tk.X)

        # Stop button
        self.stop_button = tk.Button(self.control_frame,
                                     text="Stop",
                                     command=self.stop_game,
                                     font=("Arial", 14))
        self.stop_button.pack(side=tk.TOP, fill=tk.X)

        # Reset button
        self.reset_button = tk.Button(self.control_frame,
                                      text="Reset",
                                      command=self.reset_game,
                                      font=("Arial", 14))
        self.reset_button.pack(side=tk.TOP, fill=tk.X)

        # Create a label for generation counter
        self.gen_counter_label = tk.Label(self.control_frame,
                                           text="Gen:     ")
        self.gen_counter_label.pack(side=tk.TOP, fill=tk.X)

        # Create a frame for the turtle canvas
        self.turtle_frame = tk.Frame(self)
        self.turtle_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a Turtle canvas and embed it in the Tkinter frame
        self.canvas = tk.Canvas(self.turtle_frame, width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a Turtle screen and set its background color
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.screensize(500, 500)
        # Turn off animation for instant updates
        self.turtle_screen.tracer(0)

    # Handle the play/pause game event
    def toggle_play_pause(self):
        self.debug("toggle_play_pause", "Current state...")
        if self.state == 'initial':
            self.debug("toggle_play_pause", "Need to execute tasks in INITIAL state...")
            self.toggle_button.config(text="Pause")
            self.state = 'playing'
            self.event = 'PLAY_BTN_CLICK'
            self.debug("toggle_play_pause", "Need to execute tasks in PLAYING state...")
        elif self.state in ['playing']:
            self.toggle_button.config(text="Play")
            self.state = 'paused'
            self.event = 'PAUSE_BTN_CLICK'
            self.debug("toggle_play_pause", "Need to execute tasks in PAUSED state...")
        elif self.state in ['paused']:
            self.toggle_button.config(text="Pause")
            self.state = 'playing'
            self.event = 'PLAY_BTN_CLICK'
            self.debug("toggle_play_pause", "Need to execute tasks in PLAYING state...")

        self.play_game()

    # Handle the stop game event
    def stop_game(self):
        # Stop playing
        self.toggle_button.config(text="Play")
        self.event = 'STOP_BTN_CLICK'
        self.state = 'initial'

        # Set the focus to the canvas
        self.canvas.focus_set()

        self.debug("stop_game", "Need to execute tasks in the INITIAL state...")
        self.init_game()

        # Bind the mouse motion event to motion function to get (x,y) coordinates
        self.canvas.bind('<Motion>', self.motion)

        # Bind on clicking on world
        self.canvas.bind('<Button-1>', lambda event: self.window_click(event, self.canvas))
        self.canvas.focus_set()

    # Handle the game reset event
    def reset_game(self):
        # Reset the toggle button
        self.toggle_button.config(text="Play")
        self.event = 'RESET_BTN_CLICK'
        self.state = 'initial'

        # Set the focus to the canvas
        self.canvas.focus_set()

        # Initialize the game
        self.init_game()

        # Bind the mouse motion event to motion function to get (x,y) coordinates
        self.canvas.bind('<Motion>', self.motion)

        # Bind on clicking on world
        self.canvas.bind('<Button-1>', lambda event: self.window_click(event, self.canvas))
        self.canvas.focus_set()

    # Play the game!
    def play_game(self):
        if self.state == 'playing':
            self.play_counter += 1
            self.debug('play_game', f"Play game = {self.play_counter}")

            # Move the turtle(s)
            self.ca.apply_rules()

            # Update the gen counter
            self.gen_counter_label.config(text=f"Gen: {self.play_counter}")

            # Repeat after time delay
            self.after(1000, self.play_game)

    # Initialize the game
    def init_game(self):
        # Reset gen counter
        self.play_counter = 0

        # Update the gen counter
        self.gen_counter_label.config(text=f"Gen: {self.play_counter}")

        # Reset the state
        self.state = 'initial'

        # Instantiate the turtle graphics
        if self.event in ['START', 'RESET_BTN_CLICK']:
            # Instantiate the game of life
            self.ca = CellularAutomata(pen=Pen(screen=self.turtle_screen))

            # Clear the canvas
            self.turtle_screen.clear()

            # Create the glider
            self.ca.add_pattern((7, 1), (6, 2), (6, 3), (7, 3), (8, 3))  # start with glider

    # Handle mouse movement event for selecting cells
    def motion(self, event):
        # Set map limits
        min_value = 0
        max_value = 9

        # Restrict to the limits
        def restrict_to_range(value):
            if value < min_value:
                return min_value
            elif value > max_value:
                return max_value
            else:
                return value

        # Get the mouse coordinates
        x,y = event.x, event.y

        # Convert the mouse coordinates to map coordinates
        self.rel_x = 9 - y//50
        self.rel_y = x//50

        # Restrict the coordinates
        self.map_x = restrict_to_range(self.rel_x)
        self.map_y = restrict_to_range(self.rel_y)
        #print(f"[({x},{y})] -> ({self.map_x},{self.map_y})")

    # Handle mouse click event for selecting cells
    def window_click(self, event, canvas):
        # Set the focus on the canvas so the mouse will register clicks
        canvas.focus_set()

        # Only allow setting of the initial state of the cellular automata when not in a playing state
        if self.state != 'playing':
            # Toggle the cell in the map
            live_status = self.ca.grid[self.map_x][self.map_y]

            # Toggle live/dead cell
            if live_status == 0:
                new_status = 1
            else:
                new_status = 0

            # Update the map
            self.ca.grid[self.map_x][self.map_y] = new_status
            self.ca.draw_grid()


if __name__ == "__main__":
    app = App()
    app.mainloop()