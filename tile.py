import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, width, height, col, row, pix_array):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        # self.image.fill(color)

        pixel_array = pygame.PixelArray(self.image)
        # pixel_array[0:width, 0:height] = color
        for pix in pix_array:
            pixel_array[pix[0],pix[1]] = pix[2]
        pixel_array.close()


        self.col = col
        self.row = row

        self.rect = self.image.get_rect(left = self.col, top = self.row)

