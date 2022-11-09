import pygame

class PaintTile(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface, *, border=False):
            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                
            surface.blit(self.image, (self.rect.x, self.rect.y))
            if border:
                pygame.draw.rect(surface, (0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)

            return action