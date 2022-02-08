import pygame
import random
from math import dist
from queue import PriorityQueue
from resources.helper_funcs import reconstruct_path


def c(n1, n2):
    # x1, y1 = n1
    # x2, y2 = n2
    # return abs(x1 - x2) + abs(y1 - y2)
    # return random.randint(1,10)
    # return dist(n1, n2)
    return 1


def dijkstra_alg(draw, grid, source, goal):
    # Dijkstra's algorithm - unweighted: c(u,v) = 1, weighted: c(u,v) = distance heuristic

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, source))
    came_from = {}

    dist = {node: float("inf") for row in grid for node in row}
    dist[source] = 0

    open_set_hash = {source}

    while not open_set.empty():  # while there's still nodes to explore/traverse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal, draw)  # found goal node, make path
            goal.make_goal()
            return True

        for neighbour in current.neighbours:  # consider all neighbours of current node
            temp_dist = dist[current] + c(
                current.get_pos(), neighbour.get_pos()
            )  # calculate distance of current node from source node

            if temp_dist < dist[neighbour]:  # relaxation
                came_from[neighbour] = current
                dist[neighbour] = temp_dist
                if (
                    neighbour not in open_set_hash
                ):  # if neighbouring node not in open set then put it in open set to explore
                    count += 1
                    open_set.put((dist[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != source:  # explored current node, make it closed
            current.make_closed()

    return False  # did not find a goal
