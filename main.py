import pygame
import random
import math
import time
import sys
import threading
import queue
import traceback
from copy import deepcopy
from collections import OrderedDict
from tile import Tile
from button import Button
from pattern import Pattern
from rule_index import RuleIndex
from initial_tile import InitialTile
from tile_button import TileButton
from paint_tile import PaintTile


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

color_list = [WHITE, LIGHTGREY, GREY, DARKGREY, BLACK,
            DARKBROWN, BROWN, LIGHTBROWN, ORANGEBROWN, 
            KHAKI, LIGHTYELLOW, YELLOW, GOLD, ORANGE, 
            ORANGERED, RED, DARKRED, CRIMSON, PINK,
            LIGHTISHPINK, LIGHTPINK, LIGHTPURPLE, PURPLE,
            DARKPURPLE, DARKBLUE, BLUE, LIGHTISHBLUE, LIGHTBLUE,
            CYAN, LIGHTGREEN, GREEN, LAWNGREEN,  DARKISHGREEN, DARKGREEN]

BACKGROUND_COLOR = (155, 155, 155)

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

def get_rotated_pix_array(pix_array):
    rotated_pix_array_270 = tuple(zip(*pix_array[::-1]))
    rotated_pix_array_180 = tuple(zip(*rotated_pix_array_270[::-1]))
    rotated_pix_array_90 = tuple(zip(*rotated_pix_array_180[::-1]))

    if len(pix_array) == 2:
        vertically_flipped_pix_array = tuple(pix_array[0][::-1]), tuple(pix_array[-1][::-1])
    elif len(pix_array) == 3:
        vertically_flipped_pix_array = tuple(pix_array[0][::-1]), tuple(pix_array[1][::-1]), tuple(pix_array[-1][::-1])

    horizontally_flipped_pix_array = tuple(pix_array[::-1])

    pix_array = tuple(pix_array)
    # return (pix_array, rotated_pix_array_90, rotated_pix_array_180, rotated_pix_array_270)
    return (pix_array, rotated_pix_array_90, rotated_pix_array_180, rotated_pix_array_270, vertically_flipped_pix_array, horizontally_flipped_pix_array)


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

def observe(coefficients, probability, coefficients_state):
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
    current_coefficients = deepcopy(coefficients)
    coefficients_state.append(current_coefficients)

    return min_entropy_pos


def propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, coefficients_state):
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
                    current_coefficients = deepcopy(coefficients)
                    coefficients_state.append(current_coefficients)
                        
                    if adjacent_pos not in stack:
                        stack.append(adjacent_pos)
    
    


def execute_wave_function_collapse(patterns, output_width, output_height, thread_queue, render_wfc_during_execution):
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

    perf_time_start = time.perf_counter()
    print("Wave Function Collapse Started")

    wfc_completed = True

    coefficients_state = []

    # Actual start of WFC
    try:
        while not is_wave_function_fully_collapsed(coefficients):
            if render_wfc_during_execution:
                thread_queue.put(deepcopy(coefficients))

            min_entropy_pos = observe(coefficients, probability, coefficients_state)

            if render_wfc_during_execution:
                thread_queue.put(deepcopy(coefficients))

            propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, coefficients_state)
            
            if render_wfc_during_execution:
                thread_queue.put(deepcopy(coefficients))


    except Exception as e:
        wfc_completed = False
        # print("WFC FAIL: ", e)
        traceback.print_exc()
    perf_time_end = time.perf_counter()
    # thread_queue.put(round((perf_time_end - perf_time_start), 3))
    print(f"Wave Function Collapse Ended After {(perf_time_end - perf_time_start):.3f}s")

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
        thread_queue.put([True, final_pixels, coefficients_state, round((perf_time_end - perf_time_start), 3)])
    else:
        final_pixels = []
        for i in coefficients: 
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
        thread_queue.put([False, final_pixels, coefficients_state, round((perf_time_end - perf_time_start), 3)]) 


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

def draw_window(screen):
    screen.fill(BACKGROUND_COLOR)


def draw_patterns(pattern_group, pattern_list, screen, enlargement_scale):
    pattern_group.empty()
    for pattern in pattern_list:
        pattern_group.add(pattern)
        pygame.draw.rect(screen, (0, 0, 0), (pattern.x - 1, pattern.y - 1, pattern.width * enlargement_scale + 2, pattern.height * enlargement_scale + 2), 1)

