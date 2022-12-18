import pygame


class InfoBox():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self, surface):
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1)

