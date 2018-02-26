from pprint import pprint
from time import sleep
from random import randint
import os

# The rules:
# Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


SIZE = 42
DEAD = ' '
LIVE = '*'

THRESHOLD = (SIZE * 10) / 5
MAX = (SIZE * 20) / 2
CLOCK = 0.5

def generate_row(size):
    row = []
    for i in range(size):
        row.append(DEAD)
    return row

def generate_board(size, seed=False):
    board = []
    for i in range(size):
        board.append(generate_row(size))

    # add a glider

    board[0][1] = LIVE
    board[1][2] = LIVE
    board[2][0] = LIVE
    board[2][1] = LIVE
    board[2][2] = LIVE    

        
    if False:
        how_many = 0
        # insert a random selection of LIVE cells
        for y in range(size):
            for x in range(size):
                if how_many < MAX:
                    randy = randint(0, size * 10)
                    if randy < THRESHOLD:
                        board[x][y] = LIVE
                        how_many = how_many + 1
    return board

def neighbors(cells, x, y):
    neighbor_cells = []
    if x > 0:
        neighbor_cells.append(cells[x-1][y])

    if x < SIZE - 1:
        neighbor_cells.append(cells[x+1][y])        

    if y > 0:
        neighbor_cells.append(cells[x][y-1])

    if y < SIZE - 1:
        neighbor_cells.append(cells[x][y+1])

    if x > 0 and y > 0:
        neighbor_cells.append(cells[x-1][y-1])

    if x < SIZE - 1 and y < SIZE - 1:
        neighbor_cells.append(cells[x+1][y+1])

    if x > 0 and y < SIZE - 1:
        neighbor_cells.append(cells[x-1][y+1])

    if x < SIZE - 1 and y > 0:
        neighbor_cells.append(cells[x+1][y-1])

    return neighbor_cells

def is_live(cell):
    return cell is not DEAD

def live_neighbors(cells, x, y):
    lives = 0
    for c in neighbors(cells, x, y):
        if is_live(c):
            lives = lives + 1
    return lives

def has_under_population(live_neighbor_count):
    # if fewer than 2 live neighbors
    return live_neighbor_count < 2

def will_live_on(live_neighbor_count):
    # has 2 or 3 live neighbors
    return live_neighbor_count > 1 and live_neighbor_count < 4

def has_over_population(live_neighbor_count):
    # has more than 3 live neighbors
    return live_neighbor_count > 3

def will_reproduce(live_neighbor_count):
    # is dead and has exactly 3 live neighbors
    return live_neighbor_count == 3

def print_board(cells):
    for row in cells:
        print(' '.join(row))

def game_loop(cells):
    gen_count = 0
    while True:
        gen_count = gen_count + 1
        prev_gen = generate_board(SIZE)
        new_cells = generate_board(SIZE)
        # loop through all cells
        for y in range(len(cells)):
            for x in range(len(cells[y])):
                # calculating the next generation for a coord
                c = cells[x][y]
                count = live_neighbors(cells, x, y)
            
                if is_live(c):
                    if has_under_population(count):
                        new_cells[x][y] = DEAD
                        continue
                    elif will_live_on(count):
                        new_cells[x][y] = LIVE
                        continue
                    elif has_over_population(count):
                        new_cells[x][y] = DEAD
                        continue
                elif will_reproduce(count):
                    new_cells[x][y] = LIVE
        if cells == new_cells or prev_gen == new_cells:
            break
        else:
            prev_gen = cells[:]
            cells = new_cells[:]
            os.system('clear')
            print_board(cells)
            # input()

            print("Generation: ", gen_count)
            sleep(CLOCK)            
        
if __name__ == '__main__':
    game_loop(generate_board(SIZE, True))
