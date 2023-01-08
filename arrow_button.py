import pygame

class ArrowButton():
    def __init__(self, color, x, y, width, height, arrow_color, hover_color, *, is_pointing_up):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hover_color = hover_color
        self.arrow_color = arrow_color

        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.arrow_offset = 4
        if is_pointing_up:
            self.arrow_coords = ((self.x + self.arrow_offset, self.y + self.height - self.arrow_offset), (self.x + self.width / 2, self.y + self.arrow_offset), (self.x + self.width - self.arrow_offset, self.y + self.height - self.arrow_offset))
        else:
            self.arrow_coords = ((self.x + self.arrow_offset, self.y + self.arrow_offset), (self.x + self.width / 2, self.y + self.height - self.arrow_offset), (self.x + self.width - self.arrow_offset, self.y + self.arrow_offset))
        

    def draw(self, surface):
        action = False
        pygame.draw.rect(surface, self.color, self.rect)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        pygame.draw.polygon(surface, self.arrow_color, self.arrow_coords)
        #Border
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1)

        return action