import pygame


class Button():
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial Bold', 25)
        self.text = text


    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)

        button_text = self.font.render("You win!", True, (255,0,0))
        button_text_rect = button_text.get_rect(center = (self.x+self.width/2, self.y+self.height/2))
        surface.blit(button_text, button_text_rect)