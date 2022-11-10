import pygame
import random
import math
import time
import sys
from collections import OrderedDict
from tile import Tile
from button import Button
from pattern import Pattern
from rule_index import RuleIndex
from initial_tile import InitialTile
from tile_button import TileButton
from paint_tile import PaintTile


pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

error_font = pygame.font.Font(pygame.font.get_default_font(), 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DARKGREY = (105, 105, 105)
GREY = (175, 175, 175)
LIGHTGREY = (213, 213, 213)

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

RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 50, 255)
DARKBLUE = (0, 0, 155)

LIGHTBLUE = (100, 175, 255)

DARKRED = (150, 0, 0)
color_list = [WHITE, BLACK, DARKGREY, GREY, LIGHTGREY, 
            LAWNGREEN, GREEN, DARKISHGREEN, DARKGREEN, 
            LIGHTYELLOW, YELLOW, GOLD, ORANGE, ORANGEBROWN, KHAKI,
            RED, BLUE, PURPLE, DARKBLUE, 
            LIGHTBLUE, DARKRED]

BACKGROUND_COLOR = GREY

UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)
UP_LEFT = (-1, -1)
UP_RIGHT = (1, -1)
DOWN_LEFT = (-1, 1)
DOWN_RIGHT = (1, 1)
directions = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

sample_pixel_array = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, BLACK),
    (WHITE, BLACK, LIGHTGREY, BLACK),
    (WHITE, BLACK, BLACK, BLACK),
    ]

sample_initial_tile_1 = InitialTile(sample_pixel_array, 4, 4)

sample_pixel_array_5x5 = [
    (WHITE, WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, BLACK, WHITE),
    (WHITE, BLACK, LIGHTGREY, BLACK, GREEN),
    (WHITE, BLACK, BLACK, BLACK, BLACK),
    (GREEN, GREEN, GREEN, GREEN, WHITE)
]

sample_initial_tile_2 = InitialTile(sample_pixel_array_5x5, 5, 5)

sample_pixel_array_5x4 = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, BLACK),
    (WHITE, BLACK, LIGHTGREY, BLACK),
    (WHITE, BLACK, BLACK, GREEN),
    (WHITE, BLACK, BLACK, GREEN)
]

sample_initial_tile_3 = InitialTile(sample_pixel_array_5x4, 5, 4)

sample_pixel_array_3x4 = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, LIGHTGREY, LIGHTGREY, GREEN),
    (WHITE, LIGHTGREY, WHITE, GREEN)
]

sample_initial_tile_4 = InitialTile(sample_pixel_array_3x4, 3, 4)

sample_pixel_array_3x3 = [
    (WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK),
    (WHITE, BLACK, GREEN)
]

sample_initial_tile_5 = InitialTile(sample_pixel_array_3x3, 3, 3)

sample_pixel_array_5x4_test = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, GREEN),
    (WHITE, BLACK, WHITE, GREEN)
]

sample_initial_tile_6 = InitialTile(sample_pixel_array_5x4_test, 5, 4)

sample_pixel_array_4x4_test = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, GREEN),
    (WHITE, BLACK, WHITE, GREEN)
    ]

sample_initial_tile_7 = InitialTile(sample_pixel_array_4x4_test, 4, 4)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_group = pygame.sprite.Group()
pattern_group = pygame.sprite.Group()
completed_wfc_pattern_group = pygame.sprite.Group()
wfc_animation_group = pygame.sprite.Group()
paint_grid_tile_group = pygame.sprite.Group()
paint_color_group = pygame.sprite.Group()

def get_rotated_pix_array(pix_array):
    rotated_pix_array_270 = tuple(zip(*pix_array[::-1]))
    rotated_pix_array_180 = tuple(zip(*rotated_pix_array_270[::-1]))
    rotated_pix_array_90 = tuple(zip(*rotated_pix_array_180[::-1]))
    pix_array = tuple(pix_array)
    return (pix_array, rotated_pix_array_90, rotated_pix_array_180, rotated_pix_array_270)

