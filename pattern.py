class Pattern:
    """
    This is a class for the patterns extracted from the base tile.

    Attributes:
        pix_array (list): Two dimensonal array storing color data for every position in the Pattern. 
    """
    def __init__(self, pix_array):
        self.pix_array = pix_array
        
    def __len__(self) -> int:
        return 1