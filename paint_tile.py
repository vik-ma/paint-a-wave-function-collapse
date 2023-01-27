import pygame

class PaintTile(pygame.sprite.Sprite):
    """
    This is a class for clickable, single colored paint tiles in the GUI of the pygame application.
      
    Attributes:
        x (int): X-position of the tile.
        y (int): Y-position of the tile.
        width (int): Width of the tile.
        height (int): Height of the tile.
        color (tuple): Background color of the tile in RGB format.
        image (pygame.Surface): Pygame Surface object to render tile in GUI.
        rect (pygame.Rect): Pygame Rect object for rendering and collision detection.
        clicked (bool): Bool to represent whether or not the tile is clicked.

    Methods:
        draw(self, surface, *, border=False)
            Draws the tile on the pygame surface and returns True if button is clicked. 
            Also draws a black border around the tile if border parameter is True.
    """
    def __init__(self, width, height, x, y, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface, *, border=False) -> bool:
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # If PaintTile is being left-clicked
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        # Draw PaintTile
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # PaintTile Border
        if border:
            pygame.draw.rect(surface, (0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)

        return action