def get_offset_tiles(pattern, offset):
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

def get_valid_directions(position, output_width, output_height):
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

def get_patterns(pattern_size, initial_tile):
    pattern_list = []

    occurence_weights = {}
    probability = {}

    pix_array = initial_tile.pix_array

    for row in range(initial_tile.width - (pattern_size - 1)):
        for col in range(initial_tile.height - (pattern_size - 1)):
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
        
    unique_pattern_list = []
    for pattern in pattern_list:
        if pattern not in unique_pattern_list:
            unique_pattern_list.append(pattern)
    pattern_list = unique_pattern_list

    sum_of_weights = 0
    for weight in occurence_weights:
        sum_of_weights += occurence_weights[weight]

    for pattern in pattern_list:
        probability[pattern] = occurence_weights[pattern] / sum_of_weights

    pattern_list = [Pattern(pattern) for pattern in pattern_list]
    occurence_weights = {pattern:occurence_weights[pattern.pix_array] for pattern in pattern_list}
    probability = {pattern:probability[pattern.pix_array] for pattern in pattern_list}

    return pattern_list, occurence_weights, probability


def initialize_wave_function(pattern_list, output_width, output_height):
    coefficients = []
    
    for col in range(output_width):
        row = []
        for r in range(output_height):
            row.append(pattern_list)
        coefficients.append(row)

    return coefficients

def is_wave_function_fully_collapsed(coefficients):
    """Check if wave function is fully collapsed meaning that for each tile available is only one pattern"""
    for col in coefficients:
        for entry in col:
            if len(entry) > 1:
                return False
    return True

def get_possible_patterns_at_position(position, coefficients):
    """Return possible patterns at position (x, y)"""
    x, y = position
    possible_patterns = coefficients[x][y]
    return possible_patterns

def get_shannon_entropy(position, coefficients, probability):
    """Calcualte the Shannon Entropy of the wavefunction at position (x, y)"""
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

def get_min_entropy_at_pos(coefficients, probability):
    """Return position of tile with the lowest entropy"""
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

def observe(coefficients, probability):
    # Find the lowest entropy
    min_entropy_pos = get_min_entropy_at_pos(coefficients, probability)
    
    if min_entropy_pos == None:
        print("All tiles have 0 entropy")
        return
    
    # Choose a pattern at lowest entropy position which is most frequent in the sample
    possible_patterns = get_possible_patterns_at_position(min_entropy_pos, coefficients)
    
    # calculate max probability for patterns that are left
    max_p = 0
    for pattern in possible_patterns:
        if max_p < probability[pattern]:
            max_p == probability[pattern]
    
    
    semi_random_pattern = random.choice([pat for pat in possible_patterns if probability[pat]>=max_p])
    
    # Set this pattern to be the only available at this position
    coefficients[min_entropy_pos[0]][min_entropy_pos[1]] = semi_random_pattern

    return min_entropy_pos


def propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, order, order_dict):
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
                # asd = (possible_pattern_at_adjacent.pix_array, pos)
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
                    for patt in coefficients[x][y]:
                        if order_dict.get((x,y)) is not None:
                            del order_dict[(x,y)]
                        order_dict[(x,y)] = patt.pix_array
                        # order.append((patt.pix_array, x, y))
                    order.append((coefficients[x][y][-1].pix_array, x, y))
                        
                    if adjacent_pos not in stack:
                        stack.append(adjacent_pos)
    
    


