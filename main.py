import pygame
import random
import math
import time
import traceback
import asyncio
from copy import deepcopy
from tile import Tile
from button import Button
from pattern import Pattern
from rule_index import RuleIndex
from sample_tile import SampleTile
from tile_button import TileButton
from paint_tile import PaintTile
from info_text import InfoText
from hover_box import HoverBox
from arrow_button import ArrowButton


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DARKGREY = (105, 105, 105)
GREY = (175, 175, 175)
LIGHTGREY = (213, 213, 213)

LIGHTGREEN = (0, 255, 127)
GREEN = (0, 255, 00)
LAWNGREEN = (124,252,0)
DARKISHGREEN = (50, 205, 50)
DARKGREEN = (0, 128, 0)

LIGHTYELLOW = (255, 255, 125)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
KHAKI = (240, 230, 140)

ORANGE = (255, 165, 0)
ORANGEBROWN = (218, 165, 32)
ORANGERED = (255, 69, 0)

LIGHTBROWN = (244, 164, 96)
BROWN = (139, 69, 19)
DARKBROWN = (92, 64, 51)

DARKRED = (128, 0, 0)
RED = (255, 0, 0)
CRIMSON = (220, 20, 60)

DARKPURPLE = (75, 0, 130)
PURPLE = (150, 50, 255)
LIGHTPURPLE = (186, 85, 211)

PINK = (255, 20, 147)
LIGHTISHPINK = (255, 105, 180)
LIGHTPINK = (255, 228, 225)

CYAN = 	(0, 255, 255)
LIGHTBLUE = (100, 175, 255)
LIGHTISHBLUE = (30, 144, 255)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 155)

COLOR_LIST = [WHITE, LIGHTGREY, GREY, DARKGREY, BLACK,
            DARKBROWN, BROWN, LIGHTBROWN, ORANGEBROWN, 
            KHAKI, LIGHTYELLOW, YELLOW, GOLD, ORANGE, 
            ORANGERED, RED, DARKRED, CRIMSON, PINK,
            LIGHTISHPINK, LIGHTPINK, LIGHTPURPLE, PURPLE,
            DARKPURPLE, DARKBLUE, BLUE, LIGHTISHBLUE, LIGHTBLUE,
            CYAN, LIGHTGREEN, GREEN, LAWNGREEN, DARKISHGREEN, DARKGREEN]

BACKGROUND_COLOR = (155, 155, 155)
SCREEN_TEXT_COLOR = (30, 30, 30)
IMPORTANT_SCREEN_TEXT_COLOR = (170, 0, 30)
HELP_TITLE_TEXT_COLOR = (105, 0, 135)

UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)
UP_LEFT = (-1, -1)
UP_RIGHT = (1, -1)
DOWN_LEFT = (-1, 1)
DOWN_RIGHT = (1, 1)
directions = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

# List of premade sample Base Tiles
sample_tile_list = []

# Unused color variations of original sample tile

# original_pixel_array = [
#     (WHITE, WHITE, WHITE, WHITE),
#     (WHITE, BLACK, BLACK, BLACK),
#     (WHITE, BLACK, LIGHTGREY, BLACK),
#     (WHITE, BLACK, BLACK, BLACK),
#     ]
# original_sample_tile = SampleTile(original_pixel_array, 4, 4)

# green_original_pixel_array = [
#     ((50, 205, 50), (50, 205, 50), (50, 205, 50), (50, 205, 50)), 
#     ((50, 205, 50), (0, 128, 0), (0, 128, 0), (0, 128, 0)), 
#     ((50, 205, 50), (0, 128, 0), (240, 230, 140), (0, 128, 0)), 
#     ((50, 205, 50), (0, 128, 0), (0, 128, 0), (0, 128, 0))
#     ]
# green_original_sample_tile = SampleTile(green_original_pixel_array, 4, 4)

beige_brown_green_original_pixel_array = [
    ((240, 230, 140), (240, 230, 140), (240, 230, 140), (240, 230, 140)), 
    ((240, 230, 140), (92, 64, 51), (92, 64, 51), (92, 64, 51)), 
    ((240, 230, 140), (92, 64, 51), (124, 252, 0), (92, 64, 51)), 
    ((240, 230, 140), (92, 64, 51), (92, 64, 51), (92, 64, 51))
]
beige_brown_green_original_sample_tile = SampleTile(beige_brown_green_original_pixel_array, 4, 4)

flower_pix_array = [
    ((0, 128, 0), (124, 252, 0), (124, 252, 0), (124, 252, 0), (255, 20, 147), (255, 228, 225)), 
    ((124, 252, 0), (124, 252, 0), (218, 165, 32), (124, 252, 0), (124, 252, 0), (255, 20, 147)), 
    ((124, 252, 0), (218, 165, 32), (255, 255, 125), (218, 165, 32), (124, 252, 0), (124, 252, 0)), 
    ((124, 252, 0), (124, 252, 0), (218, 165, 32), (124, 252, 0), (124, 252, 0), (124, 252, 0)), 
    ((75, 0, 130), (124, 252, 0), (124, 252, 0), (124, 252, 0), (124, 252, 0), (255, 69, 0)), 
    ((100, 175, 255), (75, 0, 130), (124, 252, 0), (124, 252, 0), (255, 69, 0), (255, 215, 0))
    ]
flower_sample_tile = SampleTile(flower_pix_array, 6, 6)

fire_pix_array = [
    ((92, 64, 51), (92, 64, 51), (92, 64, 51), (255, 0, 0), (92, 64, 51), (92, 64, 51), (92, 64, 51)), 
    ((92, 64, 51), (92, 64, 51), (255, 0, 0), (255, 165, 0), (255, 0, 0), (92, 64, 51), (92, 64, 51)), 
    ((92, 64, 51), (255, 0, 0), (255, 165, 0), (255, 255, 125), (255, 165, 0), (255, 0, 0), (92, 64, 51)), 
    ((255, 0, 0), (255, 165, 0), (255, 255, 125), (255, 255, 125), (255, 255, 125), (255, 165, 0), (255, 0, 0)), 
    ((92, 64, 51), (255, 0, 0), (255, 165, 0), (255, 255, 125), (255, 165, 0), (255, 0, 0), (92, 64, 51)), 
    ((92, 64, 51), (92, 64, 51), (255, 0, 0), (255, 165, 0), (255, 0, 0), (92, 64, 51), (92, 64, 51)), 
    ((92, 64, 51), (92, 64, 51), (92, 64, 51), (255, 0, 0), (92, 64, 51), (92, 64, 51), (92, 64, 51))
    ]
fire_sample_tile = SampleTile(fire_pix_array, 7, 7)

ice_pix_array = [
    ((0, 0, 155), (0, 0, 155), (30, 144, 255), (0, 255, 255)), 
    ((0, 0, 155), (30, 144, 255), (0, 255, 255), (255, 255, 255)), 
    ((30, 144, 255), (0, 255, 255), (255, 255, 255), (255, 255, 255)), 
    ((0, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255))
    ]
ice_sample_tile = SampleTile(ice_pix_array, 4, 4)

purple_void_pix_array = [
    ((0, 0, 0), (0, 0, 0), (255, 228, 225), (186, 85, 211), (150, 50, 255), (75, 0, 130), (75, 0, 130)), 
    ((0, 0, 0), (255, 228, 225), (186, 85, 211), (150, 50, 255), (75, 0, 130), (75, 0, 130), (75, 0, 130)), 
    ((255, 228, 225), (186, 85, 211), (150, 50, 255), (75, 0, 130), (75, 0, 130), (75, 0, 130), (150, 50, 255)), 
    ((186, 85, 211), (150, 50, 255), (75, 0, 130), (75, 0, 130), (75, 0, 130), (150, 50, 255), (186, 85, 211)), 
    ((150, 50, 255), (75, 0, 130), (75, 0, 130), (75, 0, 130), (150, 50, 255), (186, 85, 211), (255, 228, 225)), 
    ((75, 0, 130), (75, 0, 130), (75, 0, 130), (150, 50, 255), (186, 85, 211), (255, 228, 225), (0, 0, 0)), 
    ((75, 0, 130), (75, 0, 130), (150, 50, 255), (186, 85, 211), (255, 228, 225), (0, 0, 0), (0, 0, 0))
    ] 
purple_void_sample_tile = SampleTile(purple_void_pix_array, 7, 7)

sample_tile_list.append(beige_brown_green_original_sample_tile)
sample_tile_list.append(ice_sample_tile)
sample_tile_list.append(flower_sample_tile)
sample_tile_list.append(fire_sample_tile)
sample_tile_list.append(purple_void_sample_tile)


def get_rotated_pix_array(pix_array) -> tuple:
    """
    Take a two dimensional pixel array (list) and return a tuple consisting of
    the same pixel array in tuple form, every 90 degree rotation of the original pixel array,
    and the vertical and horizontal mirror of the pixel array.
    """
    rotated_pix_array_270 = tuple(zip(*pix_array[::-1]))
    rotated_pix_array_180 = tuple(zip(*rotated_pix_array_270[::-1]))
    rotated_pix_array_90 = tuple(zip(*rotated_pix_array_180[::-1]))

    if len(pix_array) == 2:
        # 2x2 patterns
        vertically_flipped_pix_array = tuple(pix_array[0][::-1]), tuple(pix_array[-1][::-1])
    elif len(pix_array) == 3:
        # 3x3 patterns
        vertically_flipped_pix_array = tuple(pix_array[0][::-1]), tuple(pix_array[1][::-1]), tuple(pix_array[-1][::-1])

    horizontally_flipped_pix_array = tuple(pix_array[::-1])
    pix_array = tuple(pix_array)

    return (pix_array, rotated_pix_array_90, rotated_pix_array_180, rotated_pix_array_270, vertically_flipped_pix_array, horizontally_flipped_pix_array)


