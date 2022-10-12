import pygame
import random
from tile import Tile

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
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, pygame.Rect((col * TILE_SIZE + 50), (row * TILE_SIZE + 50), TILE_SIZE, TILE_SIZE))

def draw_tile():
    asd = Tile(BLACK, 16, 16, 600, 20)
    tile_group.add(asd)
    tile_group.draw(screen)

def main():
    run = True
    while run:
        clock.tick(FPS)
        draw_window()
        draw_grid()
        draw_tile()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()