def execute_wave_function_collapse(patterns, output_width, output_height):
    pattern_list = patterns[0]
    occurence_weights = patterns[1]
    probability = patterns[2]

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

    order = []

    order_dict = OrderedDict()

    perf_time_start = time.monotonic()
    print("Wave Function Collapse Started")

    wfc_completed = True

    # Actual start of WFC
    try:
        while not is_wave_function_fully_collapsed(coefficients):
            min_entropy_pos = observe(coefficients, probability)
            propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, order, order_dict)
    except Exception as e:
        wfc_completed = False
        print("WFC FAIL: ", e)
    perf_time_end = time.monotonic()
    print(f"Wave Function Collapse Ended After {(perf_time_end - perf_time_start):.3f}s")

    new_order = swap_x_y_order(order)
    new_order_dict = swap_x_y_order_dict(order_dict)

    if wfc_completed:
        final_pixels = []

        for i in coefficients:
            row = []
            for j in i:
                if isinstance(j, list):
                    first_pixel = j[0].pix_array[0][0]
                else:
                    first_pixel = j.pix_array[0][0]
                row.append(first_pixel)
            final_pixels.append(row)
        return final_pixels, new_order_dict, new_order
    return None, new_order_dict, new_order

def swap_x_y_order(order):
    new_order = []
    for o in order:
        swapped = ((o[0][0][0],o[0][1][0]),(o[0][0][1],o[0][1][1]))
        new_order.append([swapped, o[1], o[2]])
    return new_order

def swap_x_y_order_dict(order_dict):
    new_order_dict = OrderedDict()
    for k, v in order_dict.items():
        swapped = ((v[0][0],v[1][0]),(v[0][1],v[1][1]))
        new_order_dict[k] = swapped
    return new_order_dict


def draw_window():
    screen.fill(BACKGROUND_COLOR)

def draw_grid(pix_array, output_width, output_height):
    for row in range(output_width):
        for col in range(output_height):
            tile = Tile(output_width, output_height, (col * output_width + 50), (row * output_height + 50), pix_array)
            tile_group.add(tile)

def draw_patterns(pattern_list):
    pattern_group.empty()
    for pattern in pattern_list:
        pattern_group.add(pattern)

def get_pattern_tiles(patterns, pattern_size, enlargement_scale):
    x = 50
    y = 25
    col_limit = 16
    tile_list = []
    for col in range(len(patterns)):
        if col % col_limit == 0 and col > 1:
            y += 25
            x -= col_limit * (pattern_size + 25)
        tile = Tile(pattern_size, pattern_size, (col * (pattern_size + 25) + x), y, patterns[col].pix_array, enlargement_scale)
        tile_list.append(tile)
    return tile_list

make_grid_button = Button(WHITE, 600, 50, 150, 40, "Make Grid", BLACK, LIGHTGREY)
test_button = Button(WHITE, 600, 550, 150, 40, "TEST", BLACK, LIGHTGREY)
draw_test_button = Button(WHITE, 600, 450, 150, 40, "DRAW TEST", BLACK, LIGHTGREY)
switch_state_button = Button(WHITE, 50, 550, 150, 40, "SWITCH STATE", BLACK, LIGHTGREY)

save_tile_button = Button(WHITE, 50, 450, 150, 40, "Save Tile", BLACK, LIGHTGREY)
toggle_grid_lines_button = Button(WHITE, 250, 450, 200, 40, "Toggle Grid Lines", BLACK, LIGHTGREY)


white_button = Button(WHITE, 600, 50, 150, 40, "WHITE", BLACK, LIGHTGREY)
black_button = Button(WHITE, 600, 150, 150, 40, "BLACK", BLACK, LIGHTGREY)
grey_button = Button(WHITE, 600, 250, 150, 40, "GREY", BLACK, LIGHTGREY)
green_button = Button(WHITE, 600, 350, 150, 40, "GREEN", BLACK, LIGHTGREY)

def create_tile_buttons(initial_tile_list):
    tile_buttons = []
    for tile in initial_tile_list:
        tile_button = TileButton(tile.x, tile.y, tile.image)
        tile_buttons.append(tile_button)
    return tile_buttons

def draw_selected_tile_border(tile):
    if tile is not None:
        pygame.draw.rect(screen, YELLOW, (tile.x-5, tile.y-5, tile.width + 10, tile.height + 10), 5)

def show_prob(patterns):
    count = 1
    for pattern, prob in patterns[2].items():
        print(count, pattern.pix_array, prob)
        count += 1

