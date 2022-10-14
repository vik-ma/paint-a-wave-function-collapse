import pygame


class Button():
    def __init__(self, color, x, y, width, height, text, text_color):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial Bold', 27)
        self.text = text
        self.text_color = text_color


    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)

        button_text = self.font.render(self.text, True, self.text_color)
        button_text_rect = button_text.get_rect(center = (self.x+self.width/2, self.y+self.height/2))
        surface.blit(button_text, button_text_rect)
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1) # Border