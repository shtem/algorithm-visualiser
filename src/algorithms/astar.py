import pygame
from queue import PriorityQueue
from resources.helper_funcs import reconstruct_path


def h(n1, n2):
    # manhattan distance between 2 nodes n1 and n2
    x1, y1 = n1
    x2, y2 = n2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_alg(draw, grid, source, goal):
    # A* algorithm

    count = 0  # keep track of when we inserted each node in the queue, so we can break ties on nodes that have the same f score
    open_set = PriorityQueue()
    open_set.put((0, count, source))  # insert source node
    came_from = {}  # keep track of what node we came from

    g_score = {
        node: float("inf") for row in grid for node in row
    }  # keeps track of the shortest distance to get from source node to current node
    g_score[source] = 0
    f_score = {
        node: float("inf") for row in grid for node in row
    }  # keeps track of predicted distance from current node to goal node
    f_score[source] = h(
        source.get_pos(), goal.get_pos()
    )  # initial estimate of how far source node is from goal node

    open_set_hash = {
        source
    }  # keep track of items that are in or not in the priority queue, initially has source node

    while not open_set.empty():  # while there's still nodes to explore/traverse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[
            2
        ]  # get node with minimum f score from open set to explore
        open_set_hash.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal, draw)  # found goal node, make path
            goal.make_goal()
            return True

        for neighbour in current.neighbours:  # consider all neighbours of current node
            temp_g_score = (
                g_score[current] + 1
            )  # calculate new g score for neighbouring nodes using curent nodes g score

            if (
                temp_g_score < g_score[neighbour]
            ):  # if new g score is less than neighbouring nodes current g score update their g score and calculate new f score
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(
                    neighbour.get_pos(), goal.get_pos()
                )
                if (
                    neighbour not in open_set_hash
                ):  # if neighbouring node not in open set then put it in open set to explore
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if (
            current != source
        ):  # explored current node, no longer in open set, so we can make it closed
            current.make_closed()

    return False  # did not find a goal
