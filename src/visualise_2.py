import pygame
import random
from resources.const import *
pygame.init()

class DrawInformation:
    BG_COL = WHITE
    SIDE_PAD = 100 # padding on each side of screen
    TOP_PAD = 150 # padding on the top of the screen

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

        self.block_width = round(self.width - self.SIDE_PAD / len(lst)) # width of each block in list
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) # height of each block in list
        self.start_x = self.SIDE_PAD // 2
    

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def draw(draw_info):
    draw_info.window.fill(draw_info.BG_COL)
    pygame.display.update()

def main():
    run = True 
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    while run:
        clock.tick(60) # 60 fps

        draw(draw_info)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    

    pygame.quit()



if __name__ == "__main__":
    main()
