import pygame

pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_window():
    screen.fill((255,255,255))

def main():
    run = True
    while run:
        clock.tick(FPS)
        draw_window()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()