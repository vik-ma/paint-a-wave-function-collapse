import pygame


class Button():
    def __init__(self, color, x, y, width, height, text, text_color, hover_color, *, small_text=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial Bold', 27)
        self.text = text
        self.text_color = text_color
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover_color = hover_color
        if small_text:
            self.font = pygame.font.SysFont('Arial Bold', 16)


    def draw(self, surface):
        action = False
        pygame.draw.rect(surface, self.color, self.rect)
        button_text = self.font.render(self.text, True, self.text_color)
        button_text_rect = button_text.get_rect(center = (self.x+self.width/2, self.y+self.height/2))
       
        
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
                
        surface.blit(button_text, button_text_rect)
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1) # Border

        return action