def get_pattern_tiles(patterns, pattern_size, enlargement_scale):
    y_offset = 30
    x_offset = 25
    if pattern_size == 3:
        y_offset = 38
        x_offset = 33
    x = 50
    y = 25
    col_limit = 15
    tile_list = []

    for col in range(len(patterns)):
        if col % col_limit == 0 and col > 1:
            y += y_offset
            x -= col_limit * (pattern_size + x_offset)
        tile = Tile(pattern_size, pattern_size, (col * (pattern_size + x_offset) + x), y, patterns[col].pix_array, enlargement_scale)
        tile_list.append(tile)
    return tile_list, y+y_offset-2

def create_tile_buttons(initial_tile_list):
    tile_buttons = []
    for tile in initial_tile_list:
        tile_button = TileButton(tile.x, tile.y, tile.image)
        tile_buttons.append(tile_button)
    return tile_buttons

def draw_selected_tile_border(screen, tile):
    if tile is not None:
        pygame.draw.rect(screen, YELLOW, (tile.x-5, tile.y-5, tile.width + 10, tile.height + 10), 4)

def show_prob(patterns):
    count = 1
    for pattern, prob in patterns[2].items():
        print(count, pattern.pix_array, prob)
        count += 1

def get_pattern_dict(pattern_list):
    pattern_dict = {}
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

def create_empty_paint_grid(x_pos, y_pos, cols, rows, tile_size):
    grid = []
    for col in range(cols):
        new_row = []
        for row in range(rows):
            tile = PaintTile(tile_size, tile_size, (x_pos + tile_size * col), (y_pos + tile_size * row), WHITE)
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
    y = 10
    x = 17
    col_limit = 17
    color_tile_list = []
    for col in range(34):
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

def get_grid_size_text_color(size):
    if size < 15:
        return GREEN
    elif size >= 15 and size < 22:
        return YELLOW
    return DARKRED

def test_threading():
    time.sleep(2)
    print("TEST")

