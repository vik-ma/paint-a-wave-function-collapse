import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, pix_array, enlargement_scale):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.pix_array = pix_array

        for i, row in enumerate(self.pix_array):
            for j, color in enumerate(row):
                self.image.set_at((i, j), color)

        self.image = pygame.transform.scale(self.image, ((width*enlargement_scale), (height*enlargement_scale)))        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pix_array = pix_array

        self.rect = self.image.get_rect(left = self.x, top = self.y)
