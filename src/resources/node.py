import pygame
from resources.const import *

class Node:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.neighbours = []
        self.colour = WHITE

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_obstacle(self):
        return self.colour == BLACK

    def is_source(self):
        return self.colour == ORANGE

    def is_goal(self):
        return self.colour == CYAN

    def reset(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN
    
    def make_obstacle(self):
        self.colour = BLACK
    
    def make_source(self):
        self.colour = ORANGE
    
    def make_goal(self):
        self.colour = CYAN

    def make_path(self):
        self.colour = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        # only want to traverse nodes that we can reach, so only add neighbouring nodes that are not obstacles to the list
        self.neighbours = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self):
        return False