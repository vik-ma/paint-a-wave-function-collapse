import pygame


class InfoText():
    def __init__(self, x, y, main_text, font, hover_box_text, hover_box_width, hover_box_height):
        self.x = x
        self.y = y
        self.main_text = main_text
        self.hover_box_text = hover_box_text
        self.hover_box_width = hover_box_width
        self.hover_box_height = hover_box_height
        self.font = font
        self.rect = pygame.Rect(self.x, self.y, self.font.size(main_text)[0], self.font.size(main_text)[1])
        self.render_text = self.font.render(main_text, True, (0, 0, 0))

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.render_text, (self.x, self.y))

        if self.rect.collidepoint(pos):
            hover_box_rect = pygame.Rect(pos[0], pos[1], self.hover_box_width, self.hover_box_height)
            pygame.draw.rect(surface, (255, 255, 255), hover_box_rect)
            pygame.draw.rect(surface, (0,0,0), (pos[0], pos[1], self.hover_box_width + 1, self.hover_box_height + 1), 1)