def get_offset_tiles(pattern, offset) -> tuple:
    """
    Return the tile(s) from input pattern pix_array which intersects with 
    input offset coordinates (x, y) from the perspective of the offset.
    """
    if offset == (0, 0):
        return pattern.pix_array
    if offset == (-1, -1):
        return tuple([pattern.pix_array[1][1]])
    if offset == (0, -1):
        return tuple(pattern.pix_array[1][:])
    if offset == (1, -1):
        return tuple([pattern.pix_array[1][0]])
    if offset == (-1, 0):
        return tuple([pattern.pix_array[0][1], pattern.pix_array[1][1]])
    if offset == (1, 0):
        return tuple([pattern.pix_array[0][0], pattern.pix_array[1][0]])
    if offset == (-1, 1):
        return tuple([pattern.pix_array[0][1]])
    if offset == (0, 1):
        return tuple(pattern.pix_array[0][:])
    if offset == (1, 1):
        return tuple([pattern.pix_array[0][0]])

def get_valid_directions(position, output_width, output_height) -> list:
    """
    Return a list of strings representing the valid directions that can be taken 
    from the given input position on the grid.
    """
    x, y = position
    
    valid_directions = []

    if x == 0:
        valid_directions.extend([RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_RIGHT])
        elif y == output_height-1:
            valid_directions.extend([UP, UP_RIGHT])
        else:
            valid_directions.extend([DOWN, DOWN_RIGHT, UP, UP_RIGHT])
    elif x == output_width-1:
        valid_directions.extend([LEFT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT])
        elif y == output_height-1:
            valid_directions.extend([UP, UP_LEFT])
        else:
            valid_directions.extend([DOWN, DOWN_LEFT, UP, UP_LEFT])
    else:
        valid_directions.extend([LEFT, RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT, DOWN_RIGHT])
        elif y == output_height-1:
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT])
        else: 
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT])
    
    return valid_directions

def get_patterns(pattern_size, base_tile) -> tuple:
    """
    Return a tuple consisting of a list of every unique pattern of input size pattern_size x pattern_size 
    inside input base_tile object, a dictionary of each unique pattern's occurence weight and a dictionary
    of each unique pattern's probability of being propagated.
    """
    pattern_list = []

    occurence_weights = {}
    probability = {}

    pix_array = base_tile.pix_array

    # Get every 2x2 pattern in Base Tile along with all rotations and mirrors of pattern
    for row in range(base_tile.width - (pattern_size - 1)):
        for col in range(base_tile.height - (pattern_size - 1)):
            pattern = []
            for pix in pix_array[row:row+pattern_size]:
                pattern.append(pix[col:col+pattern_size])
            pattern_rotations = get_rotated_pix_array(pattern)
        
            for rotation in pattern_rotations:
                if rotation not in occurence_weights:
                    occurence_weights[rotation] = 1
                else:
                    occurence_weights[rotation] += 1
            
            pattern_list.extend(pattern_rotations)
    
    # Remove all duplicate patterns
    unique_pattern_list = []
    for pattern in pattern_list:
        if pattern not in unique_pattern_list:
            unique_pattern_list.append(pattern)
    pattern_list = unique_pattern_list

    # Calculate probability for every unique pattern
    sum_of_weights = 0
    for weight in occurence_weights:
        sum_of_weights += occurence_weights[weight]

    for pattern in pattern_list:
        probability[pattern] = occurence_weights[pattern] / sum_of_weights

    pattern_list = [Pattern(pattern) for pattern in pattern_list]
    occurence_weights = {pattern:occurence_weights[pattern.pix_array] for pattern in pattern_list}
    probability = {pattern:probability[pattern.pix_array] for pattern in pattern_list}

    return pattern_list, occurence_weights, probability

def initialize_wave_function(pattern_list, output_width, output_height) -> list:
    """
    Create and return a two dimensional array of size output_width x output_height, 
    where every element stores a list of every pattern in input pattern_list. 
    """
    coefficients = []
    for col in range(output_width):
        row = []
        for r in range(output_height):
            row.append(pattern_list)
        coefficients.append(row)
    return coefficients

def is_wave_function_fully_collapsed(coefficients) -> bool:
    """Check if wave function is fully collapsed meaning that for each tile available is only one pattern."""
    for col in coefficients:
        for entry in col:
            if len(entry) > 1:
                return False
    return True

def get_possible_patterns_at_position(position, coefficients) -> list:
    """Return possible patterns at position (x, y)."""
    x, y = position
    possible_patterns = coefficients[x][y]
    return possible_patterns

def get_shannon_entropy(position, coefficients, probability) -> float:
    """Calcualte the Shannon Entropy of the wavefunction at position (x, y)."""
    x, y = position
    entropy = 0
    
    # A cell with one valid pattern has 0 entropy
    if len(coefficients[x][y]) == 1:
        return 0
    
    for pattern in coefficients[x][y]:
        entropy += probability[pattern] * math.log(probability[pattern], 2)
    entropy *= -1
    
    # Add noise to break ties and near-ties
    entropy -= random.uniform(0, 0.1)

    return entropy

def get_min_entropy_at_pos(coefficients, probability) -> tuple:
    """Return position of tile with the lowest entropy."""
    min_entropy = None
    min_entropy_pos = None
    
    for x, col in enumerate(coefficients):
        for y, row in enumerate(col):
            entropy = get_shannon_entropy((x, y), coefficients, probability)

            if entropy == 0:
                continue
            
            if min_entropy is None or entropy < min_entropy:
                min_entropy = entropy
                min_entropy_pos = (x, y)

    return min_entropy_pos

def observe(coefficients, probability, coefficients_state) -> tuple:
    """
    Return the position of the grid with the lowest entropy after assigning
    a pattern to the position and updating the grid.
    """
    # Find the lowest entropy
    min_entropy_pos = get_min_entropy_at_pos(coefficients, probability)

    if min_entropy_pos == None:
        print("All tiles have 0 entropy")
        return
    
    # Choose a pattern at lowest entropy position which is most frequent in the sample
    possible_patterns = get_possible_patterns_at_position(min_entropy_pos, coefficients)

    random_pattern = random.choice([pat for pat in possible_patterns])

    # Set this pattern to be the only available at this position
    coefficients[min_entropy_pos[0]][min_entropy_pos[1]] = random_pattern
    
    # Store current state in history of WFC progress
    current_coefficients = deepcopy(coefficients)
    coefficients_state.append(current_coefficients)

    return min_entropy_pos

def propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, coefficients_state):
    """Propagate wave function at min_entropy_pos, updating its neighbouring tiles' patterns."""
    stack = [min_entropy_pos]

    while len(stack) > 0:
        pos = stack.pop()
        
        possible_patterns = get_possible_patterns_at_position(pos, coefficients)
        
        # Iterate through each location immediately adjacent to the current location
        for direction in get_valid_directions(pos, output_width, output_height):
            adjacent_pos = (pos[0] + direction[0], pos[1] + direction[1])
            possible_patterns_at_adjacent = get_possible_patterns_at_position(adjacent_pos, coefficients)
            
            # Iterate over all still available patterns in adjacent tile 
            # and check if pattern is still possible in this location
            if not isinstance(possible_patterns_at_adjacent, list):
                possible_patterns_at_adjacent = [possible_patterns_at_adjacent]
            
            for possible_pattern_at_adjacent in possible_patterns_at_adjacent:
                if len(possible_patterns) > 1:
                    is_possible = any([rule_index.check_possibility(pattern, possible_pattern_at_adjacent, direction) for pattern in possible_patterns])
                else:
                    is_possible = rule_index.check_possibility(possible_patterns, possible_pattern_at_adjacent, direction)
                """
                If the tile is not compatible with any of the tiles in the current location's wavefunction
                then it's impossible for it to ever get choosen so it needs to be removed from the other
                location's wavefunction
                """

                if not is_possible:
                    x, y = adjacent_pos
                    coefficients[x][y] = [patt for patt in coefficients[x][y] if patt.pix_array != possible_pattern_at_adjacent.pix_array]
                   
                    # Store current state in history of WFC progress
                    current_coefficients = deepcopy(coefficients)
                    coefficients_state.append(current_coefficients)
                        
                    if adjacent_pos not in stack:
                        stack.append(adjacent_pos)
    
async def execute_wave_function_collapse(patterns, output_width, output_height, asyncio_queue, wfc_state):
    """Start wave function collapse algorithm with input patterns and send updates to GUI through asyncio."""
    pattern_list = patterns[0]
    occurence_weights = patterns[1]
    probability = patterns[2]

    # Create rules for adjacent patterns for every pattern
    rule_index = RuleIndex(pattern_list, directions)

    number_of_rules = 0
    for pattern in pattern_list:
        for direction in directions:
            for pattern_next in pattern_list:
                overlap = get_offset_tiles(pattern_next, direction)
                og_dir = tuple([direction[0]*-1, direction[1]*-1])
                part_of_og_pattern = get_offset_tiles(pattern, og_dir)
                if overlap == part_of_og_pattern:
                    rule_index.add_rule(pattern, direction, pattern_next)
                    number_of_rules += 1

    coefficients = initialize_wave_function(pattern_list, output_width, output_height)

    perf_time_start = time.perf_counter()
    print("Wave Function Collapse Started")

    has_wfc_failed = False

    # List to store WFC progress history
    coefficients_state = []

    # Status message to report result of WFC
    wfc_status = ""

    # Actual start of WFC algorihm
    try:
        while not is_wave_function_fully_collapsed(coefficients):
            if wfc_state["interrupt"]:
                print("break")
                wfc_status = "finished-interrupted"
                break

            # Add latest status to asyncio queue to give real time updates to GUI
            await asyncio_queue.put(["ongoing", deepcopy(coefficients)])

            min_entropy_pos = observe(coefficients, probability, coefficients_state)

            await asyncio_queue.put(["ongoing", deepcopy(coefficients)])

            propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, coefficients_state)
            
            # Sleep to allow GUI to update while algorithm is running
            await asyncio.sleep(0)
            
            await asyncio_queue.put(["ongoing", deepcopy(coefficients)])

    except Exception as e:
        has_wfc_failed = True
        # print("WFC FAIL: ", e)
        traceback.print_exc()

    perf_time_end = time.perf_counter()
    print(f"Wave Function Collapse Ended After {(perf_time_end - perf_time_start):.3f}s")

    if wfc_status == "":
        if not has_wfc_failed:
            wfc_status = "finished-success"
        else:
            wfc_status = "finished-fail"

    """
    Create Pixel Array of final image by storing the top left color of the pattern 
    at every position in the wave function matrix. 
    """
    final_pixels = []
    for i in coefficients:
        row = []
        for j in i:
            if isinstance(j, list):
                if len(j) > 0:
                    first_pixel = j[0].pix_array[0][0]
                else:
                    """
                    If WFC fails, the position that failed will be assigned grey or
                    "transparent" color since it will not have any pattern stored.
                    """
                    first_pixel = BACKGROUND_COLOR
            else:
                first_pixel = j.pix_array[0][0]
            row.append(first_pixel)
        final_pixels.append(row)

    # Add final information about the executed WFC into asyncio queue
    await asyncio_queue.put([wfc_status, final_pixels, coefficients_state, round((perf_time_end - perf_time_start), 3)])

