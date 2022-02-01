import pygame
import random
import math
from resources.const import *
pygame.init()

class DrawInformation:
    BG_COL = WHITE
    SIDE_PAD = 100 # padding on each side of screen
    TOP_PAD = 150 # padding on the top of the screen
    FONT = pygame.font.SysFont('Helvitica', 30)
    LARGE_FONT = pygame.font.SysFont('Helvitica', 40)

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

        self.block_width = math.ceil((self.width - self.SIDE_PAD) / len(lst)) # width of each block in list
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) # height of each block in list
        self.start_x = self.SIDE_PAD // 2
    

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def draw_list(draw_info, colour_pos={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg: # clear list portion of screen
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BG_COL, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + (i * draw_info.block_width) # x position we want to draw the block from
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height # y position
        colour = GRADIENTS[i % 3] # remainder always 0 1 2

        if (draw_info.width - draw_info.SIDE_PAD//2) <= x: # if x position goes off the side pads then stop drawing list blocks
            break

        if i in colour_pos:
            colour = colour_pos[i]

        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height)) # draws down
    
    if clear_bg:
        pygame.display.update()
        pygame.event.pump()

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BG_COL)
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, PURPLE)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | Q = QuickSort | H = Heap Sort", 1, BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

    draw_list(draw_info)
    pygame.display.update()
    pygame.event.pump()

def bubble_sort(draw_info, ascending=True): # generator
    lst = draw_info.lst
    
    for i in range(len(lst) - 1): # execute n - 2 times, n = lenght of list
        for j in range(len(lst) - 1 - i): # compare adjacent values with each other
            num1 = lst[j]
            num2 = lst[j + 1]
            
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending): # if they are in the incorrect position swap them
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: GREEN, j + 1: RED}, True)
                yield True 
            # call this function for each swap, yield control back to function that called it instead of performing the whole algorithm, and wait to be called again
            # -> pause the execution of the function, then resume it -> saves state from when it yielded from last time
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)): # first element is in sorted subset 
        curr = lst[i] # select a number from list so we can insert it in the correct position by swapping

        while True:
            ascending_sort = i > 0 and lst[i - 1] > curr and ascending # if ascending we want to check if current number is less than previous number so we can swap
            descending_sort = i > 0 and lst[i - 1] < curr and not ascending # if descending we want to check if current number is greater than previous number so we can swap

            if not ascending_sort and not descending_sort:
                break # if both these conditions are not true we break, don't swap

            # swap current number with previous number
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = curr
            draw_list(draw_info, {i - 1: GREEN, i: RED}, True)
            yield True
    
    return lst

def partition(draw_info, lst, start, end, ascending=True):
    rand_pivot = random.randrange(start, end) # random pivot point chosen
    lst[end], lst[rand_pivot] = lst[rand_pivot], lst[end] # place pivot element at end of the list

    pivot = lst[end] 
    pIndex = start

    for i in range(start, end): # for each element that is not the pivot
        curr = lst[i]

        if (curr <= pivot and ascending) or (curr >= pivot and not ascending): # if current element is in the incorrect position then move element to the correct side of pivot
            lst[i], lst[pIndex] = lst[pIndex], lst[i]
            draw_list(draw_info, {i: GREEN, pIndex: RED}, True)
            pIndex += 1
    
    lst[pIndex], lst[end] = lst[end], lst[pIndex]
    draw_list(draw_info, {end: ORANGE, pIndex: RED}, True)

    return pIndex

def quick_sort_aux(draw_info, lst, start, end, ascending=True):
    if start < end:
 
        # pIndex is partitioning index, lst[p] is at correct position
        pIndex = partition(draw_info, lst, start, end, ascending)
 
        # Separately sort elements before partition and after partition
        yield from quick_sort_aux(draw_info, lst, start, pIndex - 1, ascending)
        yield from quick_sort_aux(draw_info, lst, pIndex + 1, end, ascending)
    
    yield True

def quick_sort(draw_info, ascending=True):
    # randomised quicksort

    lst = draw_info.lst
    start = 0
    end = len(lst) - 1

    yield from quick_sort_aux(draw_info, lst, start, end, ascending)
    
    return lst

def sift_down(draw_info, lst, i, upper, ascending=True):
    # sift the new first element, i, to its appropriate index in the heap - mantains max/min heap property

    # i = parent/root element
    # upper = upper bound index of list = n

    while(True):
        l, r = 2*i+1, 2*i+2 # indexes of left and right children

        if max(l, r) < upper: # if there are 2 children then children's indices have to be smaller than upper bound to be valid
            if (lst[i] >= max(lst[l], lst[r]) and ascending) or (lst[i] <= min(lst[l], lst[r]) and not ascending): # if parent node is greater/less than child nodes don't need to swap
                break 
            elif (lst[l] > lst[r] and ascending) or (lst[l] < lst[r] and not ascending): # if left child largest/smallest swap left child with parent
                lst[l], lst[i] = lst[i], lst[l]
                draw_list(draw_info, {i: GREEN, l: RED}, True)
                i = l 
            else: # else right child largest/smallest swap right child with parent
                lst[r], lst[i] = lst[i], lst[r] 
                draw_list(draw_info, {i: GREEN, r: RED}, True)
                i = r
        elif l < upper: # if there is one child that child is a left node then it's index has to be smaller than upperbound to be valid
            if (lst[l] > lst[i] and ascending) or (lst[l] < lst[i] and not ascending):
                lst[l], lst[i] = lst[i], lst[l]
                draw_list(draw_info, {i: GREEN, l: RED}, True)
                i = l
            else:
                break
        elif r < upper: # if there is one child that child is a right node then it's index has to be smaller than upperbound to be valid
            if (lst[r] > lst[i] and ascending) or (lst[r] < lst[i] and not ascending):
                lst[r], lst[i] = lst[i], lst[r]
                draw_list(draw_info, {i: GREEN, r: RED}, True)
                i = r
            else:
                break
        else: # no children
            break

def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    # (n-2)//2 = index of very last parent
    for i in range((n-2)//2, -1, -1): # heapify
        sift_down(draw_info, lst, i, n, ascending)
        yield True
    
    for end in range(n-1, 0, -1): # sort list
        lst[0], lst[end] = lst[end], lst[0]
        draw_list(draw_info, {0: GREEN, end: ORANGE}, True)
        sift_down(draw_info, lst, 0, end, ascending)
        yield True
    
    return lst


def main():
    run = True 
    clock = pygame.time.Clock()

    n = 700
    min_val = 0
    max_val = 200

    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_generator = None
    sorting_alg_name = "Bubble Sort"
    
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    while run:
        clock.tick(120) # 120 fps

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

            if event.key == pygame.K_r: # RESET SORTING LIST
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False: # START SORTING ALG
               sorting = True
               sorting_alg_generator = sorting_alg(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting: # ASCENDING
               ascending = True
            elif event.key == pygame.K_d and not sorting: # DESCENDING
               ascending = False
            elif event.key == pygame.K_b and not sorting: # BUBBLE SORT
               sorting_alg = bubble_sort
               sorting_alg_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting: # INSERTION SORT
               sorting_alg = insertion_sort
               sorting_alg_name = "Insertion Sort"
            elif event.key == pygame.K_q and not sorting: # QUICKSORT
               sorting_alg = quick_sort
               sorting_alg_name = "QuickSort"
            elif event.key == pygame.K_h and not sorting: # HEAP SORT
               sorting_alg = heap_sort
               sorting_alg_name = "Heap Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
