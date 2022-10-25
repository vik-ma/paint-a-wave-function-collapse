import pygame
import random
import math
import time
import sys
from tile import Tile
from button import Button
from pattern import Pattern
from rule_index import RuleIndex


pygame.init()

WIDTH = 800
HEIGHT = 640

clock = pygame.time.Clock()
FPS = 60

OUTPUT_WIDTH = 50
OUTPUT_HEIGHT = 50
INPUT_WIDTH = 4
INPUT_HEIGHT = 4

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (175, 175, 175)
LIGHTGREY = (213, 213, 213)

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
    (WHITE, BLACK, BLACK, BLACK)
    ]

def get_rotated_pix_array(pix_array):
    rotated_pix_array_270 = tuple(zip(*pix_array[::-1]))
    rotated_pix_array_180 = tuple(zip(*rotated_pix_array_270[::-1]))
    rotated_pix_array_90 = tuple(zip(*rotated_pix_array_180[::-1]))
    pix_array = tuple(pix_array)
    return (pix_array, rotated_pix_array_90, rotated_pix_array_180, rotated_pix_array_270)

pattern_size = 2 #2x2
pattern_list = []

occurence_weights = {}
probability = {}

pix_array = sample_pixel_array



for row in range(INPUT_WIDTH - (pattern_size - 1)):
    for col in range(INPUT_HEIGHT - (pattern_size -1)):
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



rule_index = RuleIndex(pattern_list, directions)

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




screen = pygame.display.set_mode((WIDTH, HEIGHT))

tile_group = pygame.sprite.Group()




def get_valid_directions(position):
    x, y = position
    
    valid_directions = []

    if x == 0:
        valid_directions.extend([RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_RIGHT])
        elif y == OUTPUT_WIDTH-1:
            valid_directions.extend([UP, UP_RIGHT])
        else:
            valid_directions.extend([DOWN, DOWN_RIGHT, UP, UP_RIGHT])
    elif x == OUTPUT_HEIGHT-1:
        valid_directions.extend([LEFT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT])
        elif y == OUTPUT_WIDTH-1:
            valid_directions.extend([UP, UP_LEFT])
        else:
            valid_directions.extend([DOWN, DOWN_LEFT, UP, UP_LEFT])
    else:
        valid_directions.extend([LEFT, RIGHT])
        if y == 0:
            valid_directions.extend([DOWN, DOWN_LEFT, DOWN_RIGHT])
        elif y == OUTPUT_WIDTH-1:
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT])
        else: 
            valid_directions.extend([UP, UP_LEFT, UP_RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT])
    
    return valid_directions


def initialize_wave_function():
    coefficients = []
    
    for col in range(OUTPUT_HEIGHT):
        row = []
        for r in range(OUTPUT_WIDTH):
            row.append(pattern_list)
        coefficients.append(row)

    return coefficients

coefficients = initialize_wave_function()

def is_wave_function_fully_collapsed():
    """Check if wave function is fully collapsed meaning that for each tile available is only one pattern"""
    for col in coefficients:
        for entry in col:
            if len(entry) > 1:
                return False
    return True

def get_possible_patterns_at_position(position):
    """Return possible patterns at position (x, y)"""
    x, y = position
    possible_patterns = coefficients[x][y]
    return possible_patterns

def get_shannon_entropy(position):
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

def get_min_entropy_at_pos():
    """Return position of tile with the lowest entropy"""
    min_entropy = None
    min_entropy_pos = None
    
    for x, col in enumerate(coefficients):
        for y, row in enumerate(col):
            entropy = get_shannon_entropy((x, y))
            
            if entropy == 0:
                continue
            
            if min_entropy is None or entropy < min_entropy:
                min_entropy = entropy
                min_entropy_pos = (x, y)

    return min_entropy_pos

def observe():
    # Find the lowest entropy
    min_entropy_pos = get_min_entropy_at_pos()
    
    if min_entropy_pos == None:
        print("All tiles have 0 entropy")
        return
    
    # Choose a pattern at lowest entropy position which is most frequent in the sample
    possible_patterns = get_possible_patterns_at_position(min_entropy_pos)
    
    # calculate max probability for patterns that are left
    max_p = 0
    for pattern in possible_patterns:
        if max_p < probability[pattern]:
            max_p == probability[pattern]
    
    
    semi_random_pattern = random.choice([pat for pat in possible_patterns if probability[pat]>=max_p])
    
    # Set this pattern to be the only available at this position
    coefficients[min_entropy_pos[0]][min_entropy_pos[1]] = semi_random_pattern

    return min_entropy_pos

def propagate(min_entropy_pos):
    stack = [min_entropy_pos]
    
    while len(stack) > 0:
        pos = stack.pop()
        
        possible_patterns = get_possible_patterns_at_position(pos)
        
        # Iterate through each location immediately adjacent to the current location
        for direction in get_valid_directions(pos):
            adjacent_pos = (pos[0] + direction[0], pos[1] + direction[1])
            possible_patterns_at_adjacent = get_possible_patterns_at_position(adjacent_pos)
            
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



perf_time_start = time.monotonic()
print("Wave Function Collapse Started")
while not is_wave_function_fully_collapsed():
    min_entropy_pos = observe()
    propagate(min_entropy_pos)

perf_time_end = time.monotonic()
print(f"Wave Function Collapse Ended After {(perf_time_end - perf_time_start):.3f}s")



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


def draw_window():
    screen.fill(GREY)

def draw_grid():
    for row in range(OUTPUT_WIDTH):
        for col in range(OUTPUT_HEIGHT):
            tile = Tile(OUTPUT_WIDTH, OUTPUT_HEIGHT, (col * OUTPUT_WIDTH + 50), (row * OUTPUT_HEIGHT + 50), final_pixels)
            tile_group.add(tile)
    tile_group.draw(screen)

def draw_tile():

    tile = Tile(OUTPUT_HEIGHT, OUTPUT_WIDTH, (0 * OUTPUT_HEIGHT + 50), (0 * OUTPUT_WIDTH + 50), final_pixels)
    tile_group.add(tile)
    tile_group.draw(screen)


def draw_patterns():
    for col in range(len(pattern_list)):
        tile = Tile(pattern_size, pattern_size, (col * (pattern_size + 3) + 50), 25, pattern_list[col].pix_array)
        tile_group.add(tile)
    tile_group.draw(screen)

make_grid_button = Button(WHITE, 600, 50, 150, 40, "Make Grid", BLACK, LIGHTGREY)
test_button = Button(WHITE, 600, 550, 150, 40, "TEST", BLACK, LIGHTGREY)
draw_test_button = Button(WHITE, 600, 450, 150, 40, "DRAW TEST", BLACK, LIGHTGREY)



def main():
    run = True

    is_grid_drawn = True

    draw_test = False

    while run:
        clock.tick(FPS)
        draw_window()
        pygame.draw.rect(screen, BLACK, (49, 49, OUTPUT_WIDTH + 2, OUTPUT_HEIGHT + 2), 1)

        # draw_tile()

        if is_grid_drawn:
            # draw_grid()
            draw_tile()
            # draw_patterns()

        
        if make_grid_button.draw(screen):
            is_grid_drawn = True


        if draw_test:
            draw_patterns(sample_pixel_array)

        if draw_test_button.draw(screen):
            draw_test = True


        if test_button.draw(screen):
            test = get_pix_array_patterns(sample_pixel_array)[0]

            generate_index_rules(test)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()