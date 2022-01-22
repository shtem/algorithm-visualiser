import pygame
import math
from queue import PriorityQueue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)

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

    def __lt__(self, other):
        return False


def h(n1, n2):
    # manhattan distance between 2 nodes n1 and n2
    x1, y1 = n1
    x2, y2 = n2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path() # make nodes on the path to the goal purple
        draw()

def algorithm(draw, grid, source, goal):
    # A* algorithm

    count = 0 # keep track of when we inserted each node in the queue, so we can break ties on nodes that have the same f score
    open_set = PriorityQueue()
    open_set.put((0, count, source)) # insert source node
    came_from = {} # keep track of what node we came from

    g_score = {node: float("inf") for row in grid for node in row} # keeps track of the shortest distance to get from source node to current node
    g_score[source] = 0
    f_score = {node: float("inf") for row in grid for node in row} # keeps track of predicted distance from current node to goal node
    f_score[source] = h(source.get_pos(), goal.get_pos()) # initial estimate of how far source node is from goal node

    open_set_hash = {source} # keep track of items that are in or not in the priority queue, initially has source node

    while not open_set.empty(): # while there's still nodes to explore/traverse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] # get node with minimum f score from open set to explore
        open_set_hash.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal, draw) # found goal node, make path
            goal.make_goal()
            return True 
        
        for neighbour in current.neighbours: # consider all neighbours of current node
            temp_g_score = g_score[current] + 1 # calculate new g score for neighbouring nodes using curent nodes g score

            if temp_g_score < g_score[neighbour]: # if new g score is less than neighbouring nodes current g score update their g score and calculate new f score
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), goal.get_pos())
                if neighbour not in open_set_hash: # if neighbouring node not in open set then put it in open set to explore
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        
        draw()

        if current != source: # explored current node, no longer in open set, so we can make it closed
            current.make_closed()

    return False # did not find a goal
            

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


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    source = None
    goal = None

    run = True

    while run:
        draw(win, grid, ROWS, width) # (re)draw screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                # left mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                # want to make sure the source and goal node are made first, once they're made left clicking creates a barrier
                if not source and node != goal:
                    source = node
                    source.make_source()
                if not goal and node != source:
                    goal = node
                    goal.make_goal()
                if node != source and node != goal:
                    node.make_obstacle()

            if pygame.mouse.get_pressed()[2]:
                # right mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset() # make node cube white
                
                # reset source and goal nodes
                if node == source:
                    source = None
                if node == goal:
                    goal = None
            
            if event.type == pygame.KEYDOWN: # start A* algorithm
                if event.key == pygame.K_SPACE and source and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, source, goal)
                
                if event.key == pygame.K_c: # clear screen
                    source = None
                    goal = None
                    grid = make_grid(ROWS, width)

    
    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)