def draw_window(screen):
    """Fill window with background color."""
    screen.fill(BACKGROUND_COLOR)

def get_pattern_tiles(patterns, pattern_size, enlargement_scale) -> list:
    """Create and return a list of Tile objects for every pattern in 'patterns' list."""
    y_offset = 24
    x_offset = 20

    # X and Y offset for 3x3 patterns, not currently implemented
    # if pattern_size == 3:
    #     y_offset = 38
    #     x_offset = 33

    x = 10 # Start x-coordinate
    y = 335 # Start y-coordinate
    tiles_per_row_limit = 19 # Maximum tiles per row
    
    tile_list = []
    for col in range(len(patterns)):
        if col % tiles_per_row_limit == 0 and col > 1:
            # Start new row if tiles_per_row_limit reached
            y += y_offset
            x -= tiles_per_row_limit * (pattern_size + x_offset)
        tile = Tile(pattern_size, pattern_size, (col * (pattern_size + x_offset) + x), y, patterns[col].pix_array, enlargement_scale)
        tile_list.append(tile)
    return tile_list

def update_patterns(pattern_group, pattern_tile_list, pattern_draw_limit):
    """Add list of Tile objects input to pattern_group Sprite group."""
    pattern_group.empty()
    # Removes any patterns beyond pattern_draw_limit amount from pattern_tile_list
    pattern_tile_list = pattern_tile_list[:pattern_draw_limit]
    for pattern in pattern_tile_list:
        pattern_group.add(pattern)

def create_tile_buttons(base_tile_list) -> list:
    """Create and return a list of Tile objects for every sample Base Tile from input list."""
    tile_buttons = []
    for tile in base_tile_list:
        tile_button = TileButton(tile.x, tile.y, tile.image)
        tile_buttons.append(tile_button)
    return tile_buttons

def draw_selected_tile_border(screen, tile):
    """Draw a yellow border around input Tile object."""
    pygame.draw.rect(screen, YELLOW, (tile.x-5, tile.y-5, tile.width + 10, tile.height + 10), 4)

def show_prob(patterns):
    """Display each pattern from input's probability."""
    # CURRENTLY UNUSED FUNCTION
    count = 1
    for pattern, prob in patterns[2].items():
        print(count, pattern.pix_array, prob)
        count += 1

def get_pattern_dict(pattern_list) -> dict:
    """Return a dictionary that stores every pattern in input's position in (x, y) form."""
    # CURRENTLY UNUSED FUNCTION
    pattern_dict = {}
    for pattern in pattern_list:
        pattern_dict[pattern.pix_array] = (pattern.x, pattern.y)
    return pattern_dict

def create_empty_paint_grid(x_pos, y_pos, cols, rows, tile_size) -> list:
    """Create and return grid of white colored PaintTile objects from input coordinates and dimensions."""
    grid = []
    for col in range(cols):
        new_row = []
        for row in range(rows):
            tile = PaintTile(tile_size, tile_size, (x_pos + tile_size * col), (y_pos + tile_size * row), WHITE)
            new_row.append(tile)
        grid.append(new_row)
    return grid

def create_colored_paint_grid(x_pos, y_pos, tile_size, pix_array) -> list:
    """Create and return a paint grid colored in the same way as input pix_array."""
    grid = []
    for i, row in enumerate(pix_array):
        new_row = []
        for j, color in enumerate(row):
            tile = PaintTile(tile_size, tile_size, (x_pos + tile_size * i), (y_pos + tile_size * j), color)
            new_row.append(tile)
        grid.append(new_row)
    return grid

def create_pix_array(paint_grid) -> list:
    """Create and return a color pixel array tuple from input Paint Grid."""
    pix_array = []
    for col in paint_grid:
        new_row = []
        for tile in col:
            new_row.append(tile.color)
        pix_array.append(tuple(new_row))
    return pix_array

def create_paint_color_tiles() -> list:
    """Create and return a list of different colored PaintTile objects."""
    y = 28
    x = 10
    tiles_per_row_limit = 17 # Maximum paint tiles per row

    color_tile_list = []
    for col in range(34):
        if col % tiles_per_row_limit == 0 and col > 0:
            # Start new row if tiles_per_row_limit reached
            y += 33
            x = 10
        if col < len(COLOR_LIST):
            # Create a paint tile for every color in COLOR_LIST
            color_tile = PaintTile(30, 30, x, y, (COLOR_LIST[col]))
        else:
            # Create grey paint tiles if loop is longer than the amount of colors in COLOR_LIST
            # (Mostly for debugging purposes)
            color_tile = PaintTile(30, 30, x, y, GREY)
        color_tile_list.append(color_tile)
        x += 33
    return color_tile_list

def get_output_size_text_color(size) -> tuple:
    """Return a color based on input size number."""
    if size < 15:
        return GREEN
    elif size >= 15 and size < 22:
        return YELLOW
    return IMPORTANT_SCREEN_TEXT_COLOR # Red

def print_tile_colors(tile):
    """Print the pixel array of input Tile object in terminal."""
    print(tile.pix_array)

def create_tile_list(tile_list, tile_list_x_pos, tile_list_y_pos, tile_list_offset, enlargement_scale, tiles_per_row_limit) -> list:
    """Create and return a list of Tile objects from input tile_list."""
    x_pos = tile_list_x_pos
    y_pos = tile_list_y_pos
    
    tile_width = 0 # Width of last tile in row
    row_max_height = 0 # Height of largest tile in row

    new_tile_list = []

    for i, tile in enumerate(tile_list, start=1):
        new_tile = Tile(tile.width, tile.height, x_pos, y_pos, tile.pix_array, enlargement_scale)
        new_tile_list.append(new_tile)

        if tile.height > row_max_height:
            row_max_height = tile.height
        
        if i % tiles_per_row_limit == 0:
            # Start new row if tiles_per_row_limit is reached
            x_pos = tile_list_x_pos
            y_pos = y_pos + row_max_height * enlargement_scale + tile_list_offset
            tile_width = 0
            row_max_height = 0
        else:
            # Calculate x-coordinate of next tile in list if next tile is to be placed on the same row
            tile_width = tile.width * enlargement_scale
            x_pos += tile_width + tile_list_offset

    return new_tile_list
    

