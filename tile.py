import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, pix_array, enlargement_scale):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        pixel_array = pygame.PixelArray(self.image)

        for i, pix_row in enumerate(pix_array):
            for j, pix in enumerate(pix_row):
                pixel_array[j,i] = pix
        pixel_array.close()

        self.image = pygame.transform.scale(self.image, ((width*enlargement_scale), (height*enlargement_scale)))        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = self.image.get_rect(left = self.x, top = self.y)
