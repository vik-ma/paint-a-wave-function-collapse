import pygame

class TileButton():
    """
    This is a class for Tiles that are clickable like buttons in the pygame application.
      
    Attributes:
        x (int): X-position of the clickable Tile.
        y (int): Y-position of the clickable Tile.
        width (int): Width of the clickable Tile.
        height (int): Height of the clickable Tile.
        image (pygame.Surface): Pygame Surface object to render Tile in GUI.
        rect (pygame.Rect): Pygame Rect object for rendering and collision detection.
        clicked (bool): Bool to represent whether or not the Tile is clicked.
    
    Methods:
        draw(self, surface)
            Draws the button on the pygame surface and returns True if Tile is clicked. 
   
    """
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface) -> bool:
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # If TileButton is being left-clicked
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw TileButton
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # TileButton Border
        pygame.draw.rect(surface, (0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)

        return action