"""
SYST 230: HW1
Author: Alex Trinh
"""

import turtle as t

CELL_SIZE = 50
NUM_ROWS, NUM_COLS = 10, 10
t.speed(100)

'''
Uses turtle to draw a 10x10 grid, with cell size 50
Cells are colored or plain based on the cell state (i.e. alive or dead)
given in the grid parameter (i.e. a nested list)
'''
def draw_grid(grid: list[list]):
    t.speed(100)

    # For loop for each row in the grid
    for row in range(len(grid)):

        # Loop through each column in the row
        for col in range(len(grid[row])):

            # Calculate the (x,y) coordinate of the current cell
            x = col * CELL_SIZE - (CELL_SIZE * NUM_COLS / 2)
            y = row * CELL_SIZE - (CELL_SIZE * NUM_ROWS / 2)

            # Lift pen
            t.penup()

            # Turtle Moves to (x,y) coordinate
            t.goto(x, y)

            # Start drawing with pen down
            t.pendown()

            # This determines fill color of cell if alive or dead
            if grid[row][col] == 1:

                # If cell is alive turn it into a black color
                t.fillcolor("black")
            else:

                #If cell is dead, turn it into a white color
                t.fillcolor("white")

            # Fill the cell with the specific color
            t.begin_fill()
            for i in range(4):
                t.forward(CELL_SIZE)
                t.right(90)
            # End filling cell
            t.end_fill()
    # Hides the turtle after drawing the grid
    t.hideturtle()

'''
Given row and column indices (i.e. r and c) and the CA's state (i.e. grid)
Returns a count of living neighbors of the cell referenced by the given
indices in the grid i.e. cell at grid[r][c]
NB: Boundary cells will have fewer than 8 neighbors"""
'''
def count_neighbors(r: int, c: int, grid: list[list]) -> int:
    # Define changes in row and column indices for neighboring cells
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1),(0, 1), (1, -1), (1, 0),  (1, 1)]

    # Initialize count of living neighbors
    living_neighbors = 0

    # Loop through the neighbors to check neighboring cells
    for row_offset, col_offset in neighbors:
        # Calculate the coordinates of the neighbor cell
        neighbor_row = r + row_offset
        neighbor_col = c + col_offset

        # Check if the neighbor cell is within the bounds of the grid
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):
            # Checks if the neighbor cell is alive
            if grid[neighbor_row][neighbor_col] == 1:
                living_neighbors += 1

    return living_neighbors

'''
Given the current state of the CA (i.e. grid) applies
the rules of the Game of life to each cell in the grid,
by invoking the count_neighbors function and returns a
new grid with state values for the next generation
HINT: Copy grid into a new_grid (USE deepcopy from copy module),
make changes to new_grid based on old grid and return new_grid
'''
def apply_rules(grid: list[list]) -> list:
    # Get the dimensions of the grid
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Create a new grid to store the next generation
    new_grid = []

    # Loop through each row in the grid
    for r in range(num_rows):
        # Initialize a new row
        new_row = []

        # Loop through each column in the row
        for c in range(num_cols):
            # Count the number of living neighbors for the current cell
            living_neighbors = count_neighbors(r, c, grid)

            # Apply the rules of the Game of Life
            if grid[r][c] == 1:
                # Any live cell with fewer than 2 or more than 3 live neighbors dies
                if living_neighbors < 2 or living_neighbors > 3:
                    new_row.append(0)
                else:
                    # Any live cell with 2 or 3 live neighbors survives
                    new_row.append(1)
            else:
                # Any dead cell with exactly 3 live neighbors is turned alive
                if living_neighbors == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)

        # This adds the new row to the new grid
        new_grid.append(new_row)

    return new_grid

'''
Given the state of the CA, (i.e. grid) and a list of
coordinates specifying indices for living cells set cells in grid
referenced by indices to ALIVE"""
'''
def add_pattern(grid: list[list], *living: tuple[int, int]):
    for row, col in living:
        grid[row][col] = 1

def draw_title(text):
    erase_title()
    # Move the turtle to the title position
    t.penup()
    t.goto(0, 280)
    t.hideturtle()

    # Write the new title
    t.write(text, align="left", font=("Arial", 16, "bold"))

def erase_title():
    # Move the turtle to the starting position to cover the old title
    t.penup()
    t.goto(0, 300)
    t.setheading(0)  # Ensure the turtle is facing right
    t.pendown()

    # Set the color to the background color and start filling
    t.fillcolor("white")
    t.begin_fill()
    for i in range(2):
        t.forward(220)
        t.right(90)
        t.forward(20)
        t.right(90)
    t.end_fill()

    t.penup()

'''
Program execution start point:
Initialize 10x10 CA grid with zeroes i.e. all dead
Invoke add_pattern function passing grid, and living cell indices
Ex: Assuming the bottom left cell is referenced by (0, 0) then
for Glider pattern living indices are -> (7, 1), (6, 2), (6, 3), (7, 3), (8, 3)
Iteratively:
Invoke draw_grid passing grid
Invoke apply_rules passing current grid and store return value in grid variable"""
'''
def main():
    # Initialize the grid with zeroes which is all dead cells
    grid = [[0] * NUM_COLS for i in range(NUM_ROWS)]

    # This adds the Glider Pattern form the PDF
    add_pattern(grid, (7, 1), (6, 2), (6, 3), (7, 3), (8, 3))

    # Draw the initial state of the grid
    draw_grid(grid)

    for i in range(5):
        # Apply the rules to generate the next generation
        grid = apply_rules(grid)
        draw_title(f"SHAPE={(i % 4) + 1} GENERATION={i + 1}")
        # Draw the current state of the grid
        draw_grid(grid)


if __name__ == '__main__':
    t.title("Conway's Game of Life: Glider")
    main()
    t.mainloop()