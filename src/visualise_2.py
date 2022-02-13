import pygame
import math
from resources.const import *
from resources.helper_funcs import generate_starting_list, draw_list
from algorithms.bubble_sort import bubble_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort

pygame.init()

class DrawInformation:
    FONT = pygame.font.SysFont("Helvitica", 30)
    LARGE_FONT = pygame.font.SysFont("Helvitica", 40)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualiser")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = math.ceil(
            (self.width - SIDE_PAD) / len(lst)
        )  # width of each block in list
        self.block_height = math.floor(
            (self.height - TOP_PAD) / (self.max_val - self.min_val)
        )  # height of each block in list
        self.start_x = SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(WHITE)

    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, PURPLE
    )
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, BLACK
    )
    draw_info.window.blit(
        controls, (draw_info.width / 2 - controls.get_width() / 2, 45)
    )

    sorting = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | Q = QuickSort | H = Heap Sort", 1, BLACK
    )
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()
    pygame.event.pump()


def main():
    run = True
    clock = pygame.time.Clock()

    n = 600
    min_val = 0
    max_val = 100

    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_generator = None
    sorting_alg_name = "Bubble Sort"

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(WIDTH, WIDTH, lst)

    while run:
        clock.tick(120)  # 120 fps

        if sorting:
            try:
                next(sorting_alg_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_alg_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:  # RESET SORTING LIST
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:  # START SORTING ALG
                sorting = True
                sorting_alg_generator = sorting_alg(draw_list, draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:  # ASCENDING
                ascending = True
            elif event.key == pygame.K_d and not sorting:  # DESCENDING
                ascending = False
            elif event.key == pygame.K_b and not sorting:  # BUBBLE SORT
                sorting_alg = bubble_sort
                sorting_alg_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:  # INSERTION SORT
                sorting_alg = insertion_sort
                sorting_alg_name = "Insertion Sort"
            elif event.key == pygame.K_q and not sorting:  # QUICKSORT
                sorting_alg = quick_sort
                sorting_alg_name = "QuickSort"
            elif event.key == pygame.K_h and not sorting:  # HEAP SORT
                sorting_alg = heap_sort
                sorting_alg_name = "Heap Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
