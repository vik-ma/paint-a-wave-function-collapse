import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, width, height, col, row, pix_array):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        pixel_array = pygame.PixelArray(self.image)

        for i, pix_row in enumerate(pix_array):
            for j, pix in enumerate(pix_row):
                pixel_array[j,i] = pix
        pixel_array.close()

        self.image = pygame.transform.scale(self.image, ((width*10), (height*10)))        
        self.col = col
        self.row = row

        self.rect = self.image.get_rect(left = self.col, top = self.row)
