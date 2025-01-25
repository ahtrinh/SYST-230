'''
Alex Trinh
G01310551
SYST 230 Lab 6
'''

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2D Random Walk UI Design")
        self.geometry("600x400")  # Adjusted window size for extra UI elements

        self.step_counters = {}  # Dictionary to hold step count labels
        self.create_widgets()

    def create_widgets(self):
        # Frame settings
        self.settings_frame = tk.Frame(self)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Control frame
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Settings label
        settings_label = tk.Label(self.settings_frame, text="Settings", font=("Arial", 16))
        settings_label.pack(pady=(10, 20))

        # Number of Worlds
        number_of_worlds_label = tk.Label(self.settings_frame, text="Number of Worlds:")
        number_of_worlds_label.pack()
        self.number_of_worlds_var = tk.IntVar(value=1)
        self.number_of_worlds_combo = ttk.Combobox(self.settings_frame, textvariable=self.number_of_worlds_var,
        state="readonly", values=[1, 2, 3, 4])

        self.number_of_worlds_combo.pack()

        # World Size
        world_size_label = tk.Label(self.settings_frame, text="World Size (Must be multiple of Step Size):")
        world_size_label.pack()
        self.world_size_entry = tk.Entry(self.settings_frame)
        self.world_size_entry.pack()

        # Step Size
        step_size_label = tk.Label(self.settings_frame, text="Step Size:")
        step_size_label.pack()
        self.step_size_entry = tk.Entry(self.settings_frame)
        self.step_size_entry.pack()

        '''
        Counter for turtles although implementation of lx4 code will be later but this is to show that this would exist
        '''
        for i in range(1, 5):  # Assuming up to 4 turtles
            counter_label = tk.Label(self.settings_frame, text=f"Turtle {i} Steps: 0")
            counter_label.pack()
            self.step_counters[i] = counter_label

        # Start button
        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(pady=10)

        # Pause button
        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause_simulation)
        self.pause_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(pady=10)

    def start_simulation(self):
        print("This will be later for lx7 when implementing code from lx4")

    def pause_simulation(self):
        print("wait for lx4 implement code")

    def stop_simulation(self):
        print("wait for lx4 implement code")

    def reset_simulation(self):
        print("wait for lx4 implement code")

    def update_step_counter(self, turtle_id, steps):
        """Update the step counter for a turtle."""
        if turtle_id in self.step_counters:
            self.step_counters[turtle_id].config(text=f"Turtle {turtle_id} Steps: {steps}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
