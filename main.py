import pygame
import random
from tile import Tile
from button import Button

pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

ROWS = 30
COLS = 30
TILE_SIZE = 16

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (175, 175, 175)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_group = pygame.sprite.Group()

def draw_window():
    screen.fill(GREY)

def draw_grid():
    pygame.draw.rect(screen, BLACK, (49, 49, COLS * TILE_SIZE + 2, ROWS * TILE_SIZE + 2), 1)
    for row in range(ROWS):
        for col in range(COLS):
            tile = Tile(WHITE, TILE_SIZE, TILE_SIZE, (col * TILE_SIZE + 50), (row * TILE_SIZE + 50))
            tile_group.add(tile)
            #pygame.draw.rect(screen, WHITE, pygame.Rect((col * TILE_SIZE + 50), (row * TILE_SIZE + 50), TILE_SIZE, TILE_SIZE))
    tile_group.draw(screen)


def draw_tile():
    tile = Tile(BLACK, 16, 16, 600, 16)
    tile_group.add(tile)
    tile_group.draw(screen)

def main():
    run = True
    while run:
        clock.tick(FPS)
        draw_window()
        draw_grid()
        asd = Button(WHITE, 600, 50, 150, 40, "Make Grid", BLACK)
        asd.draw(screen)
        # draw_tile()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()