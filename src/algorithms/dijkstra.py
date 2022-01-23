import pygame
from queue import PriorityQueue
from resources.helper_funcs import reconstruct_path

def dijkstra_alg(draw, grid, source, goal):
    # Dijkstra's algorithm

    count = 0 
    open_set = PriorityQueue()
    open_set.put((0, count, source)) 
    came_from = {} 

    g_score = {node: float("inf") for row in grid for node in row} 
    g_score[source] = 0

    open_set_hash = {source} 

    while not open_set.empty(): # while there's still nodes to explore/traverse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] 
        open_set_hash.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal, draw) # found goal node, make path
            goal.make_goal()
            return True 
    

        draw()

        if current != source: # explored current node, make it closed
            current.make_closed()

    return False # did not find a goal