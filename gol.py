from time import sleep
from random import randint
import json
import os

# The rules:
# Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

SIZE = 42
SHOW_GENERATIONS = False
THRESHOLD = 15
MAX = (SIZE * 10)
CLOCK = 0.5


if SHOW_GENERATIONS:
    DEAD = '   '
    LIVE = '###'
else:
    DEAD = ' '
    LIVE = '@'
    

def generate_row(size):
    """
    Creates an empty row.
    """
    return [DEAD for i in range(size)]

def generate_board(size, seed=False):
    """
    Creates an empty board, optionally filling
    it with live cells.
    """
    board = [generate_row(size) for i in range(size)]
        
    # seed a glider
    # if seed:
    if False:
        board[1][3] = LIVE
        board[2][4] = LIVE
        board[3][2] = LIVE
        board[3][3] = LIVE
        board[3][4] = LIVE    

        
    if seed:
        # insert a random selection of LIVE cells
        how_many = 0
        for y in range(size):
            for x in range(size):
                if how_many < MAX:
                    randy = randint(0, 100)
                    if randy < THRESHOLD:
                        board[x][y] = LIVE
                        how_many = how_many + 1
    return board

def neighbors(cells, y, x):
    """
    Given a board and some coordinates,
    returns the neighbor cells.
    """
    neighbor_cells = []
    if x > 0:
        neighbor_cells.append(cells[y][x-1])

    if x < SIZE - 1:
        neighbor_cells.append(cells[y][x+1])        

    if y > 0:
        neighbor_cells.append(cells[y-1][x])

    if y < SIZE - 1:
        neighbor_cells.append(cells[y+1][x])

    if x > 0 and y > 0:
        neighbor_cells.append(cells[y-1][x-1])

    if x < SIZE - 1 and y < SIZE - 1:
        neighbor_cells.append(cells[y+1][x+1])

    if x > 0 and y < SIZE - 1:
        neighbor_cells.append(cells[y+1][x-1])

    if x < SIZE - 1 and y > 0:
        neighbor_cells.append(cells[y-1][x+1])

    return neighbor_cells

def is_live(cell):
    """
    Whether or not a cell contains a live
    entity, True or False.
    """
    return cell is LIVE

def live_neighbors(cells, y, x):
    """
    Returns the number of live neighbor cells.
    """
    return sum(1 for c in neighbors(cells, y, x) if is_live(c))

def has_under_population(live_neighbor_count):
    """
    If fewer than 2 live neighbors, True.
    Otherwise, False.
    """
    return live_neighbor_count < 2

def will_live_on(live_neighbor_count):
    """
    Has 2 or 3 live neighbors, True.
    Otherwise, False.
    """
    return live_neighbor_count == 2 or live_neighbor_count == 3

def has_over_population(live_neighbor_count):
    """
    Has more than 3 live neighbors, True.
    Otherwise, False.
    """
    return live_neighbor_count > 3

def will_reproduce(live_neighbor_count):
    """
    Has exactly 3 live neighbors, True.
    Otherwise, False.
    """
    return live_neighbor_count == 3

def print_board(cells):
    """
    Clears the screen, then prints
    the board.
    """
    os.system('clear')
    for row in cells:
        print(' '.join(row))

def game_loop(cells):
    """
    Repeatedly calculates the next generation
    of cells and prints cells to screen.

    Keeps count of how many generations.
    Ends when there is no more change.
    """
    gen_count = 0

    # Stringify the board for comparing generations.
    prev_gen = json.dumps(cells) 

    while True:
        gen_count = gen_count + 1

        # Keep next generation in a new board.
        new_cells = generate_board(SIZE)

        # Iterate through current board, calculating
        # birth/death for next generation.
        for y in range(len(cells)):
            for x in range(len(cells[y])):
                c = cells[y][x]
                count = live_neighbors(cells, y, x)
            
                if is_live(c):
                    if has_under_population(count):
                        new_cells[y][x] = DEAD

                    elif will_live_on(count):
                        new_cells[y][x] = cells[y][x]

                    elif has_over_population(count):
                        new_cells[y][x] = DEAD

                elif will_reproduce(count):
                    if SHOW_GENERATIONS:
                        new_cells[y][x] = str(gen_count)
                    else:
                        new_cells[y][x] = LIVE
                        
        # If no change from previous (or next previous) generation,
        # end the game loop.
        if cells == new_cells or prev_gen == json.dumps(new_cells):
            break
        else:
            prev_gen = json.dumps(cells)            
            cells = new_cells[:]
            print_board(cells)
            print("Generation: ", gen_count)            
            sleep(CLOCK)            
        
if __name__ == '__main__':
    game_loop(generate_board(SIZE, True))
