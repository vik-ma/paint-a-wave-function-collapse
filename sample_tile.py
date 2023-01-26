class SampleTile:
    """
    This is a class for the premade sample Base Tiles.
      
    Attributes:
        pix_array (list): Two dimensonal array storing color data for every position in the Tile. 
        width (int): Width of Tile (or Pixel Array).
        height (int): Height of Tile (or Pixel Array).
    """
    def __init__(self, pix_array, width, height):
        self.pix_array = pix_array
        self.width = width
        self.height = height