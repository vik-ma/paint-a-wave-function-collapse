import pygame

class HoverBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font):
        pygame.sprite.Sprite.__init__(self)
        # self.x = x
        # self.y = y
        # self.width = width
        # self.height = height
        self.font = font

        self.text = []
        for text_line in text:
            self.text.append(self.font.render(text_line, True, (0, 0, 0)))

        self.text_line_height = self.font.get_linesize()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface([width, height])
        self.image.fill((255,255,255))
        # self.pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(self.image, (0,0,0), (x, y, width, height), 1)


    # def show(self, surface, x, y):
    #     rect = pygame.Rect(x, y, self.width, self.height)
    #     pygame.draw.rect(surface, (255, 255, 255), rect)

    #     for line_y_pos, text_line in enumerate(self.text):
    #         hover_box_text_rect = text_line.get_rect(left = x + 14, top = (y + 8 + (line_y_pos * self.text_line_height)))
    #         surface.blit(text_line, hover_box_text_rect)

    #     pygame.draw.rect(surface, (0,0,0), (x, y, self.width + 1, self.height + 1), 1)

