import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

ROWS = 10
COLS = 10
TILE_SIZE = 50

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (175, 175, 175)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_window():
    screen.fill(GREY)

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, pygame.Rect((col * TILE_SIZE + 50), (row * TILE_SIZE + 50), TILE_SIZE, TILE_SIZE))

def main():
    run = True
    while run:
        clock.tick(FPS)
        draw_window()
        draw_grid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()