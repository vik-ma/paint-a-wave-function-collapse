import pygame
import random
from tile import Tile
from button import Button

pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

ROWS = 100
COLS = 100
TILE_WIDTH = 4
TILE_HEIGHT = 4

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (175, 175, 175)
LIGHTGREY = (213, 213, 213)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_group = pygame.sprite.Group()

def draw_window():
    screen.fill(GREY)

sample_pixel_array = [
    (0,0,WHITE),(0,1,WHITE),(0,2,WHITE),(0,3,WHITE),
    (1,0,WHITE),(1,1,BLACK),(1,2,BLACK),(1,3,BLACK),
    (2,0,WHITE),(2,1,BLACK),(2,2,GREY),(2,3,BLACK),
    (3,0,WHITE),(3,1,BLACK),(3,2,BLACK),(3,3,BLACK),
    ]

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            tile = Tile(TILE_WIDTH, TILE_HEIGHT, (col * TILE_WIDTH + 50), (row * TILE_HEIGHT + 50), sample_pixel_array)
            tile_group.add(tile)
    tile_group.draw(screen)


def draw_tile():
    tile = Tile(TILE_WIDTH, TILE_HEIGHT, (0 * TILE_WIDTH + 50), (0 * TILE_HEIGHT + 50), sample_pixel_array)
    tile_group.add(tile)
    tile_group.draw(screen)

def rotate_pixel_array():
    pass
    


make_grid_button = Button(WHITE, 600, 50, 150, 40, "Make Grid", BLACK, LIGHTGREY)

def main():
    run = True

    is_grid_drawn = False

    while run:
        clock.tick(FPS)
        draw_window()
        pygame.draw.rect(screen, BLACK, (49, 49, COLS * TILE_WIDTH + 2, ROWS * TILE_HEIGHT + 2), 1)

        draw_tile()

        if is_grid_drawn:
            draw_grid()
        
        if make_grid_button.draw(screen):
            is_grid_drawn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()