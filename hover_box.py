import pygame

class HoverBox(pygame.sprite.Sprite):
    def __init__(self, width, height, text, font):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.font = font
        self.text = []
        for text_line in text:
            self.hover_box_text.append(self.font.render(text_line, True, (0, 0, 0)))
        self.text_line_height = self.font.get_linesize()