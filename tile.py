import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, width, height, col, row):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.col = col
        self.row = row

        self.rect = self.image.get_rect(left = self.col, top = self.row)