import pygame
from const import GREY, WHITE
from node import Node

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path() # make nodes on the path to the goal purple
        draw()

def make_grid(rows, width):
    # make grid of nodes
    grid = [] # 2D array
    gap = width // rows
    for i in range(rows):
        grid.append([]) # each row is a list
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def draw_grid(win, rows, width):
    # draw grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # vertical lines


def draw(win, grid, rows, width):
    # draw the whole screen
    win.fill(WHITE)

    # draw all of the nodes in the grid
    for row in grid:
        for node in row:
            node.draw(win)
    
    # draw grid lines
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    # take the mouse position, divide by width of each node cube to get what position we are and what row we clicked on
    row = y // gap
    col = x // gap

    return row, col