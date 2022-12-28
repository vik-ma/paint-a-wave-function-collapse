import pygame


class InfoText():
    def __init__(self, x, y, main_text, main_text_font, hover_box_text_font, hover_box_text, hover_box_width, hover_box_height, main_text_color):
        self.x = x
        self.y = y
        self.main_text = main_text
        self.hover_box_width = hover_box_width
        self.hover_box_height = hover_box_height
        self.main_text_font = main_text_font
        self.rect = pygame.Rect(self.x, self.y, self.main_text_font.size(main_text)[0], self.main_text_font.size(main_text)[1])
        self.render_main_text = self.main_text_font.render(main_text, True, main_text_color)
        self.hover_box_text_font = hover_box_text_font
        self.hover_box_text = []
        for text_line in hover_box_text:
            self.hover_box_text.append(self.hover_box_text_font.render(text_line, True, (0, 0, 0)))

        self.text_line_height = self.hover_box_text_font.get_linesize()


    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.render_main_text, (self.x, self.y))

        if self.rect.collidepoint(pos):
            hover_box_rect = pygame.Rect(pos[0], pos[1], self.hover_box_width, self.hover_box_height)
            pygame.draw.rect(surface, (255, 255, 255), hover_box_rect)

            for line_y_pos, text_line in enumerate(self.hover_box_text):
                hover_box_text_rect = text_line.get_rect(left = pos[0] + 14, top = (pos[1] + 8 + (line_y_pos * self.text_line_height)))
                surface.blit(text_line, hover_box_text_rect)

            pygame.draw.rect(surface, (0,0,0), (pos[0], pos[1], self.hover_box_width + 1, self.hover_box_height + 1), 1)