async def main(loop):
    """Take an asyncio event loop object and create GUI of application."""
    pygame.init()

    size_27_font = pygame.font.Font(pygame.font.get_default_font(), 27)
    size_24_font = pygame.font.Font(pygame.font.get_default_font(), 24)
    size_20_font = pygame.font.Font(pygame.font.get_default_font(), 20)
    size_18_font = pygame.font.Font(pygame.font.get_default_font(), 18)
    size_17_font = pygame.font.Font(pygame.font.get_default_font(), 17)

    # Dimensions of Pygame window
    WIDTH = 800
    HEIGHT = 640

    clock = pygame.time.Clock()
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Sprite Group for Pattern Tiles extracted from Base Tile 
    pattern_group = pygame.sprite.Group()
    # Sprite Group for first grid
    wfc_grid_group = pygame.sprite.Group()
    # Sprite Group for second grid
    wfc_second_grid_group = pygame.sprite.Group()
    # Sprite Group for all Paint Tiles
    paint_color_group = pygame.sprite.Group()
    # Sprite Group for HoverBox (Must be called last to be drawn on top)
    hover_box_group = pygame.sprite.Group()

    hover_box_font = size_18_font
    hover_box_line_height = hover_box_font.get_linesize()
    
    start_wfc_button = Button(WHITE, 509, 114, 150, 44, "Start WFC", BLACK, LIGHTGREY, big_text=True)
    cancel_wfc_button = Button(GREY, 668, 118, 120, 40, "Cancel WFC", DARKGREY, GREY)

    skip_replay_button = Button(GREY, 509, 163, 130, 40, "Skip Replay", DARKGREY, GREY)
    replay_animation_button = Button(GREY, 509, 208, 170, 40, "Replay Last WFC", DARKGREY, GREY)

    paint_new_tile_button = Button(WHITE, 650, 320, 140, 36, "Paint New Tile", BLACK, LIGHTGREY)
    return_to_wfc_button = Button(WHITE, 600, 7, 190, 40, "Return To WFC", BLACK, LIGHTGREY, big_text=True)
    
    help_button = Button(WHITE, 9, 595, 110, 38, "HELP", BLACK, LIGHTGREY, big_text=True)
    return_from_help_button = Button(WHITE, 673, 593, 120, 40, "Return", BLACK, LIGHTGREY, big_text=True)

    increase_wfc_output_size_button = ArrowButton(WHITE, 715, 47, 26, 17, BLACK, LIGHTGREY, is_pointing_up=True)
    decrease_wfc_output_size_button = ArrowButton(WHITE, 715, 66, 26, 17, BLACK, LIGHTGREY, is_pointing_up=False)

    toggle_anim_during_wfc_button = Button(WHITE, 369, 548, 50, 20, "Change", BLACK, LIGHTGREY, small_text=True)
    toggle_anim_after_wfc_button = Button(WHITE, 369, 570, 50, 20, "Change", BLACK, LIGHTGREY, small_text=True)

    increase_replay_speed_button = ArrowButton(WHITE, 165, 512, 26, 17, BLACK, LIGHTGREY, is_pointing_up=True)
    decrease_replay_speed_button = ArrowButton(WHITE, 165, 531, 26, 17, BLACK, LIGHTGREY, is_pointing_up=False)

    increase_paint_grid_size_button = ArrowButton(WHITE, 300, 95, 26, 17, BLACK, LIGHTGREY, is_pointing_up=True)
    decrease_paint_grid_size_button = ArrowButton(WHITE, 300, 114, 26, 17, BLACK, LIGHTGREY, is_pointing_up=False)

    clear_paint_grid_button = Button(WHITE, 9, 520, 170, 40, "Clear Paint Grid", BLACK, LIGHTGREY)
    toggle_grid_lines_button = Button(WHITE, 190, 520, 170, 40, "Toggle Grid Lines", BLACK, LIGHTGREY)

    save_tile_button = Button(WHITE, 615, 120, 150, 46, "Save Tile", BLACK, LIGHTGREY, big_text=True)
    delete_tile_button = Button(WHITE, 600, 320, 190, 36, "Delete Selected Tile", BLACK, LIGHTGREY)
    copy_tile_button = Button(WHITE, 440, 268, 190, 36, "Copy Selected Tile", BLACK, LIGHTGREY)

    # Unused buttons
    # test_button = Button(WHITE, 660, 163, 130, 40, "TEST", BLACK, LIGHTGREY)
    # test_paint_button = Button(WHITE, 620, 30, 150, 40, "TEST", BLACK, LIGHTGREY)
    # set_pattern_size_2_button = Button(WHITE, 570, 400, 200, 40, "Set Pattern Size 2", BLACK, LIGHTGREY)
    # set_pattern_size_3_button = Button(WHITE, 570, 450, 200, 40, "Set Pattern Size 3", BLACK, LIGHTGREY)

    run = True

    draw_second_grid = True

    # Tile Sprite for first grid
    wfc_output = None
    # Tile Sprite for second grid
    wfc_output_2 = None

    # Scale at which a Tile pixel gets scaled up by
    enlargement_scale = 8

    # X and Y start position of list of Base Tiles
    tile_list_x_pos = 455
    tile_list_y_pos = 368
    # Free space between every Tile in list of Base Tiles
    tile_list_offset = 12

    # Height of largest Base Tile in last row
    base_tile_max_height = 7
    # Amount of Base Tiles to be drawn per row
    base_tiles_per_row_limit = 5
    # Max amount of Base Tiles allowed in list of Base Tiles
    max_base_tiles = 20

    # List of Base Tiles
    base_tile_list = create_tile_list(sample_tile_list, tile_list_x_pos, tile_list_y_pos, tile_list_offset, enlargement_scale, base_tiles_per_row_limit)

    # Width and height of Pattern extracted from Base Tile
    pattern_size = 2

    # Index of selected Base Tile in base_tile_list
    selected_base_tile_index = 0

    """
    Tuple consisting of a list of every unique Pattern from Base Tile,
    along with two dictionaries to store each patterns occurence weights
    and probability respectively.
    """
    patterns = get_patterns(pattern_size, base_tile_list[selected_base_tile_index])
    
    # List of all Tile objects in Pattern list
    pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)

    # Amount of maximum patterns to be drawn on screen
    pattern_draw_limit = 57 
    # Add Patterns to be drawn on screen to pattern_group Sprite Group
    update_patterns(pattern_group, pattern_tile_list, pattern_draw_limit)

    # Start position of first grid
    grid_x_pos = 10
    grid_y_pos = 28
    # Start position of second grid
    second_grid_x_pos = 260
    second_grid_y_pos = 28

    # Output size of WFC image in pixels
    output_width = 20
    output_height = 20

    # Different color to represent slowness of WFC at different output sizes
    output_size_text_color = get_output_size_text_color(output_width)

    grid_size = output_width

    # Maximum and minimum allowed output sizes
    output_grid_upper_limit = 30
    output_grid_lower_limit = 10
    
    # Clickable buttons for every selectable Base Tile
    tile_buttons = create_tile_buttons(base_tile_list)   

    # Draw selected Base Tile
    selected_base_tile = tile_buttons[selected_base_tile_index]
    selected_base_tile_x_pos = 510
    selected_base_tile_y_pos = 50
    selected_base_tile_image = selected_base_tile.image.copy()

    selected_base_tile_text = size_20_font.render("Base Tile", True, SCREEN_TEXT_COLOR)

    # Full history of WFC progress stored as a list of images
    wfc_order_list = []
    # Index of current WFC state image as second grid loops through the full WFC progress
    wfc_list_count = 0

    # Number to represent the interval of elements from wfc_order_list to be stored in sliced_list
    wfc_replay_slice_num = 5
    # Sliced history list of WFC progress where only every Nth element is stored
    sliced_list = []
    # Final image of WFC
    last_image = None
    # Maximum and minimum allowed values for wfc_replay_slice_num
    wfc_slice_num_upper_limit = 15
    wfc_slice_num_lower_limit = 1

    # Default game state
    game_state = "wfc"
    # Game state to return to from Help state
    previous_game_state = "wfc"

    current_color_text = size_18_font.render("Paint Color:", True, SCREEN_TEXT_COLOR)

    # Start position of Paint Grid
    paint_grid_x_pos = 10
    paint_grid_y_pos = 158
    # Size of clickable Tile in Paint Grid
    paint_grid_tile_size = 50

    # Size of Paint Grid/Painted Tile
    paint_grid_cols = 4
    paint_grid_rows = 4

    #Maximum and minimum allowed sized for Paint Grid/Painted Tile
    paint_grid_size_limit_upper = 7
    paint_grid_size_limit_lower = 3

    paint_guide_color_text = size_18_font.render("Click on a color in the color panel to change color", True, IMPORTANT_SCREEN_TEXT_COLOR)
    paint_guide_grid_text = size_18_font.render("Click on a square in the grid to paint the tile", True, IMPORTANT_SCREEN_TEXT_COLOR)
    
    paint_guide_save_text_lines = ["Click on 'Save Tile' to", "save the current tile"]
    paint_guide_save_text = []
    for line in paint_guide_save_text_lines:
        paint_guide_save_text.append(size_18_font.render(line, True, IMPORTANT_SCREEN_TEXT_COLOR))

    current_paint_tile_size_text = size_18_font.render(f"Tile Size: {paint_grid_cols}x{paint_grid_rows}", True, SCREEN_TEXT_COLOR)

    painted_tile_text = size_20_font.render("Painted Tile", True, SCREEN_TEXT_COLOR)

    # Clickable Paint Grid
    paint_grid = create_empty_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_cols, paint_grid_rows, paint_grid_tile_size)

    # Pixel Array of the Paint Grid
    paint_grid_pix_array = create_pix_array(paint_grid)

    # Default selected color
    current_color = CRIMSON

    # Tile to show which color is selected
    current_color_tile = PaintTile(30, 30, paint_grid_x_pos + 114, 99, current_color)

    # Preview of Painted Tile
    preview_tile_x_pos = 455
    preview_tile_y_pos = 127
    preview_tile = Tile(paint_grid_cols, paint_grid_rows, preview_tile_x_pos, preview_tile_y_pos, paint_grid_pix_array, enlargement_scale)

    # Toggle to show black lines to separate Paint Tiles in Paint Gric
    draw_paint_grid_lines = True

    # Color Panel to select color
    color_panel = create_paint_color_tiles()

    # Is second grid animation ongoing
    is_wfc_replay_anim_ongoing = False

    # Last In First Out Queue to access WFC states from GUI as WFC is being executed
    asyncio_queue = asyncio.LifoQueue()

    # Has WFC been started and is ongoing
    has_wfc_executed = False

    # Has WFC been started and finished
    is_wfc_finished = False

    # Text to report finish status and time progressed of WFC algorithm
    wfc_finished_text = None
    wfc_state_text_pos = (8, 280)

    # String to report if WFC finished successfully, failed or was interrupted
    wfc_finish_status = ""

    # Variables to extract time taken by WFC to complete
    wfc_time_start = 0
    wfc_time_finish = 0

    # Will give real time updates of WFC state in first grid if True
    render_wfc_during_execution = True
    # Will automatically start more detailed replay of WFC progress in second grid after WFC finishes if True
    render_wfc_at_end = True

    output_size_hover_box_text = ["Larger output", "size increases", "execution time", "exponentially."]
    output_size_hover_box = HoverBox(155, len(output_size_hover_box_text) * hover_box_line_height + 14, output_size_hover_box_text, hover_box_font)
    output_size_text = InfoText(630, selected_base_tile_y_pos-23, "Output Size", size_20_font, SCREEN_TEXT_COLOR, output_size_hover_box, hover_box_group)
    output_size_value_text = InfoText(640, selected_base_tile_y_pos+7, f"{output_width} x {output_height}", size_20_font, output_size_text_color, output_size_hover_box, hover_box_group)

    settings_text = size_27_font.render("Settings", True, SCREEN_TEXT_COLOR)
    settings_sub_text = size_17_font.render("Hover over the settings for more information", True, IMPORTANT_SCREEN_TEXT_COLOR)

    replay_speed_hover_box_text = ["The replay shows every Nth state of the wave", 
                                  "function collapse, where N is the replay speed.", 
                                  "'1' will show the wave function collapse in its", 
                                  "entirety, but takes a very long time to finish."]
    replay_speed_hover_box = HoverBox(435, len(replay_speed_hover_box_text) * hover_box_line_height + 14, replay_speed_hover_box_text, hover_box_font)
    replay_speed_text = InfoText(10, 522, "Replay Speed:", size_17_font, SCREEN_TEXT_COLOR, replay_speed_hover_box, hover_box_group)

    replay_speed_value_text = size_20_font.render(str(wfc_replay_slice_num), True, BLUE)

    anim_during_wfc_hover_box_text = ["Shows the progress of the wave function", 
                                      "collapse as it's being executed."]
    anim_during_wfc_hover_box = HoverBox(380, len(anim_during_wfc_hover_box_text) * hover_box_line_height + 14, anim_during_wfc_hover_box_text, hover_box_font)
    anim_during_wfc_main_text = "Animate WFC state during execution:"
    anim_during_wfc_infotext = InfoText(10, 550, anim_during_wfc_main_text, size_17_font, SCREEN_TEXT_COLOR, anim_during_wfc_hover_box, hover_box_group)

    anim_after_wfc_hover_box_text = ["Replays a more detailed time lapse of the wave function", "collapse in a second grid once it has reached completion."]
    anim_after_wfc_hover_box = HoverBox(525, len(anim_after_wfc_hover_box_text) * hover_box_line_height + 14, anim_after_wfc_hover_box_text, hover_box_font)
    anim_after_wfc_main_text = "Replay WFC once it's completed:"
    anim_after_wfc_infotext = InfoText(10, 572, anim_after_wfc_main_text, size_17_font, SCREEN_TEXT_COLOR, anim_after_wfc_hover_box, hover_box_group)
    
    anim_during_wfc_value_text = size_17_font.render("ON", True, GREEN)
    anim_after_wfc_value_text = size_17_font.render("ON", True, GREEN)

    # Buttons to be disabled during WFC execution and post WFC replay animation
    disabled_buttons_during_wfc_exec_and_post_anim_list = [increase_wfc_output_size_button, decrease_wfc_output_size_button,
                                                          increase_replay_speed_button, decrease_replay_speed_button,
                                                          toggle_anim_after_wfc_button, toggle_anim_during_wfc_button,
                                                        #   set_pattern_size_2_button, set_pattern_size_3_button, 
                                                          replay_animation_button, paint_new_tile_button,
                                                          help_button]
    
    # Buttons to be disabled during WFC execution but NOT post WFC replay animation
    disabled_buttons_during_wfc_exec_but_not_post_anim_list = [start_wfc_button, skip_replay_button]

    # Buttons to only be enabled during post WFC replay animation
    enabled_buttons_only_during_wfc_post_anim = [skip_replay_button]

    # Buttons to only be enabled during WFC execution
    enabled_buttons_during_wfc_exec_list = [cancel_wfc_button]

    # Dictionary to allow interruption of WFC execution if "interrupt" gets assigned True
    wfc_state = {"interrupt": False}
    
    """
    Cooldown in frames after switching game state where buttons guarded by switch_state_cooldown
    are unusable to not allow accidental button presses after clicking on a button that changes
    game state, and the other button is drawn at the same position on the screen as the first one.
    """
    switch_state_cooldown = False

    # Number of frames where switch_state_cooldown will be True
    switch_state_cooldown_value = 30

    """
    Counter that counts down 1 every frame. 
    When it hits 0 switch_state_cooldown will be set to False again.
    """
    switch_state_cooldown_counter = switch_state_cooldown_value

    patterns_hover_box_text = ["Every different 2x2 pattern extracted from", 
                              "the Base Tile, including rotated, horizontally", 
                              "and vertically flipped variants.",
                              "These patterns will build the final image",
                              "through the Wave Function Collapse."]
    patterns_hover_box = HoverBox(413, len(patterns_hover_box_text) * hover_box_line_height + 14, patterns_hover_box_text, hover_box_font)
    patterns_text = InfoText(8, 310, "Patterns From Base Tile", size_20_font, SCREEN_TEXT_COLOR, patterns_hover_box, hover_box_group)
    num_patterns_text = size_17_font.render(f"({len(pattern_tile_list)})", True, SCREEN_TEXT_COLOR)
    
    num_patterns_warning_text_lines = ["WARNING: This many patterns can", "take a really long time to finish!"]
    num_patterns_warning_text = []
    for line in num_patterns_warning_text_lines:
        num_patterns_warning_text.append(size_17_font.render(line, True, IMPORTANT_SCREEN_TEXT_COLOR))

    tile_list_full_text_lines = ["List of Base Tiles full!", "Delete a tile first!"]
    tile_list_full_text = []
    for line in tile_list_full_text_lines:
        tile_list_full_text.append(size_17_font.render(line, True, IMPORTANT_SCREEN_TEXT_COLOR))

    tile_list_guide_text_lines = ["Click on a tile below to change", "the Base Tile, or click the button", "to paint your own custom tile"]
    tile_list_guide_text = []
    for line in tile_list_guide_text_lines:
        tile_list_guide_text.append(size_17_font.render(line, True, IMPORTANT_SCREEN_TEXT_COLOR))

    base_tiles_hover_box_text = ["The wave function collapse", "algorithm will procedurally", "generate a new image based", "on the patterns in the Base", "Tile."]
    base_tiles_hover_box = HoverBox(275, len(base_tiles_hover_box_text) * hover_box_line_height + 14, base_tiles_hover_box_text, hover_box_font)
    base_tiles_text = InfoText(tile_list_x_pos-5, tile_list_y_pos-42, "Base Tiles", size_27_font, SCREEN_TEXT_COLOR, base_tiles_hover_box, hover_box_group) 

    wfc_guide_text = size_18_font.render("Click on 'Start WFC' to generate a new image based on the selected Base Tile", True, IMPORTANT_SCREEN_TEXT_COLOR)

    # All Help section titles
    help_state_title_text_list = []
    help_state_title_text_list.append([size_24_font.render("What Is This Program?", True, HELP_TITLE_TEXT_COLOR), 8])
    help_state_title_text_list.append([size_24_font.render("How To Use", True, HELP_TITLE_TEXT_COLOR), 114])
    help_state_title_text_list.append([size_24_font.render("What Affects The Execution Time Of The WFC?", True, HELP_TITLE_TEXT_COLOR), 282])
    help_state_title_text_list.append([size_24_font.render("What Causes The Wave Function Collapse To Fail?", True, HELP_TITLE_TEXT_COLOR), 405])
    help_state_title_text_list.append([size_24_font.render("Why Does The Output End Up Not Looking Like The Base Tile?", True, HELP_TITLE_TEXT_COLOR), 485])

    # All Help section paragraphs
    help_state_sub_text_lines_1 = ["This program shows off the procedural image generation of the Wave Function Collapse", 
                                  "algorithm. In this application, a basic version of the WFC algorithm will generate a larger", 
                                  "image based off the patterns from a sample base tile. Since this is currently just a basic", 
                                  "adjacent model version of the WFC algorithm, support for the overlapping model,",
                                  "additional constraints or backtracking have not yet been implemented."]
    help_state_sub_text_1 = []
    for line in help_state_sub_text_lines_1:
        help_state_sub_text_1.append(size_17_font.render(line, True, SCREEN_TEXT_COLOR))

    help_state_sub_text_lines_2 = ["To generate a new image, click on the 'Start WFC' button. The WFC algorithm will then begin", 
                                  "and you will be able to see its progress as it is executing. After the WFC is finished, the",
                                  "second grid will show a more detailed replay of the procedural generation of the image.",
                                  "",
                                  "You can generate an image based of a different base tile by selecting one in the list in the",
                                  "bottom right, or paint your own base tile by clicking the 'Paint New Tile' button.",
                                  "",
                                  "The 'Cancel WFC' button will interrupt and stop the WFC when it's executing. This may not",
                                  "immediately happen, as the algorithm can only be interrupted during certain stages."]
    help_state_sub_text_2 = []
    for line in help_state_sub_text_lines_2:
        help_state_sub_text_2.append(size_17_font.render(line, True, SCREEN_TEXT_COLOR))

    help_state_sub_text_lines_3 = ["The first thing that will affect execution time is the output size of the generated image.", 
                                  "Larger output sizes will exponentially increase the execution time.",
                                  "",
                                  "The second thing is the amount of patterns that has been extracted from the base tile.",
                                  "A warning will appear if the selected base tile contains an amount of patterns that may", 
                                  "lead to a very slow execution."]
    help_state_sub_text_3 = []
    for line in help_state_sub_text_lines_3:
        help_state_sub_text_3.append(size_17_font.render(line, True, SCREEN_TEXT_COLOR))

    help_state_sub_text_lines_4 = ["The most common reason for the wave function failing to collapse is because it has generated",
                                  "a 2x2 pattern that no patterns from the list of base tile patterns can intersect with.",
                                  "This usually happens when two or more colors from the base tile share no 2x2 pattern."]
    help_state_sub_text_4 = []
    for line in help_state_sub_text_lines_4:
        help_state_sub_text_4.append(size_17_font.render(line, True, SCREEN_TEXT_COLOR))

    help_state_sub_text_lines_5 = ["Since this is just a basic adjacent model Wave Function Collapse, the only constraints are",
                                  "the patterns themselves. Considering that the patterns are only 2x2 tiles, this can result",
                                  "in a new image which bears very little resemblance to the original sample tile.",
                                  "",
                                  "Another thing to note is that the 'default background color' of the WFC will always be the",
                                  "top left pixel of the base tile."]
    help_state_sub_text_5 = []
    for line in help_state_sub_text_lines_5:
        help_state_sub_text_5.append(size_17_font.render(line, True, SCREEN_TEXT_COLOR))

    help_state_sub_text_list = []
    help_state_sub_text_list.append([help_state_sub_text_1, help_state_title_text_list[0][1]+24])
    help_state_sub_text_list.append([help_state_sub_text_2, help_state_title_text_list[1][1]+24])
    help_state_sub_text_list.append([help_state_sub_text_3, help_state_title_text_list[2][1]+24])
    help_state_sub_text_list.append([help_state_sub_text_4, help_state_title_text_list[3][1]+24])
    help_state_sub_text_list.append([help_state_sub_text_5, help_state_title_text_list[4][1]+24])

    def change_button_color(state, button_list):
        """Change color of all buttons in input button_list after input state specifications."""
        state_colors = {"disabled": {"color": GREY, "hover_color": GREY, "foreground_color": DARKGREY}, "enabled": {"color":WHITE, "hover_color": LIGHTGREY, "foreground_color": BLACK}} 

        for button in button_list:
            button.color = state_colors[state]["color"]
            button.hover_color = state_colors[state]["hover_color"]
            button.foreground_color = state_colors[state]["foreground_color"]

    while run:
        clock.tick(FPS)
        draw_window(screen)

        # WFC state
        if game_state == "wfc":
            # Cooldown to stop accidental clicking of button at same position as button at old state
            if switch_state_cooldown:
                switch_state_cooldown_counter -= 1
                if switch_state_cooldown_counter == 0:
                    switch_state_cooldown = False
                    switch_state_cooldown_counter = switch_state_cooldown_value
           

            screen.blit(wfc_guide_text, (10, 5))

            # First grid when WFC has been started
            if has_wfc_executed:
                # Get latest item added to queue (LIFO queue)
                current_wfc_state = await asyncio_queue.get()

                if current_wfc_state[0] == "ongoing":   
                    #If WFC is ongoing
                    time_progressed = time.perf_counter() - wfc_time_start
                    wfc_status_text = size_20_font.render(f"Wave Function Collapse In Progress... {round(time_progressed, 3)}s", True, DARKPURPLE)
                    screen.blit(wfc_status_text, wfc_state_text_pos)

                    if render_wfc_during_execution:
                        # Grid Animation
                        final_pixels = []
                        for i in current_wfc_state[1]:
                            row = []
                            for j in i:
                                if isinstance(j, list):
                                    if len(j) > 0:
                                        first_pixel = j[0].pix_array[0][0]
                                    else:
                                        first_pixel = BACKGROUND_COLOR
                                else:
                                    first_pixel = j.pix_array[0][0]
                                row.append(first_pixel)
                            final_pixels.append(row)

                        wfc_grid_group.empty()
                        wfc_output = Tile(grid_size, grid_size, grid_x_pos, grid_y_pos, final_pixels, enlargement_scale)
                        wfc_grid_group.add(wfc_output)
                else:   
                    # If WFC has finished
                    has_wfc_executed = False
                    is_wfc_finished = True
                    wfc_time_finish = current_wfc_state[3]
                    wfc_finish_status = current_wfc_state[0]

                    # Store full list of every WFC state for replay
                    wfc_order_list = current_wfc_state[2]
                    last_image = wfc_order_list[-1]
                    # Create shorter list where only every Nth element is stored (N = wfc_replay_slice_num) 
                    sliced_list = wfc_order_list[::wfc_replay_slice_num]
                    sliced_list.append(last_image)

                    if render_wfc_at_end:
                        change_button_color("enabled", disabled_buttons_during_wfc_exec_but_not_post_anim_list)
                        # Start replay animation
                        draw_second_grid = True
                        is_wfc_replay_anim_ongoing = True
                    else:
                        change_button_color("enabled", disabled_buttons_during_wfc_exec_and_post_anim_list)
                        change_button_color("enabled", [start_wfc_button])
                        for tile_button in tile_buttons:
                            # Remove opacity for base tile buttons
                            tile_button.image.set_alpha(255)

                    change_button_color("disabled", enabled_buttons_during_wfc_exec_list)

                    wfc_grid_group.empty()
                    wfc_output = Tile(grid_size, grid_size, grid_x_pos, grid_y_pos, current_wfc_state[1], enlargement_scale)
                    wfc_grid_group.add(wfc_output)

            # First grid border
            pygame.draw.rect(screen, BLACK, (grid_x_pos-1, grid_y_pos-1, (grid_size * enlargement_scale) + 2, (grid_size * enlargement_scale) + 2), 1)
        

            # Second grid
            if draw_second_grid:
                if is_wfc_replay_anim_ongoing:
                    if wfc_list_count < len(sliced_list):
                        # Loop through the enitre sliced list of WFC states and render one each frame
                        final_pixels = []
                        for i in sliced_list[wfc_list_count]: 
                            row = []
                            for j in i:
                                if isinstance(j, list):
                                    if len(j) > 0:
                                        first_pixel = j[0].pix_array[0][0]
                                    else:
                                        first_pixel = BACKGROUND_COLOR
                                else:
                                    first_pixel = j.pix_array[0][0]
                                row.append(first_pixel)
                            final_pixels.append(row)

                        wfc_second_grid_group.empty()
                        wfc_output_2 = Tile(grid_size, grid_size, second_grid_x_pos, second_grid_y_pos, final_pixels, enlargement_scale)
                        wfc_second_grid_group.add(wfc_output_2)
                        # Show next WFC state next frame
                        wfc_list_count += 1
                    if wfc_list_count == len(sliced_list):
                        is_wfc_replay_anim_ongoing = False
                        change_button_color("disabled", enabled_buttons_only_during_wfc_post_anim)
                        change_button_color("enabled", disabled_buttons_during_wfc_exec_and_post_anim_list)
                        for tile_button in tile_buttons:
                            tile_button.image.set_alpha(255)
                if wfc_output_2 != None:
                    # Second grid border
                    pygame.draw.rect(screen, BLACK, (second_grid_x_pos-1, second_grid_y_pos-1, (grid_size * enlargement_scale) + 2, (grid_size * enlargement_scale) + 2), 1)


            # WFC status text
            if is_wfc_finished:
                if wfc_finish_status == "finished-success":
                    wfc_finished_text = size_20_font.render(f"Wave Function Collapse Finished After {wfc_time_finish}s", True, LAWNGREEN)
                elif wfc_finish_status == "finished-fail":
                    wfc_finished_text = size_20_font.render(f"Wave Function Collapse Failed After {wfc_time_finish}s", True, CRIMSON)
                elif wfc_finish_status == "finished-interrupted":
                    wfc_finished_text = size_20_font.render(f"Wave Function Collapse Interrupted After {wfc_time_finish}s", True, DARKBROWN)
                screen.blit(wfc_finished_text, wfc_state_text_pos)


            # Selected Base Tile
            screen.blit(selected_base_tile_text, (selected_base_tile_x_pos-1, selected_base_tile_y_pos-23))
            screen.blit(selected_base_tile_image, (selected_base_tile_x_pos, selected_base_tile_y_pos))
            # Seledcted Base Tile Border
            pygame.draw.rect(screen, BLACK, (selected_base_tile_x_pos-1, selected_base_tile_y_pos-1, selected_base_tile.width + 2, selected_base_tile.height + 2), 1)


            # Output Size Setting
            output_size_text.draw(screen)
            output_size_value_text.draw(screen)

            if increase_wfc_output_size_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and output_width < output_grid_upper_limit and not has_wfc_executed:
                    output_width += 1
                    output_height += 1
                    output_size_text_color = get_output_size_text_color(output_width)
                    output_size_value_text.render_main_text = size_20_font.render(f"{output_width} x {output_height}", True, output_size_text_color)
                    if output_width == output_grid_upper_limit:
                        change_button_color("disabled", [increase_wfc_output_size_button])
                        disabled_buttons_during_wfc_exec_and_post_anim_list.remove(increase_wfc_output_size_button)
                    if output_width == output_grid_lower_limit + 1:
                        change_button_color("enabled", [decrease_wfc_output_size_button])
                        disabled_buttons_during_wfc_exec_and_post_anim_list.append(decrease_wfc_output_size_button)

            if decrease_wfc_output_size_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and output_width > output_grid_lower_limit and not has_wfc_executed:
                    output_width -= 1
                    output_height -= 1
                    output_size_text_color = get_output_size_text_color(output_width)
                    output_size_value_text.render_main_text = size_20_font.render(f"{output_width} x {output_height}", True, output_size_text_color)
                    if output_width == output_grid_lower_limit:
                        change_button_color("disabled", [decrease_wfc_output_size_button])
                        disabled_buttons_during_wfc_exec_and_post_anim_list.remove(decrease_wfc_output_size_button)
                    if output_width == output_grid_upper_limit - 1:
                        change_button_color("enabled", [increase_wfc_output_size_button])
                        disabled_buttons_during_wfc_exec_and_post_anim_list.append(increase_wfc_output_size_button)


            if start_wfc_button.draw(screen):
                if not has_wfc_executed and not switch_state_cooldown:
                    wfc_grid_group.empty()
                    wfc_second_grid_group.empty()
                    asyncio_queue = asyncio.LifoQueue()
                    wfc_list_count = 0
                    is_wfc_replay_anim_ongoing = False
                    has_wfc_executed = True
                    is_wfc_finished = False
                    wfc_state["interrupt"] = False
                    wfc_output_2 = None
                    grid_size = output_width
                    change_button_color("disabled", disabled_buttons_during_wfc_exec_and_post_anim_list)
                    change_button_color("disabled", disabled_buttons_during_wfc_exec_but_not_post_anim_list)
                    change_button_color("enabled", enabled_buttons_during_wfc_exec_list)
                    for tile_button in tile_buttons:
                        # Make base tile buttons opaque
                        tile_button.image.set_alpha(100)
                    wfc_time_start = time.perf_counter()
                    loop.create_task(execute_wave_function_collapse(patterns, output_width, output_height, asyncio_queue, wfc_state))

            if cancel_wfc_button.draw(screen):
                if has_wfc_executed:
                    wfc_state["interrupt"] = True

            if skip_replay_button.draw(screen):
                if is_wfc_replay_anim_ongoing:
                    wfc_list_count = len(sliced_list) - 1
                    change_button_color("disabled", enabled_buttons_only_during_wfc_post_anim)

            if replay_animation_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and not has_wfc_executed and len(wfc_order_list) > 0:
                    wfc_list_count = 0
                    is_wfc_replay_anim_ongoing = True
                    change_button_color("enabled", enabled_buttons_only_during_wfc_post_anim)
                    change_button_color("disabled", disabled_buttons_during_wfc_exec_and_post_anim_list)
                    if not draw_second_grid:
                        draw_second_grid = True
                        is_wfc_replay_anim_ongoing = True


            patterns_text.draw(screen)
            screen.blit(num_patterns_text, (251, 312))
            # List of pattern tiles
            for pattern in pattern_tile_list[:pattern_draw_limit]:
                pygame.draw.rect(screen, BLACK, (pattern.x - 1, pattern.y - 1, pattern.width * enlargement_scale + 2, pattern.height * enlargement_scale + 2), 1)

            # Warning for high amount of patterns
            if len(pattern_tile_list) > 39:
                for y, line in enumerate(num_patterns_warning_text):
                    screen.blit(line, (8, 409 + y * 18))


            for y, line in enumerate(tile_list_guide_text):
                screen.blit(line, (510, 253 + y * 18))

            # Lines for Base Tiles "box"
            pygame.draw.line(screen, BLACK, (440, 311), (800, 311))
            pygame.draw.line(screen, BLACK, (440, 311), (440, 640))

            base_tiles_text.draw(screen)
                   
            if paint_new_tile_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and not has_wfc_executed:
                    game_state = "paint"
                    previous_game_state = "paint"
                    switch_state_cooldown = True

            # Draw yellow border around selected tile
            draw_selected_tile_border(screen, selected_base_tile)

            # List of selectable Base Tiles
            for index, tile_button in enumerate(tile_buttons):
                if tile_button.draw(screen):
                    if not is_wfc_replay_anim_ongoing and not has_wfc_executed:
                        if index != selected_base_tile_index:
                            selected_base_tile = tile_buttons[index]
                            selected_base_tile_index = index
                            selected_base_tile_image = selected_base_tile.image.copy()
                            patterns = get_patterns(pattern_size, base_tile_list[index])
                            pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                            num_patterns_text = size_17_font.render(f"({len(pattern_tile_list)})", True, SCREEN_TEXT_COLOR)
                            update_patterns(pattern_group, pattern_tile_list, pattern_draw_limit)
                        
            
            # Line to separate Settings section
            pygame.draw.line(screen, BLACK, (0, 452), (440, 452))

            screen.blit(settings_text, (10, 460))
            screen.blit(settings_sub_text, (10, 489))

            replay_speed_text.draw(screen)
            screen.blit(replay_speed_value_text, (134, 521))

            if increase_replay_speed_button.draw(screen):
                if not is_wfc_replay_anim_ongoing:
                    if wfc_replay_slice_num < wfc_slice_num_upper_limit:
                        wfc_replay_slice_num += 1
                        sliced_list = wfc_order_list[::wfc_replay_slice_num]
                        sliced_list.append(last_image)
                        replay_speed_value_text = size_20_font.render(str(wfc_replay_slice_num), True, (0, 0, 255))
                        if wfc_replay_slice_num == wfc_slice_num_upper_limit:
                            change_button_color("disabled", [increase_replay_speed_button])
                            disabled_buttons_during_wfc_exec_and_post_anim_list.remove(increase_replay_speed_button)
                        if wfc_replay_slice_num == wfc_slice_num_lower_limit + 1:
                            change_button_color("enabled", [decrease_replay_speed_button])
                            disabled_buttons_during_wfc_exec_and_post_anim_list.append(decrease_replay_speed_button)

            if decrease_replay_speed_button.draw(screen):
                if not is_wfc_replay_anim_ongoing:
                    if wfc_replay_slice_num > wfc_slice_num_lower_limit:
                        wfc_replay_slice_num -= 1
                        sliced_list = wfc_order_list[::wfc_replay_slice_num]
                        sliced_list.append(last_image)
                        replay_speed_value_text = size_20_font.render(str(wfc_replay_slice_num), True, (0, 0, 255))
                        if wfc_replay_slice_num == wfc_slice_num_lower_limit:
                            change_button_color("disabled", [decrease_replay_speed_button])
                            disabled_buttons_during_wfc_exec_and_post_anim_list.remove(decrease_replay_speed_button)
                        if wfc_replay_slice_num == wfc_slice_num_upper_limit - 1:
                            change_button_color("enabled", [increase_replay_speed_button])
                            disabled_buttons_during_wfc_exec_and_post_anim_list.append(increase_replay_speed_button)

            anim_during_wfc_infotext.draw(screen)
            screen.blit(anim_during_wfc_value_text, (329, 550))

            if toggle_anim_during_wfc_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and not has_wfc_executed:
                    if render_wfc_during_execution:
                        render_wfc_during_execution = False
                        anim_during_wfc_value_text = size_17_font.render("OFF", True, DARKRED)
                    else:
                        render_wfc_during_execution = True
                        anim_during_wfc_value_text = size_17_font.render("ON", True, GREEN)
            
            anim_after_wfc_infotext.draw(screen)
            screen.blit(anim_after_wfc_value_text, (329, 572))

            if toggle_anim_after_wfc_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and not has_wfc_executed:
                    if render_wfc_at_end:
                        render_wfc_at_end = False
                        anim_after_wfc_value_text = size_17_font.render("OFF", True, DARKRED)
                    else:
                        render_wfc_at_end = True
                        anim_after_wfc_value_text = size_17_font.render("ON", True, GREEN)


            if help_button.draw(screen):
                if not is_wfc_replay_anim_ongoing and not has_wfc_executed:
                    game_state = "help"
                    previous_game_state = "wfc"


            # if test_button.draw(screen):
            #     print(patterns)


            # Unused buttons to change pattern size

            # if set_pattern_size_2_button.draw(screen):
            #     if not is_wfc_anim_ongoing and not is_wfc_executing:
            #         pattern_size = 2
            #         prob_text_x_offset = -2
            #         prob_text_y_offset = -11
            #         patterns = get_patterns(pattern_size, base_tile_list[selected_tile_index])
            #         pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)

            # if set_pattern_size_3_button.draw(screen):
            #     if not is_wfc_anim_ongoing and not is_wfc_executing:
            #         pattern_size = 3
            #         prob_text_x_offset = 2
            #         prob_text_y_offset = -11
            #         patterns = get_patterns(pattern_size, base_tile_list[selected_tile_index])
            #         pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)


            # Draw sprite groups
            wfc_grid_group.draw(screen)
            wfc_second_grid_group.draw(screen)
            pattern_group.draw(screen)
            hover_box_group.draw(screen)


        # Paint state
        if game_state == "paint":
            # Cooldown to stop accidental clicking of button at same position as button at old state
            if switch_state_cooldown:
                switch_state_cooldown_counter -= 1
                if switch_state_cooldown_counter == 0:
                    switch_state_cooldown = False
                    switch_state_cooldown_counter = switch_state_cooldown_value


            screen.blit(paint_guide_color_text, (10, 5))

            # Clickable color palette
            for color in color_panel:
                if color.draw(screen, border=True):
                    current_color = color.color
                    current_color_tile.image.fill(current_color)
            
            screen.blit(current_color_text, (paint_grid_x_pos, 105))
            current_color_tile.draw(screen, border=True)

            screen.blit(current_paint_tile_size_text, (175, 105))

            if increase_paint_grid_size_button.draw(screen):
                if paint_grid_cols < paint_grid_size_limit_upper:
                    paint_grid_cols += 1
                    paint_grid_rows += 1
                    new_grid = create_empty_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_cols, paint_grid_rows, paint_grid_tile_size)
                    for col in range(paint_grid_cols - 1):
                        for row in range(paint_grid_rows - 1):
                            new_grid[col][row] = paint_grid[col][row]
                    paint_grid = new_grid
                    paint_grid_pix_array = create_pix_array(paint_grid)
                    preview_tile = Tile(paint_grid_cols, paint_grid_rows, preview_tile_x_pos, preview_tile_y_pos, paint_grid_pix_array, enlargement_scale)
                    current_paint_tile_size_text = size_18_font.render(f"Tile Size: {paint_grid_cols}x{paint_grid_rows}", True, SCREEN_TEXT_COLOR)
                    if paint_grid_cols == paint_grid_size_limit_upper:
                        change_button_color("disabled", [increase_paint_grid_size_button])
                    if paint_grid_cols == paint_grid_size_limit_lower + 1:
                        change_button_color("enabled", [decrease_paint_grid_size_button])

            if decrease_paint_grid_size_button.draw(screen):
                if paint_grid_cols > paint_grid_size_limit_lower:
                    paint_grid_cols -= 1
                    paint_grid_rows -= 1
                    new_grid = []
                    for col in range(paint_grid_cols):
                        new_row = []
                        for row in range(paint_grid_rows):
                            new_row.append(paint_grid[col][row])
                        new_grid.append(new_row)
                    paint_grid = new_grid
                    paint_grid_pix_array = create_pix_array(paint_grid)
                    preview_tile = Tile(paint_grid_cols, paint_grid_rows, preview_tile_x_pos, preview_tile_y_pos, paint_grid_pix_array, enlargement_scale)
                    current_paint_tile_size_text = size_18_font.render(f"Tile Size: {paint_grid_cols}x{paint_grid_rows}", True, SCREEN_TEXT_COLOR)
                    if paint_grid_cols == paint_grid_size_limit_lower:
                        change_button_color("disabled", [decrease_paint_grid_size_button])
                    if paint_grid_cols == paint_grid_size_limit_upper - 1:
                        change_button_color("enabled", [increase_paint_grid_size_button])


            screen.blit(paint_guide_grid_text, (10, 133))

            # Paint grid
            for x, col in enumerate(paint_grid):
                for y, tile in enumerate(col):
                    if tile.draw(screen):
                        paint_grid[x][y] = PaintTile(paint_grid_tile_size, paint_grid_tile_size, paint_grid[x][y].x, paint_grid[x][y].y, current_color)

                        paint_grid_pix_array = create_pix_array(paint_grid)
                        preview_tile = Tile(paint_grid_cols, paint_grid_rows, preview_tile_x_pos, preview_tile_y_pos, paint_grid_pix_array, enlargement_scale)

            # Paint grid lines
            if draw_paint_grid_lines:
                for col in range(1, paint_grid_cols):
                    pygame.draw.line(screen, BLACK, (paint_grid_x_pos + col * paint_grid_tile_size, paint_grid_y_pos), (paint_grid_x_pos + col * paint_grid_tile_size, paint_grid_y_pos + paint_grid_tile_size * paint_grid_rows))
                for row in range(1, paint_grid_rows):
                    pygame.draw.line(screen, BLACK, (paint_grid_x_pos, paint_grid_y_pos + row * paint_grid_tile_size), (paint_grid_x_pos + paint_grid_tile_size * paint_grid_cols, paint_grid_y_pos + row * paint_grid_tile_size))

            # Paint grid border
            pygame.draw.rect(screen, BLACK, (paint_grid_x_pos-1, paint_grid_y_pos-1, (paint_grid_cols * paint_grid_tile_size + 2), (paint_grid_rows * paint_grid_tile_size) + 2), 1) 

            
            if clear_paint_grid_button.draw(screen):
                paint_grid = create_empty_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_cols, paint_grid_rows, paint_grid_tile_size)
                paint_grid_pix_array = create_pix_array(paint_grid)
                preview_tile = Tile(paint_grid_cols, paint_grid_rows, preview_tile_x_pos, preview_tile_y_pos, paint_grid_pix_array, enlargement_scale)

            if toggle_grid_lines_button.draw(screen):
                draw_paint_grid_lines = not draw_paint_grid_lines


            if return_to_wfc_button.draw(screen):
                game_state = "wfc"
                previous_game_state = "wfc"


            screen.blit(painted_tile_text, (preview_tile_x_pos-1, preview_tile_y_pos-23))
            # Painted Tile
            screen.blit(preview_tile.image, (preview_tile.x, preview_tile.y))
            # Preview Tile Border
            pygame.draw.rect(screen, BLACK, (preview_tile.x - 1, preview_tile.y - 1, (preview_tile.width * enlargement_scale) + 2, (preview_tile.height * enlargement_scale) + 2), 1)


            for y, line in enumerate(paint_guide_save_text):
                screen.blit(line, (600, 80 + y * 18))

            if save_tile_button.draw(screen):
                if len(base_tile_list) < max_base_tiles:
                    if len(base_tile_list) == 1:
                        change_button_color("enabled", [delete_tile_button])

                    prev_tile = base_tile_list[-1]
                    if len(tile_buttons) % base_tiles_per_row_limit == 0:
                        x_pos = tile_list_x_pos
                        y_pos = prev_tile.y + base_tile_max_height * enlargement_scale + tile_list_offset
                        base_tile_max_height = paint_grid_rows
                    else:
                        x_pos = prev_tile.x + prev_tile.width * enlargement_scale + tile_list_offset
                        y_pos = prev_tile.y
                    
                    if paint_grid_rows > base_tile_max_height:
                        base_tile_max_height = paint_grid_rows

                    new_tile_button = Tile(paint_grid_cols, paint_grid_rows, x_pos, y_pos, paint_grid_pix_array, enlargement_scale)
                    base_tile_list.append(new_tile_button)
                    tile_buttons = create_tile_buttons(base_tile_list)

                    selected_base_tile = tile_buttons[-1]
                    selected_base_tile_index = len(tile_buttons)-1
                    selected_base_tile_image = selected_base_tile.image.copy()

                    patterns = get_patterns(pattern_size, base_tile_list[-1])
                    pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                    num_patterns_text = size_17_font.render(f"({len(pattern_tile_list)})", True, SCREEN_TEXT_COLOR)
                    update_patterns(pattern_group, pattern_tile_list, pattern_draw_limit)

                    if len(base_tile_list) == max_base_tiles:
                        change_button_color("disabled", [save_tile_button])

                    switch_state_cooldown = True

                    game_state = "wfc"
                    previous_game_state = "wfc"

            # Message if Base Tile list is full
            if len(base_tile_list) == max_base_tiles:
                for y, line in enumerate(tile_list_full_text):
                    screen.blit(line, (600, 170 + y * 18))


            if copy_tile_button.draw(screen):
                paint_grid = create_colored_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_tile_size, base_tile_list[selected_base_tile_index].pix_array)
                paint_grid_pix_array = create_pix_array(paint_grid)
                paint_grid_cols = len(paint_grid_pix_array)
                paint_grid_rows = len(paint_grid_pix_array[0])
                preview_tile = Tile(paint_grid_cols, paint_grid_rows, preview_tile_x_pos, preview_tile_y_pos, paint_grid_pix_array, enlargement_scale)
                current_paint_tile_size_text = size_18_font.render(f"Tile Size: {paint_grid_cols}x{paint_grid_rows}", True, SCREEN_TEXT_COLOR)
                if paint_grid_cols == paint_grid_size_limit_upper:
                    change_button_color("disabled", [increase_paint_grid_size_button])
                else:
                    change_button_color("enabled", [increase_paint_grid_size_button])
                if paint_grid_cols == paint_grid_size_limit_lower:
                    change_button_color("disabled", [decrease_paint_grid_size_button])
                else:
                    change_button_color("enabled", [decrease_paint_grid_size_button])

            # Lines for Base Tiles "box"
            pygame.draw.line(screen, BLACK, (440, 311), (800, 311))
            pygame.draw.line(screen, BLACK, (440, 311), (440, 640))

            base_tiles_text.draw(screen) 

            if delete_tile_button.draw(screen):
                if not switch_state_cooldown and selected_base_tile != None:
                    if len(base_tile_list) > 1:
                        base_tile_list.remove(base_tile_list[selected_base_tile_index])

                        tiles_in_row = len(base_tile_list) % base_tiles_per_row_limit
                        max_height = 0
                        for tile in base_tile_list[-tiles_in_row:]:
                            if tile.height > max_height:
                                max_height = tile.height
                        base_tile_max_height = max_height

                        base_tile_list = create_tile_list(base_tile_list, tile_list_x_pos, tile_list_y_pos, tile_list_offset, enlargement_scale, base_tiles_per_row_limit)
                        tile_buttons = create_tile_buttons(base_tile_list)

                        if selected_base_tile_index >= len(base_tile_list):
                            selected_base_tile_index -= 1
                        selected_base_tile = tile_buttons[selected_base_tile_index]
                        selected_base_tile_image = selected_base_tile.image.copy()

                        patterns = get_patterns(pattern_size, base_tile_list[selected_base_tile_index])
                        pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                        num_patterns_text = size_17_font.render(f"({len(pattern_tile_list)})", True, SCREEN_TEXT_COLOR)
                        update_patterns(pattern_group, pattern_tile_list, pattern_draw_limit)

                        if len(base_tile_list) == 1:
                            change_button_color("disabled", [delete_tile_button])
                        if len(base_tile_list) == max_base_tiles - 1:
                            change_button_color("enabled", [save_tile_button])

            # Draw yellow border around selected tile
            if selected_base_tile != None:
                draw_selected_tile_border(screen, selected_base_tile)

            # List of selectable Base Tiles
            for index, tile_button in enumerate(tile_buttons):
                if tile_button.draw(screen):
                    if not is_wfc_replay_anim_ongoing and not has_wfc_executed:
                        selected_base_tile = tile_buttons[index]
                        selected_base_tile_index = index
                        selected_base_tile_image = selected_base_tile.image.copy()
                        patterns = get_patterns(pattern_size, base_tile_list[index])
                        pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                        num_patterns_text = size_17_font.render(f"({len(pattern_tile_list)})", True, SCREEN_TEXT_COLOR)
                        update_patterns(pattern_group, pattern_tile_list, pattern_draw_limit)


            if help_button.draw(screen):
                game_state = "help"
                previous_game_state = "paint"


            # if test_paint_button.draw(screen):
            #     paint_grid = create_colored_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_tile_size, base_tile_list[selected_tile_index].pix_array)
            #     paint_grid_pix_array = create_pix_array(paint_grid)
            

            # Draw sprite groups
            paint_color_group.draw(screen)
            hover_box_group.draw(screen)

        # Help state
        if game_state == "help":
            # Draw all help section titles
            for title_text in help_state_title_text_list:
                screen.blit(title_text[0], (10, title_text[1]))

            #Draw all help section paragraphs
            for sub_text in help_state_sub_text_list:
                for y, line in enumerate(sub_text[0]):
                    screen.blit(line, (10, sub_text[1] + y * 15))


            if return_from_help_button.draw(screen):
                game_state = previous_game_state


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Interrupt WFC if window is exited
                wfc_state["interrupt"] = True
                run = False


        pygame.display.update()

        # Needed for WebAssembly embed
        await asyncio.sleep(0)

    # pygame.quit()

async def start_app():
    """Helper function to allow for asyncio features in application."""
    loop = asyncio.get_event_loop()
    await main(loop)

if __name__ == "__main__":
    asyncio.run(start_app())