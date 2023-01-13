import pygame

class HoverBox(pygame.sprite.Sprite):
    def __init__(self, width, height, text, font):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.font = font
        self.text_line_height = self.font.get_linesize()
        self.text = []
        for text_line in text:
            self.text.append(self.font.render(text_line, True, (0, 0, 0)))
        
    def update_image(self, x, y):
        #Box
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,255,255))
        
        #Border
        pygame.draw.rect(self.image, (0,0,0), (0, 0, self.width, self.height), 1)
        
        #Text
        for line_y_pos, text_line in enumerate(self.text):
            hover_box_text_rect = text_line.get_rect(left = 14, top = (8 + (line_y_pos * self.text_line_height)))
            self.image.blit(text_line, hover_box_text_rect)