def get_pattern_dict(pattern_list):
    pattern_dict = {}
    pattern_list = swap_pattern_x_y(pattern_list)
    for pattern in pattern_list:
        pattern_dict[pattern.pix_array] = (pattern.x, pattern.y)
    return pattern_dict

def swap_pattern_x_y(pattern_list):
    new_list = []
    for pattern in pattern_list:
        swapped = ((pattern.pix_array[0][0], pattern.pix_array[1][0]),(pattern.pix_array[0][1], pattern.pix_array[1][1]))
        pattern.pix_array = swapped
        new_list.append(pattern)
    return new_list

def highlight_pattern(pattern, pattern_size, enlargement_scale):
    pygame.draw.rect(screen, YELLOW, (pattern[0]-5, pattern[1]-5, pattern_size*enlargement_scale + 10, pattern_size*enlargement_scale + 10), 5)

def create_empty_paint_grid(x_pos, y_pos, cols, rows, tile_size):
    grid = []
    for col in range(cols):
        new_row = []
        for row in range(rows):
            tile = PaintTile(tile_size, tile_size, (x_pos + tile_size * col), (y_pos + tile_size * row), GREEN)
            new_row.append(tile)
        grid.append(new_row)
    return grid

def create_pix_array(paint_grid):
    pix_array = []
    for col in paint_grid:
        new_row = []
        for tile in col:
            new_row.append(tile.color)
        pix_array.append(tuple(new_row))
    return pix_array

def create_paint_color_tiles():
    y = 20
    x = 20
    col_limit = 15
    color_tile_list = []
    for col in range(30):
        if col % col_limit == 0 and col > 1:
            y += 33
            x -= col * 33
        x += 33
        if col < len(color_list):
            color_tile = PaintTile(30, 30, x, y, (color_list[col]))
        else:
            color_tile = PaintTile(30, 30, x, y, GREY)
        color_tile_list.append(color_tile)
    return color_tile_list


