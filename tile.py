import pygame

class Tile(pygame.sprite.Sprite):
    """
    This is a class for the Base Tiles that gets painted and ultimately extracted for patterns for the WFC algorithm.

    Attributes:
        x (int): X-position of the Tile.
        y (int): Y-position of the Tile.
        width (int): Width of the Tile.
        height (int): Height of the Tile.
        image (pygame.Surface): Pygame Surface object to render Tile in GUI.
        pix_array (list): Two dimensonal array storing color data for every position in the Tile.
        rect (pygame.Rect): Pygame Rect object for rendering tile onto screen.
    """
    def __init__(self, width, height, x, y, pix_array, enlargement_scale):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.pix_array = pix_array

        # Place every color in pix_array at corresponding X and Y position
        for i, row in enumerate(self.pix_array):
            for j, color in enumerate(row):
                self.image.set_at((i, j), color)

        # Scale up every pixel in tile by amount defined by enlargement_scale
        self.image = pygame.transform.scale(self.image, ((self.width*enlargement_scale), (self.height*enlargement_scale)))        
        self.rect = self.image.get_rect(left = self.x, top = self.y)
