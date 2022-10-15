import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, width, height, col, row):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        # self.image.fill(color)

        pixel_array = pygame.PixelArray(self.image)

        pixel_array[0:width, 0:height] = color
        pixel_array[1, 1] = (0,0,0)
        pixel_array[1, 2] = (0,0,0)
        pixel_array[1, 3] = (0,0,0)
        pixel_array[2, 1] = (0,0,0)
        pixel_array[3, 1] = (0,0,0)
        pixel_array.close()


        self.col = col
        self.row = row

        self.rect = self.image.get_rect(left = self.col, top = self.row)

