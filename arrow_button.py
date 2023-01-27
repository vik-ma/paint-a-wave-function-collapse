import pygame

class ArrowButton():
    """
    This is a class for the GUI buttons with arrows on them in the pygame application.
      
    Attributes:
        color (tuple): Background color of the button in RGB format.
        x (int): X-position of the button.
        y (int): Y-position of the button.
        width (int): Width of the button.
        height (int): Height of the button.
        foreground_color (tuple): Arrow color of the button in RGB format.
        clicked (bool): Bool to represent whether or not the button is clicked.
        rect (pygame.Rect): Pygame Rect object for rendering and collision detection.
        hover_color (tuple): Background color of the button when mouse is hovering over in RGB format.
        arrow_offset (int): Offset to calculate where arrow is drawn on button in relation to the x or y coordinates of button.
        arrow_coords (tuple): X, Y, and Z coordinates for the arrow polygon that is drawn on the button. 
    
    Methods:
        draw(self, surface)
            Draws the button on the pygame surface and returns True if button is clicked. 
    """
    def __init__(self, color, x, y, width, height, foreground_color, hover_color, *, is_pointing_up):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.foreground_color = foreground_color
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover_color = hover_color
        self.arrow_offset = 4
        if is_pointing_up:
            # Create upwards pointing arrow
            self.arrow_coords = ((self.x + self.arrow_offset, self.y + self.height - self.arrow_offset), (self.x + self.width / 2, self.y + self.arrow_offset), (self.x + self.width - self.arrow_offset, self.y + self.height - self.arrow_offset))
        else:
            # Create downwards pointing arrow
            self.arrow_coords = ((self.x + self.arrow_offset, self.y + self.arrow_offset), (self.x + self.width / 2, self.y + self.height - self.arrow_offset), (self.x + self.width - self.arrow_offset, self.y + self.arrow_offset))
        
    def draw(self, surface) -> bool:
        action = False
        pygame.draw.rect(surface, self.color, self.rect)

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            # If mouse hovers over the button
            pygame.draw.rect(surface, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                # If Button is being left-clicked
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False

        # Arrow Triangle
        pygame.draw.polygon(surface, self.foreground_color, self.arrow_coords)
        # Button Border
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1)

        return action