def main():
    pygame.init()

    error_font = pygame.font.Font(pygame.font.get_default_font(), 24)
    info_font = pygame.font.Font(pygame.font.get_default_font(), 20)
    probability_font = pygame.font.Font(pygame.font.get_default_font(), 10)

    WIDTH = 800
    HEIGHT = 640

    clock = pygame.time.Clock()
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    tile_group = pygame.sprite.Group()
    pattern_group = pygame.sprite.Group()
    completed_wfc_pattern_group = pygame.sprite.Group()
    paint_grid_tile_group = pygame.sprite.Group()
    paint_color_group = pygame.sprite.Group()

    make_grid_button = Button(WHITE, 600, 50, 150, 40, "Make Grid", BLACK, LIGHTGREY)
    test_button = Button(WHITE, 600, 100, 150, 40, "TEST", BLACK, LIGHTGREY)

    switch_state_button = Button(WHITE, 630, 580, 150, 40, "SWITCH STATE", BLACK, LIGHTGREY)

    increase_output_size_button = Button(WHITE, 570, 200, 210, 40, "Increase Grid Size", BLACK, LIGHTGREY)
    decrease_output_size_button = Button(WHITE, 570, 250, 210, 40, "Decrease Grid Size", BLACK, LIGHTGREY)

    set_pattern_size_2_button = Button(WHITE, 570, 400, 200, 40, "Set Pattern Size 2", BLACK, LIGHTGREY)
    set_pattern_size_3_button = Button(WHITE, 570, 450, 200, 40, "Set Pattern Size 3", BLACK, LIGHTGREY)

    toggle_show_probability_button = Button(WHITE, 550, 500, 230, 40, "Hide Pattern Probability", BLACK, LIGHTGREY)

    replay_animation_button = Button(WHITE, 570, 300, 210, 40, "Replay WFC Animation", BLACK, LIGHTGREY)
    skip_animation_button = Button(WHITE, 570, 350, 210, 40, "Skip WFC Animation", BLACK, LIGHTGREY)

    toggle_anim_during_wfc_button = Button(WHITE, 520, 560, 50, 20, "Change", BLACK, LIGHTGREY, small_text=True)
    toggle_anim_after_wfc_button = Button(WHITE, 520, 590, 50, 20, "Change", BLACK, LIGHTGREY, small_text=True)

    increase_nth_button = Button(WHITE, 480, 510, 50, 16, "Increase", BLACK, LIGHTGREY, small_text=True)
    decrease_nth_button = Button(WHITE, 480, 528, 50, 16, "Decrease", BLACK, LIGHTGREY, small_text=True)

    test_paint_button = Button(WHITE, 600, 550, 150, 40, "TEST", BLACK, LIGHTGREY)

    increase_pattern_size_button = Button(WHITE, 580, 450, 210, 40, "Increase Pattern Size", BLACK, LIGHTGREY)
    decrease_pattern_size_button = Button(WHITE, 580, 400, 210, 40, "Decrease Pattern Size", BLACK, LIGHTGREY)
    save_tile_button = Button(WHITE, 50, 450, 150, 40, "Save Tile", BLACK, LIGHTGREY)
    toggle_grid_lines_button = Button(WHITE, 250, 450, 200, 40, "Toggle Grid Lines", BLACK, LIGHTGREY)

    run = True

    is_grid_drawn = False

    draw_second_grid = False

    wfc_output = None

    enlargement_scale = 8

    initial_tile_list = []
    tile_list_x_pos = 50
    tile_list_x_offset = 16
    tile_list_y_pos = 400

    sample_tile_1 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_1)
    tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
    sample_tile_2 = Tile(sample_initial_tile_2.width, sample_initial_tile_2.height, tile_list_x_pos, tile_list_y_pos, sample_initial_tile_2.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_2)


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

    selected_tile_index = 0

    patterns = get_patterns(pattern_size, initial_tile_list[selected_tile_index])
    
    pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)

    pattern_tile_list = pattern_list[0]

    pattern_dict = get_pattern_dict(pattern_tile_list)

    grid_x_pos = 50
    grid_y_pos = pattern_list[1]
    second_grid_x_pos = 300
    second_grid_y_pos = pattern_list[1]

    output_width = 20
    output_height = 20

    tile_buttons = create_tile_buttons(initial_tile_list)   

    selected_tile = tile_buttons[selected_tile_index]

    wfc_order_list = []
    wfc_list_count = 0

    game_state = "wfc"

    paint_grid_x_pos = 50
    paint_grid_y_pos = 120

    paint_grid_tile_size = 50

    paint_grid_cols = 4
    paint_grid_rows = 4
    paint_grid_size_limit_upper = 9
    paint_grid_size_limit_lower = 3

    paint_grid = create_empty_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_cols, paint_grid_rows, paint_grid_tile_size)

    paint_grid_pix_array = create_pix_array(paint_grid)

    current_color = WHITE

    current_color_tile = PaintTile(30, 30, 200, 80, current_color)

    preview_tile = Tile(paint_grid_cols, paint_grid_rows, 50, 400, paint_grid_pix_array, enlargement_scale)

    draw_paint_grid_lines = True

    color_panel = create_paint_color_tiles()

    tile_col_limit = 8

    wfc_slice_num = 5

    is_wfc_anim_ongoing = False

    grid_size_text_color = get_grid_size_text_color(output_width)

    prob_text_x_offset = -2
    prob_text_y_offset = -11

    show_probability = True

    get_wfc_output = None

    standard_threads = threading.active_count()
    is_wfc_started = False

    is_wfc_finished = False
    
    thread_queue = queue.Queue()

    wfc_time_start = 0
    wfc_time_finish = 0

    did_wfc_fail = False

    render_wfc_during_execution = True
    render_wfc_at_end = True

    anim_during_wfc_info_text = info_font.render("Show current state of WFC during execution:", True, BLACK)
    anim_after_wfc_info_text = info_font.render("Show animation of WFC after completion:", True, BLACK)
    anim_during_wfc_value_text = info_font.render("Yes", True, GREEN)
    anim_after_wfc_value_text = info_font.render("Yes", True, GREEN)

    sliced_list = []
    last_image = None

    while run:
        clock.tick(FPS)
        draw_window(screen)

        if game_state == "wfc":
            if not threading.active_count() > standard_threads:
                if not thread_queue.empty() and is_wfc_started:
                    result = thread_queue.queue[-1]
                    if result[0]:
                        wfc_output = Tile(output_width, output_height, grid_x_pos, grid_y_pos, result[1], enlargement_scale)
                    else:
                        did_wfc_fail = True
                        wfc_output = Tile(output_width, output_height, grid_x_pos, grid_y_pos, result[1], enlargement_scale)
                    wfc_time_finish = result[3]
                    is_wfc_finished = True
                    is_grid_drawn = True
                    is_wfc_started = False
                    wfc_order_list = result[2]
                    last_image = wfc_order_list[-1]
                    sliced_list = wfc_order_list[::wfc_slice_num]
                    sliced_list.append(last_image)
                    if render_wfc_at_end:
                        wfc_output_2 = Tile(output_width, output_height, second_grid_x_pos, second_grid_y_pos, result[1], enlargement_scale)
                        completed_wfc_pattern_group.add(wfc_output_2)
                        draw_second_grid = True
                        is_wfc_anim_ongoing = True

            else:                
                time_progressed = time.perf_counter() - wfc_time_start
                wfc_in_progress_text = info_font.render(f"Wave Function Collapse In Progress... {round(time_progressed, 3)}s", True, DARKPURPLE)
                screen.blit(wfc_in_progress_text, (48, 370))
                if render_wfc_during_execution and not thread_queue.empty():
                    current_wfc_state = thread_queue.queue[-1]
                    if isinstance(current_wfc_state, list):

                        final_pixels = []

                        for i in current_wfc_state:
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

                        wfc_output = Tile(output_width, output_height, grid_x_pos, grid_y_pos, final_pixels, enlargement_scale)
                        completed_wfc_pattern_group.add(wfc_output)


            if is_wfc_finished:
                if not did_wfc_fail:
                    wfc_finished_text = info_font.render(f"Wave Function Collapse Finished After {wfc_time_finish}s", True, LAWNGREEN)
                    screen.blit(wfc_finished_text, (48, 370))
                else:
                    wfc_failed_text = info_font.render(f"Wave Function Collapse Failed After {wfc_time_finish}s", True, CRIMSON)
                    screen.blit(wfc_failed_text, (48, 370))

            draw_patterns(pattern_group, pattern_tile_list, screen, enlargement_scale)
        
            if show_probability:
                prob_text = probability_font.render("Pattern Probability", True, DARKPURPLE)
                screen.blit(prob_text, (48, 3))
                for patt in patterns[0]:
                    patt_prob = probability_font.render("{0:.2f}".format(round(patterns[2][patt], 2)), True, DARKPURPLE)
                    screen.blit(patt_prob, (pattern_dict[patt.pix_array][0] + prob_text_x_offset, pattern_dict[patt.pix_array][1] + prob_text_y_offset))

            if is_grid_drawn:
                tile_group.add(wfc_output)

            if make_grid_button.draw(screen):
                if not is_wfc_started:
                    completed_wfc_pattern_group.empty()
                    tile_group.empty()
                    thread_queue = queue.Queue()
                    wfc_list_count = 0
                    is_grid_drawn = False
                    did_wfc_fail = False
                    is_wfc_anim_ongoing = False
                    is_wfc_started = True
                    is_wfc_finished = False
                    wfc_time_start = time.perf_counter()
                    get_wfc_output = threading.Thread(target=execute_wave_function_collapse, args=(patterns, output_width, output_height, thread_queue, render_wfc_during_execution))
                    get_wfc_output.start()

            current_grid_size_text = info_font.render(f"Grid Size: ", True, (0, 0, 0))
            grid_size_text = info_font.render(f"{output_width} x {output_height}", True, grid_size_text_color)

            screen.blit(current_grid_size_text, (580, 175))
            screen.blit(grid_size_text, (685, 175))
            
            if increase_output_size_button.draw(screen):
                if not is_wfc_anim_ongoing and output_width < 30 and not is_wfc_started:
                    output_width += 1
                    output_height += 1
                    grid_size_text_color = get_grid_size_text_color(output_width)
            if decrease_output_size_button.draw(screen):
                if not is_wfc_anim_ongoing and output_width > 10 and not is_wfc_started:
                    output_width -= 1
                    output_height -= 1
                    grid_size_text_color = get_grid_size_text_color(output_width)


            # Original tiles
            for index, tile_button in enumerate(tile_buttons):
                if tile_button.draw(screen):
                    selected_tile = tile_buttons[index]
                    selected_tile_index = index
                    patterns = get_patterns(pattern_size, initial_tile_list[index])
                    pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                    pattern_tile_list = pattern_list[0]
                    pattern_dict = get_pattern_dict(pattern_tile_list)
                    grid_y_pos = pattern_list[1]
                    second_grid_y_pos = pattern_list[1]
                    print(len(patterns[0]))

            draw_selected_tile_border(screen, selected_tile)

            # Animation
            if draw_second_grid:
                if is_wfc_anim_ongoing:
                    if wfc_list_count < len(sliced_list):
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

                        wfc_output_2 = Tile(output_width, output_height, second_grid_x_pos, second_grid_y_pos, final_pixels, enlargement_scale)
                        completed_wfc_pattern_group.add(wfc_output_2)
                        wfc_list_count += 1
                    if wfc_list_count == len(sliced_list):
                        is_wfc_anim_ongoing = False

            if replay_animation_button.draw(screen):
                if not is_wfc_anim_ongoing and not is_wfc_started and len(wfc_order_list) > 0:
                    wfc_list_count = 0
                    is_wfc_anim_ongoing = True

            if skip_animation_button.draw(screen):
                if is_wfc_anim_ongoing:
                    wfc_list_count = len(sliced_list) - 1

            if test_button.draw(screen):
                print(thread_queue.qsize())

            if toggle_show_probability_button.draw(screen):
                if show_probability:
                    show_probability = False
                    toggle_show_probability_button.text = "Show Pattern Probability"
                else:
                    show_probability = True
                    toggle_show_probability_button.text = "Hide Pattern Probability"


            if set_pattern_size_2_button.draw(screen):
                pattern_size = 2
                prob_text_x_offset = -2
                prob_text_y_offset = -11
                patterns = get_patterns(pattern_size, initial_tile_list[selected_tile_index])
                pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                pattern_tile_list = pattern_list[0]
                grid_y_pos = pattern_list[1]
                second_grid_y_pos = pattern_list[1]
                pattern_dict = get_pattern_dict(pattern_tile_list)


            if set_pattern_size_3_button.draw(screen):
                pattern_size = 3
                prob_text_x_offset = 2
                prob_text_y_offset = -11
                patterns = get_patterns(pattern_size, initial_tile_list[selected_tile_index])
                pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                pattern_tile_list = pattern_list[0]
                grid_y_pos = pattern_list[1]
                second_grid_y_pos = pattern_list[1]
                pattern_dict = get_pattern_dict(pattern_tile_list)

            current_speed_text = info_font.render(f"Current Speed:", True, (0, 0, 0))
            screen.blit(current_speed_text, (300, 520))

            
            wfc_slice_num_text = info_font.render(str(wfc_slice_num), True, (0, 0, 255))
            screen.blit(wfc_slice_num_text, (454, 520))
            if increase_nth_button.draw(screen):
                if not is_wfc_anim_ongoing:
                    if wfc_slice_num < 10:
                        wfc_slice_num += 1
                        sliced_list = wfc_order_list[::wfc_slice_num]
                        sliced_list.append(last_image)

            if decrease_nth_button.draw(screen):
                if not is_wfc_anim_ongoing:
                    if wfc_slice_num > 1:
                        wfc_slice_num -= 1
                        sliced_list = wfc_order_list[::wfc_slice_num]
                        sliced_list.append(last_image)

            screen.blit(anim_during_wfc_info_text, (30, 560))
            screen.blit(anim_after_wfc_info_text, (30, 590))
            screen.blit(anim_during_wfc_value_text, (478, 560))
            screen.blit(anim_after_wfc_value_text, (478, 590))

            if toggle_anim_during_wfc_button.draw(screen):
                if not is_wfc_anim_ongoing and not is_wfc_started:
                    if render_wfc_during_execution:
                        render_wfc_during_execution = False
                        anim_during_wfc_value_text = info_font.render("No", True, DARKRED)
                    else:
                        render_wfc_during_execution = True
                        anim_during_wfc_value_text = info_font.render("Yes", True, GREEN)

            if toggle_anim_after_wfc_button.draw(screen):
                if not is_wfc_anim_ongoing and not is_wfc_started:
                    if render_wfc_at_end:
                        render_wfc_at_end = False
                        anim_after_wfc_value_text = info_font.render("No", True, DARKRED)
                    else:
                        render_wfc_at_end = True
                        anim_after_wfc_value_text = info_font.render("Yes", True, GREEN)


            pattern_group.draw(screen)
            tile_group.draw(screen)
            completed_wfc_pattern_group.draw(screen)
            

            # Grid border
            pygame.draw.rect(screen, BLACK, (grid_x_pos-1, grid_y_pos-1, (output_width * enlargement_scale) + 2, (output_height * enlargement_scale) + 2), 1)
            # Second grid border
            pygame.draw.rect(screen, BLACK, (second_grid_x_pos-1, second_grid_y_pos-1, (output_width * enlargement_scale) + 2, (output_height * enlargement_scale) + 2), 1)

            if switch_state_button.draw(screen):
                game_state = "paint"

        if game_state == "paint":
            current_speed_text = info_font.render("Current Color:", True, (0, 0, 0))
            screen.blit(current_speed_text, (50, 86))

            if current_color_tile.draw(screen, border=True):
                pass

            for color in color_panel:
                if color.draw(screen, border=True):
                    current_color = color.color
                    current_color_tile.image.fill(current_color)

            # Draw grid 
            for x, col in enumerate(paint_grid):
                for y, tile in enumerate(col):
                    if tile.draw(screen):
                        paint_grid[x][y] = PaintTile(paint_grid_tile_size, paint_grid_tile_size, paint_grid[x][y].x, paint_grid[x][y].y, current_color)

                        paint_grid_pix_array = create_pix_array(paint_grid)
                        preview_tile = Tile(paint_grid_cols, paint_grid_rows, 50, 400, paint_grid_pix_array, enlargement_scale)

            # Grid border
            pygame.draw.rect(screen, BLACK, (paint_grid_x_pos-1, paint_grid_y_pos-1, (paint_grid_cols * paint_grid_tile_size + 2), (paint_grid_rows * paint_grid_tile_size) + 2), 1) 

            if save_tile_button.draw(screen):
                if len(tile_buttons) % tile_col_limit == 0:
                    tile_list_x_pos = 50
                    tile_list_y_pos += 50
                new_tile_button = Tile(paint_grid_cols, paint_grid_rows, tile_list_x_pos, tile_list_y_pos, paint_grid_pix_array, enlargement_scale)
                initial_tile_list.append(new_tile_button)
                tile_list_x_pos += initial_tile_list[-1].width * enlargement_scale + tile_list_x_offset
                tile_buttons = create_tile_buttons(initial_tile_list)

                selected_tile = tile_buttons[-1]
                selected_tile_index = len(tile_buttons)-1
                patterns = get_patterns(pattern_size, initial_tile_list[-1])
                pattern_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)
                pattern_tile_list = pattern_list[0]
                pattern_dict = get_pattern_dict(pattern_tile_list)
                grid_y_pos = pattern_list[1]
                second_grid_y_pos = pattern_list[1]
                
                game_state = "wfc"

            screen.blit(preview_tile.image, (preview_tile.x, preview_tile.y))
            #Preview Tile Border
            pygame.draw.rect(screen, BLACK, (preview_tile.x - 1, preview_tile.y - 1, (preview_tile.width * enlargement_scale) + 2, (preview_tile.height * enlargement_scale) + 2), 1)

            if switch_state_button.draw(screen):
                game_state = "wfc"
            
            # paint_grid_tile_group.draw(screen)

            if draw_paint_grid_lines:
                for col in range(1, paint_grid_cols):
                    pygame.draw.line(screen, BLACK, (paint_grid_x_pos + col * paint_grid_tile_size, paint_grid_y_pos), (paint_grid_x_pos + col * paint_grid_tile_size, paint_grid_y_pos + paint_grid_tile_size * paint_grid_rows))
                for row in range(1, paint_grid_rows):
                    pygame.draw.line(screen, BLACK, (paint_grid_x_pos, paint_grid_y_pos + row * paint_grid_tile_size), (paint_grid_x_pos + paint_grid_tile_size * paint_grid_cols, paint_grid_y_pos + row * paint_grid_tile_size))

            if toggle_grid_lines_button.draw(screen):
                draw_paint_grid_lines = not draw_paint_grid_lines

            if decrease_pattern_size_button.draw(screen):
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
                    preview_tile = Tile(paint_grid_cols, paint_grid_rows, 50, 400, paint_grid_pix_array, enlargement_scale)

            if increase_pattern_size_button.draw(screen):
                if paint_grid_cols < paint_grid_size_limit_upper:
                    paint_grid_cols += 1
                    paint_grid_rows += 1
                    new_grid = create_empty_paint_grid(paint_grid_x_pos, paint_grid_y_pos, paint_grid_cols, paint_grid_rows, paint_grid_tile_size)
                    for col in range(paint_grid_cols - 1):
                        for row in range(paint_grid_rows - 1):
                            new_grid[col][row] = paint_grid[col][row]
                    paint_grid = new_grid
                    paint_grid_pix_array = create_pix_array(paint_grid)
                    preview_tile = Tile(paint_grid_cols, paint_grid_rows, 50, 400, paint_grid_pix_array, enlargement_scale)

            if test_paint_button.draw(screen):
                print("TEST")

            paint_color_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()