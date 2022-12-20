import pygame


class InfoText():
    def __init__(self, x, y, main_text, hover_box_text, hover_box_width, hover_box_height):
        self.x = x
        self.y = y
        self.main_text = main_text
        self.hover_box_text = hover_box_text
        self.hover_box_width = hover_box_width
        self.hover_box_height = hover_box_height

    def show(self, surface):
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1)

