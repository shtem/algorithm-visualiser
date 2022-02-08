import pygame
from resources.const import ROWS, WIDTH, WHITE
from resources.helper_funcs import make_grid, draw_grid, get_clicked_pos
from algorithms.astar import a_star_alg
from algorithms.dijkstra import dijkstra_alg

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Algorithm Visualiser")


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


def main(win, width):
    grid = make_grid(ROWS, width)

    source = None
    goal = None
    run = True

    while run:
        draw(win, grid, ROWS, width)  # (re)draw screen

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
                node.reset()  # make node cube white

                # reset source and goal nodes
                if node == source:
                    source = None
                if node == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:  # start A* algorithm

                if event.key == pygame.K_a and source and goal:  # PRESS A = A STAR ALG
                    pygame.display.set_caption("A* Path Finding Algorithm")
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    a_star_alg(lambda: draw(win, grid, ROWS, width), grid, source, goal)

                if (
                    event.key == pygame.K_d and source and goal
                ):  # PRESS D = DIJKSTRA ALG
                    pygame.display.set_caption("Dijkstra's Path Finding Algorithm")
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    dijkstra_alg(
                        lambda: draw(win, grid, ROWS, width), grid, source, goal
                    )

                if event.key == pygame.K_c:  # clear screen
                    pygame.display.set_caption("Algorithm Visualiser")
                    source = None
                    goal = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