def main():
    run = True

    is_grid_drawn = False

    draw_test_grid = False

    wfc_output = None

    wfc_render_pattern_count = 0

    test_wfc_output = None
    test_wfc_output_length = 0

    wfc_render_pattern_list = []

    enlargement_scale = 8

    initial_tile_list = []
    tile_list_x_pos = 50
    tile_list_x_offset = 16
    tile_list_y_pos = 350

    grid_x_pos = 50
    grid_y_pos = 100
    test_grid_x_pos = 300
    test_grid_y_pos = 100

    sample_tile_1 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_1)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
    sample_tile_2 = Tile(sample_initial_tile_2.width, sample_initial_tile_2.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_2.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_2)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
    sample_tile_3 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_3)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
    sample_tile_4 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_4)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
    sample_tile_5 = Tile(sample_initial_tile_2.width, sample_initial_tile_2.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_2.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_5)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset

    sample_tile_6 = Tile(sample_initial_tile_3.width, sample_initial_tile_3.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_3.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_6)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset

    sample_tile_7 = Tile(sample_initial_tile_4.width, sample_initial_tile_4.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_4.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_7)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
    
    sample_tile_8 = Tile(sample_initial_tile_5.width, sample_initial_tile_5.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_5.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_8)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset

    sample_tile_9 = Tile(sample_initial_tile_6.width, sample_initial_tile_6.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_6.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_9)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset

    sample_tile_10 = Tile(sample_initial_tile_7.width, sample_initial_tile_7.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_7.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_10)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset

    pattern_size = 2

    patterns = get_patterns(pattern_size, initial_tile_list[0])

    pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)

    pattern_dict = get_pattern_dict(pattern_tile_list)

    output_width = 30
    output_height = 30

    tile_buttons = create_tile_buttons(initial_tile_list)   

    selected_tile = tile_buttons[0]

    error_msg = error_font.render("WAVE FUNCTION COLLAPSE FAILED", True, (255, 0, 0))
    render_error_msg = False

    test_wfc_list = []
    wfc_list_count = 0

    hide_out_of_bounds = True

    game_state = "paint"

    paint_grid_x_pos = 50
    paint_grid_y_pos = 120

    paint_grid_tile_size = 50

    paint_grid_cols = 4
    paint_grid_rows = 4

    paint_grid = create_empty_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_cols, paint_grid_rows, paint_grid_tile_size)

    paint_grid_pix_array = create_pix_array(paint_grid)

    current_color = WHITE

    preview_tile = Tile(paint_grid_cols, paint_grid_rows, 50, 400, paint_grid_pix_array, enlargement_scale)

    draw_paint_grid_lines = True

    color_panel = create_paint_color_tiles()

    while run:
        clock.tick(FPS)
        draw_window()
        
        draw_patterns(pattern_tile_list)

        if game_state == "wfc":

            if is_grid_drawn:
                tile_group.add(wfc_output)

            if make_grid_button.draw(screen):
                completed_wfc_pattern_group.empty()
                wfc_render_pattern_list = []
                wfc_render_pattern_count = 0
                wfc_animation_group.empty()
                wfc_list_count = 0
                render_error_msg = False
                get_wfc_output = execute_wave_function_collapse(patterns, output_width, output_height)
                if get_wfc_output[0] is not None:
                    wfc_output = Tile(output_width, output_height, grid_x_pos, grid_y_pos, get_wfc_output[0], enlargement_scale)
                    is_grid_drawn = True  
                else:
                    render_error_msg = True

                test_wfc_output = get_wfc_output[1]
                test_wfc_output_length = len(test_wfc_output)

                test_wfc_list = get_wfc_output[2]
                draw_test_grid = True

            if render_error_msg:
                screen.blit(error_msg, (50, 300))

            # Original tiles
            for index, tile_button in enumerate(tile_buttons):
                if tile_button.draw(screen):
                    selected_tile = tile_buttons[index]
                    patterns = get_patterns(pattern_size, initial_tile_list[index])
                    pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                    pattern_dict = get_pattern_dict(pattern_tile_list)
                    print(len(patterns[0]))

            draw_selected_tile_border(selected_tile)

            # Animation
            if draw_test_grid:
                # Order list
                # if wfc_list_count < len(test_wfc_list):
                #     new_tile = Tile(pattern_size, pattern_size, test_grid_x_pos+test_wfc_list[wfc_list_count][1]*enlargement_scale, test_grid_y_pos+test_wfc_list[wfc_list_count][2]*enlargement_scale, test_wfc_list[wfc_list_count][0], enlargement_scale)
                #     wfc_animation_group.add(new_tile)
                #     wfc_list_count += 1
                # Order dict
                if wfc_render_pattern_count < test_wfc_output_length:
                    new_tile = test_wfc_output.popitem(last=False)
                    wfc_render_pattern_list.append(Tile(pattern_size, pattern_size, test_grid_x_pos+new_tile[0][0]*enlargement_scale, test_grid_y_pos+new_tile[0][1]*enlargement_scale, new_tile[1], enlargement_scale))
                    completed_wfc_pattern_group.add(wfc_render_pattern_list[wfc_render_pattern_count])
                    highlight_pattern(pattern_dict[new_tile[1]], pattern_size, enlargement_scale)
                    wfc_render_pattern_count += 1

            if draw_test_button.draw(screen):
                if wfc_render_pattern_count < test_wfc_output_length:
                    new_tile = test_wfc_output.popitem(last=False)
                    wfc_render_pattern_list.append(Tile(pattern_size, pattern_size, test_grid_x_pos+new_tile[0][0]*enlargement_scale, test_grid_y_pos+new_tile[0][1]*enlargement_scale, new_tile[1], enlargement_scale))
                    completed_wfc_pattern_group.add(wfc_render_pattern_list[wfc_render_pattern_count])
                    wfc_render_pattern_count += 1

            if test_button.draw(screen):
                pass

            pattern_group.draw(screen)
            tile_group.draw(screen)
            completed_wfc_pattern_group.draw(screen)
            wfc_animation_group.draw(screen)
            
            if hide_out_of_bounds:
                pygame.draw.rect(screen, BACKGROUND_COLOR, ((test_grid_x_pos + output_width * enlargement_scale), test_grid_y_pos, (pattern_size * enlargement_scale), (output_height * enlargement_scale + 1)))
                pygame.draw.rect(screen, BACKGROUND_COLOR, (test_grid_x_pos, (output_height * enlargement_scale + 1 + test_grid_y_pos), (output_width * enlargement_scale + pattern_size*enlargement_scale), (pattern_size * enlargement_scale)))

            # Grid border
            pygame.draw.rect(screen, BLACK, (grid_x_pos-1, grid_y_pos-1, (output_width * enlargement_scale) + 2, (output_height * enlargement_scale) + 2), 1)
            # TEST GRID BORDER
            pygame.draw.rect(screen, BLACK, (test_grid_x_pos-1, test_grid_y_pos-1, (output_width * enlargement_scale) + 2, (output_height * enlargement_scale) + 2), 1)
        
            if switch_state_button.draw(screen):
                game_state = "paint"

        if game_state == "paint":

            for color in color_panel:
                if color.draw(screen, border=True):
                    current_color = color.color

            # Draw grid 
            for x, col in enumerate(paint_grid):
                for y, tile in enumerate(col):
                    if tile.draw(screen):
                        paint_grid[x][y] = PaintTile(paint_grid_tile_size, paint_grid_tile_size, paint_grid[x][y].x, paint_grid[x][y].y, current_color)

                        paint_grid_pix_array = create_pix_array(paint_grid)
                        preview_tile = Tile(paint_grid_cols, paint_grid_rows, 50, 400, paint_grid_pix_array, enlargement_scale)

            # Grid border
            pygame.draw.rect(screen, BLACK, (paint_grid_x_pos-1, paint_grid_y_pos-1, (paint_grid_cols * paint_grid_tile_size + 2), (paint_grid_rows * paint_grid_tile_size) + 2), 1)

            if white_button.draw(screen):
                current_color = WHITE

            if black_button.draw(screen):
                current_color = BLACK

            if grey_button.draw(screen):
                current_color = LIGHTGREY

            if green_button.draw(screen):
                current_color = GREEN  

            if save_tile_button.draw(screen):
                new_tile_button = Tile(paint_grid_cols, paint_grid_rows, tile_list_x_pos, tile_list_y_pos, paint_grid_pix_array, enlargement_scale)
                initial_tile_list.append(new_tile_button)
                tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
                tile_buttons = create_tile_buttons(initial_tile_list)

                selected_tile = tile_buttons[-1]
                patterns = get_patterns(pattern_size, initial_tile_list[-1])
                pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                pattern_dict = get_pattern_dict(pattern_tile_list)
                
                game_state = "wfc"

            screen.blit(preview_tile.image, (preview_tile.x, preview_tile.y))

            if switch_state_button.draw(screen):
                game_state = "wfc"
            
            paint_grid_tile_group.draw(screen)

            if draw_paint_grid_lines:
                for col in range(1, paint_grid_cols):
                    pygame.draw.line(screen, BLACK, (paint_grid_x_pos + col * paint_grid_tile_size, paint_grid_y_pos), (paint_grid_x_pos + col * paint_grid_tile_size, paint_grid_y_pos + paint_grid_tile_size * paint_grid_rows))
                for row in range(1, paint_grid_rows):
                    pygame.draw.line(screen, BLACK, (paint_grid_x_pos, paint_grid_y_pos + row * paint_grid_tile_size), (paint_grid_x_pos + paint_grid_tile_size * paint_grid_cols, paint_grid_y_pos + row * paint_grid_tile_size))

            if toggle_grid_lines_button.draw(screen):
                draw_paint_grid_lines = not draw_paint_grid_lines

            paint_color_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()