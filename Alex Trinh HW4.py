'''
Alex Trinh
G01310551
SYST 230 HW4
'''

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import QTimer
from utils import Screen, CellularAutomata

class GameOfLifeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conway's Game of Life: Glider")
        self.setGeometry(100, 100, 800, 600)
        self.playing = False
        self.play_counter = 0
        self.user_pattern = []  # To save the user's starting pattern

        self.initUI()
        self.init_game()

    def initUI(self):
        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)  # Main layout is horizontal

        # Control panel on the left
        control_layout = QVBoxLayout()  # Vertical layout for controls
        main_layout.addLayout(control_layout, 1)  # Add control layout to main layout

        # Create Screen and CellularAutomata
        self.screen = Screen()
        self.ca = CellularAutomata(self.screen)

        # Control buttons
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.toggle_play_pause)
        control_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_game)
        control_layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_game)
        control_layout.addWidget(self.reset_button)

        # Generation counter
        self.gen_counter_label = QLabel(f"Gen: {self.play_counter}", self)
        control_layout.addWidget(self.gen_counter_label)

        # Game area on the right
        game_layout = QVBoxLayout()  # Vertical layout for the game area
        main_layout.addLayout(game_layout, 3)  # Add game layout to main layout
        game_layout.addWidget(self.screen)  # Add the Screen to the game layout

        # Timer for playing game
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_game)

        # Signals for mouse events
        self.screen.onclick.connect(self.handle_click)

    def toggle_play_pause(self):
        if not self.playing:
            self.play_button.setText("Pause")
            self.playing = True
            self.timer.start(1000)  # Update every second
        else:
            self.play_button.setText("Play")
            self.playing = False
            self.timer.stop()

    def stop_game(self):
        self.play_button.setText("Play")
        self.playing = False
        self.timer.stop()
        if self.user_pattern:
            self.ca.grid = [row[:] for row in self.user_pattern]  # Restore user's saved pattern
        else:
            self.init_game()  # Default to initial setup if no user pattern is saved
        self.screen.draw_grid(self.ca.grid)

    def reset_game(self):
        self.play_button.setText("Play")
        self.playing = False
        self.timer.stop()
        self.init_game()  # Initialize with the default glider pattern

    def play_game(self):
        self.ca.apply_rules()
        self.play_counter += 1
        self.gen_counter_label.setText(f"Gen: {self.play_counter}")

    def init_game(self):
        self.play_counter = 0
        self.gen_counter_label.setText(f"Gen: {self.play_counter}")
        self.user_pattern = [[0 for _ in range(self.ca.ncols)] for _ in range(self.ca.nrows)]
        self.ca.grid = [row[:] for row in self.user_pattern]  # Start with a blank grid
        self.ca.add_pattern((7, 1), (6, 2), (6, 3), (7, 3), (8, 3))  # Add default glider
        self.user_pattern = [row[:] for row in self.ca.grid]  # Save as user's starting pattern
        self.screen.draw_grid(self.ca.grid)  # Redraw the grid

    def handle_click(self, position):
        if not self.playing:
            r, c = position
            if 0 <= r < self.ca.nrows and 0 <= c < self.ca.ncols:
                # Toggle the clicked cell status
                self.ca.grid[r][c] = 1 if self.ca.grid[r][c] == 0 else 0
                self.user_pattern = [row[:] for row in self.ca.grid]  # Update user's starting pattern
                self.screen.draw_grid(self.ca.grid)
        else:
            QMessageBox.information(self, "Game In Progress", "Please pause the game before editing the grid.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOfLifeApp()
    ex.show()
    sys.exit(app.exec())
