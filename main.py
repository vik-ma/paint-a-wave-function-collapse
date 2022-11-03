import pygame
import random
import math
import time
import sys
from tile import Tile
from button import Button
from pattern import Pattern
from rule_index import RuleIndex
from initial_tile import InitialTile
from tile_button import TileButton


pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

error_font = pygame.font.Font(pygame.font.get_default_font(), 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (175, 175, 175)
LIGHTGREY = (213, 213, 213)
GREEN = (0, 255, 00)
YELLOW = (255, 255, 0)

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
    (WHITE, BLACK, GREY, BLACK),
    (WHITE, BLACK, BLACK, BLACK),
    ]

sample_initial_tile_1 = InitialTile(sample_pixel_array, 4, 4)

sample_pixel_array_5x5 = [
    (WHITE, WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, BLACK, WHITE),
    (WHITE, BLACK, GREY, BLACK, GREEN),
    (WHITE, BLACK, BLACK, BLACK, BLACK),
    (GREEN, GREEN, GREEN, GREEN, WHITE)
]

sample_initial_tile_2 = InitialTile(sample_pixel_array_5x5, 5, 5)

sample_pixel_array_5x4 = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, BLACK),
    (WHITE, BLACK, GREY, BLACK),
    (WHITE, BLACK, BLACK, GREEN),
    (WHITE, BLACK, BLACK, GREEN)
]

sample_initial_tile_3 = InitialTile(sample_pixel_array_5x4, 5, 4)

sample_pixel_array_3x4 = [
    (WHITE, WHITE, WHITE, WHITE),
    (WHITE, BLACK, BLACK, GREEN),
    (WHITE, BLACK, WHITE, GREEN)
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


def propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, order):
    stack = [min_entropy_pos]
    print(stack)
    print(coefficients[stack[0][0]][stack[0][1]].pix_array)
    order.extend(stack)
    
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

    perf_time_start = time.monotonic()
    print("Wave Function Collapse Started")

    wfc_completed = True

    # Actual start of WFC
    try:
        while not is_wave_function_fully_collapsed(coefficients):
            min_entropy_pos = observe(coefficients, probability)
            propagate(min_entropy_pos, coefficients, rule_index, output_width, output_height, order)
    except Exception as e:
        wfc_completed = False
        print("WFC FAIL: ", e)

    perf_time_end = time.monotonic()
    print(f"Wave Function Collapse Ended After {(perf_time_end - perf_time_start):.3f}s")

    # print(coefficients[order[0][0]][order[0][1]].pix_array)
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
        return final_pixels
    return None
    # return [coefficients[order[0][0]][order[0][1]].pix_array[0]]ord


def draw_window():
    screen.fill(GREY)

def draw_grid(pix_array, output_width, output_height):
    for row in range(output_width):
        for col in range(output_height):
            tile = Tile(output_width, output_height, (col * output_width + 50), (row * output_height + 50), pix_array)
            tile_group.add(tile)

def draw_test_grid(pix_array, output_width, output_height):
    for row in range(output_width):
        for col in range(output_height):
            tile = Tile(output_width, output_height, (col * output_width + 300), (row * output_height + 50), pix_array)
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

def main():
    run = True

    is_grid_drawn = False

    draw_test_grid = False

    wfc_output = None

    enlargement_scale = 8

    initial_tile_list = []
    tile_list_x_pos = 50
    tile_list_x_offset = 50
    tile_list_y_pos = 350

    sample_tile_1 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_1)
    sample_tile_2 = Tile(sample_initial_tile_2.width, sample_initial_tile_2.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_2.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_2)
    sample_tile_3 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_3)
    sample_tile_4 = Tile(sample_initial_tile_1.width, sample_initial_tile_1.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_1.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_4)
    sample_tile_5 = Tile(sample_initial_tile_2.width, sample_initial_tile_2.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_2.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_5)

    sample_tile_6 = Tile(sample_initial_tile_3.width, sample_initial_tile_3.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_3.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_6)

    sample_tile_7 = Tile(sample_initial_tile_4.width, sample_initial_tile_4.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_4.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_7)
    
    sample_tile_8 = Tile(sample_initial_tile_5.width, sample_initial_tile_5.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_5.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_8)

    sample_tile_9 = Tile(sample_initial_tile_6.width, sample_initial_tile_6.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_6.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_9)

    sample_tile_10 = Tile(sample_initial_tile_7.width, sample_initial_tile_7.height, (tile_list_x_pos + len(initial_tile_list)* tile_list_x_offset), tile_list_y_pos, sample_initial_tile_7.pix_array, enlargement_scale)
    initial_tile_list.append(sample_tile_10)

    pattern_size = 2

    patterns = get_patterns(pattern_size, initial_tile_list[0])

    pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)

    output_width = 6
    output_height = 6

    tile_buttons = create_tile_buttons(initial_tile_list)   

    selected_tile = tile_buttons[0]

    error_msg = error_font.render("WAVE FUNCTION COLLAPSE FAILED", True, (255, 0, 0))
    render_error_msg = False

    while run:
        clock.tick(FPS)
        draw_window()
        
        # Grid border
        pygame.draw.rect(screen, BLACK, (49, 99, (output_width * enlargement_scale) + 2, (output_height * enlargement_scale) + 2), 1)
        # TEST GRID BORDER
        pygame.draw.rect(screen, BLACK, (299, 99, (output_width * enlargement_scale) + 2, (output_height * enlargement_scale) + 2), 1)
        
        draw_patterns(pattern_tile_list)

        if is_grid_drawn:
            tile_group.add(wfc_output)

        if make_grid_button.draw(screen):
            render_error_msg = False
            get_wfc_output = execute_wave_function_collapse(patterns, output_width, output_height)
            if get_wfc_output is not None:
                wfc_output = Tile(output_width, output_height, 50, 100, get_wfc_output, enlargement_scale)
                is_grid_drawn = True
            else:
                render_error_msg = True


        if render_error_msg is True:
            screen.blit(error_msg, (50, 300))

        # Original tiles
        for index, tile_button in enumerate(tile_buttons):
            if tile_button.draw(screen):
                selected_tile = tile_buttons[index]
                patterns = get_patterns(pattern_size, initial_tile_list[index])
                pattern_tile_list = get_pattern_tiles(patterns[0], pattern_size, enlargement_scale)

        draw_selected_tile_border(selected_tile)

        if draw_test_grid:
            tile_group.add(wfc_output)

        if draw_test_button.draw(screen):
            pass

        if test_button.draw(screen):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pattern_group.draw(screen)
        tile_group.draw(screen)


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()