import pygame


class InfoText():
    """
    This is a class for text in the GUI of the pygame application that has a HoverBox object attached to it.
      
    Attributes:
        x (int): X-position of the text.
        y (int): Y-position of the text.
        main_text (str): Text to be drawn in the GUI.
        main_text_font (pygame.font): Pygame font object to store font type and size.
        rect (pygame.Rect): Pygame Rect object for rendering and collision detection.
        render_main_text (pygame.Surface): Pygame Surface object to render text in GUI.
        hover_box (HoverBox): HoverBox object to show a box with text when mouse is hovering over text.
        hover_box_group (pygame.sprite.Group): Pygame Sprite Group that HoverBox is added to.
        is_showing_hover_box (bool): Bool to represent whether or not HoverBox is currently rendered on screen or not.

    Methods:
        draw(self, surface)
            Draws the text on the pygame surface and shows attached HoverBox object if mouse is hovering over text. 
    """
    def __init__(self, x, y, main_text, main_text_font, main_text_color, hover_box, hover_box_group):
        self.x = x
        self.y = y
        self.main_text = main_text
        self.main_text_font = main_text_font
        self.rect = pygame.Rect(self.x, self.y, self.main_text_font.size(main_text)[0], self.main_text_font.size(main_text)[1])
        self.render_main_text = self.main_text_font.render(main_text, True, main_text_color)
        self.hover_box = hover_box
        self.hover_box_group = hover_box_group
        self.is_showing_hover_box = False

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.render_main_text, (self.x, self.y))

        if self.rect.collidepoint(pos):
            self.hover_box.update_image(pos[0], pos[1])
            self.hover_box_group.add(self.hover_box)
            self.is_showing_hover_box = True
        else:
            if self.is_showing_hover_box:
                self.hover_box_group.remove(self.hover_box)
                self.is_showing_hover_box = False
