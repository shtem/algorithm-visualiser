import pygame
from random import randint
from resources.const import GREY, WHITE, GRADIENTS, SIDE_PAD, TOP_PAD
from resources.node import Node


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()  # make nodes on the path to the goal purple
        draw()


def make_grid(rows, width):
    # make grid of nodes
    grid = []  # 2D array
    gap = width // rows
    for i in range(rows):
        grid.append([])  # each row is a list
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    # draw grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  # horizontal lines
        for j in range(rows):
            pygame.draw.line(
                win, GREY, (j * gap, 0), (j * gap, width)
            )  # vertical lines


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = randint(min_val, max_val)
        lst.append(val)

    return lst


def draw_list(draw_info, colour_pos={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:  # clear list portion of screen
        clear_rect = (
            SIDE_PAD // 2,
            TOP_PAD,
            draw_info.width - SIDE_PAD,
            draw_info.height - TOP_PAD,
        )
        pygame.draw.rect(draw_info.window, WHITE, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + (
            i * draw_info.block_width
        )  # x position we want to draw the block from
        y = (
            draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        )  # y position
        colour = GRADIENTS[i % 3]  # remainder always 0 1 2

        if (
            draw_info.width - SIDE_PAD // 2
        ) <= x:  # if x position goes off the side pads then stop drawing list blocks
            break

        if i in colour_pos:
            colour = colour_pos[i]

        pygame.draw.rect(
            draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height)
        )  # draws down

    if clear_bg:
        pygame.display.update()
        pygame.event.pump()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    # take the mouse position, divide by width of each node cube to get what position we are and what row we clicked on
    row = y // gap
    col = x // gap

    return row, col


def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]
