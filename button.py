import pygame


class Button():
    """
    This is a class for the GUI buttons in the pygame application.
      
    Attributes:
        color (tuple): Background color of the button in RGB format.
        x (int): X-position of the button.
        y (int): Y-position of the button.
        width (int): Width of the button.
        height (int): Height of the button.
        font (pygame.font): Pygame font object to store font type and size.
        text (str): Text inside the button.
        foreground_color (tuple): Text color of the button in RGB format.
        clicked (bool): Bool to represent whether or not the button is clicked.
        rect (pygame.Rect): Pygame Rect object for rendering and collision detection.
        hover_color (tuple): Background color of the button when mouse is hovering over in RGB format.
        hover_box (HoverBox): HoverBox object to show a box with text when mouse is hovering over button (if present).
    
    Methods:
        draw(self, surface)
            Draws the button on the pygame surface and returns True if button is clicked. 
    """

    def __init__(self, color, x, y, width, height, text, foreground_color, hover_color, *, small_text=False, big_text=False, hover_box=None, hover_box_group=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial Bold', 25)
        self.text = text
        self.foreground_color = foreground_color
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover_color = hover_color
        self.has_hover_box = False
        if small_text:
            self.font = pygame.font.SysFont('Arial Bold', 16)
        if big_text:
            self.font = pygame.font.SysFont('Arial Bold', 32)
        if hover_box is not None:
            self.hover_box = hover_box
            self.hover_box_group = hover_box_group
            self.is_showing_hover_box = False
            self.has_hover_box = True

    def draw(self, surface):
        action = False
        pygame.draw.rect(surface, self.color, self.rect)
        button_text = self.font.render(self.text, True, self.foreground_color)
        button_text_rect = button_text.get_rect(center = (self.x+self.width/2, self.y+self.height/2))
       
        
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
            if self.has_hover_box:
                self.hover_box.update_image(pos[0], pos[1])
                self.hover_box_group.add(self.hover_box)
                self.is_showing_hover_box = True
        else:
            if self.has_hover_box and self.is_showing_hover_box:
                self.hover_box_group.remove(self.hover_box)
                self.is_showing_hover_box = False

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
                
        surface.blit(button_text, button_text_rect)
        pygame.draw.rect(surface, (0,0,0), (self.x, self.y, self.width + 1, self.height + 1), 1) # Border

        return action