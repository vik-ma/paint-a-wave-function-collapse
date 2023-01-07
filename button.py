import pygame


class Button():
    def __init__(self, color, x, y, width, height, text, text_color, hover_color, *, small_text=False, big_text=False, hover_box=None, hover_box_group=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.font = pygame.font.SysFont('Arial Bold', 27)
        self.font = pygame.font.SysFont('Arial Bold', 25)
        self.text = text
        self.text_color = text_color
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover_color = hover_color
        self.has_hover_box = False
        if small_text:
            self.font = pygame.font.SysFont('Arial Bold', 16)
        if big_text:
            self.font = pygame.font.SysFont('Arial Bold', 32)
        if hover_box is not None:
            self.hover_box = hover_box
            self.hover_box_group = hover_box_group
            self.is_showing_hover_box = False
            self.has_hover_box = True

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
            if self.has_hover_box:
                self.hover_box.update_image(pos[0], pos[1])
                self.hover_box_group.add(self.hover_box)
                self.is_showing_hover_box = True
        else:
            if self.has_hover_box and self.is_showing_hover_box:
                self.hover_box_group.remove(self.hover_box)
                self.is_showing_hover_box = False

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
                
        surface.blit(button_text, button_text_rect)
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1) # Border

        return action