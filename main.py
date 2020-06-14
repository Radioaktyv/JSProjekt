import pygame
import sys
import numpy

ROW_COUNT = 7
COLUMN_COUNT = 7
MAX_RIGHT: int = 535
MAX_LEFT: int = 85
SCREEN_SIZE = 620
BOARD_SIZE = 520
MOVEMENT_DISTANCE = 75
CHIP_DIAMETER = 35
BOARD_POS = 50
CHOICE_BACKGROUND_WIDTH = 70

class Colors:
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BACKGROUND = (0, 0, 123)
    CHOICE_BACKGROUND = (0, 150, 255)


def draw(position_x_draw, position_y_draw, screen, board, choice_background, array):
    """It draws board and chips"""
    pygame.draw.rect(screen, Colors.BLUE, board)
    pygame.draw.rect(screen, Colors.CHOICE_BACKGROUND, choice_background)
    for x in range(0, COLUMN_COUNT):
        position_x_draw += MOVEMENT_DISTANCE
        position_y_draw = 10
        for y in range(0, ROW_COUNT):
            position_y_draw += MOVEMENT_DISTANCE
            if array[x][y] == 0:
                pygame.draw.circle(screen, Colors.BLACK, (position_x_draw, position_y_draw), CHIP_DIAMETER)
            else:
                chip(position_x_draw, position_y_draw, array[x][y], screen)


def chip(centerx, centery, turn, screen):
    """It decides which chip should be drawn and also it draws  it on given position"""
    if turn == -1:
        pygame.draw.circle(screen, Colors.RED, (centerx, centery), CHIP_DIAMETER)
    elif turn == 1:
        pygame.draw.circle(screen, Colors.YELLOW, (centerx, centery), CHIP_DIAMETER)


def make_a_move(array, turn, x_array_position):
    """Checks if a position is taken and if so it gives your chip one above if possible"""
    flag = True
    for y in range(COLUMN_COUNT - 1, 0, -1):
        if not flag:
            break
        y_array_position = y
        if array[x_array_position][y_array_position] == 0:
            array[x_array_position][y_array_position] = turn
            flag = False
    next_turn(turn)


def next_turn(turn):
    """It switches turns"""
    if turn == -1:
        turn += 2
    else:
        turn -= 2
    return turn


def check(array, x_array_position, my_font, screen):
    """Checks if move is forbidden"""
    if array[x_array_position][1] == 0:
        return True
    if array[x_array_position][1] != 0:
        label = my_font.render("Forbidden Move", 1, Colors.YELLOW)
        screen.blit(label, (SCREEN_SIZE // 2 - label.get_width() // 2, SCREEN_SIZE // 2 - label.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)
        return False


def winning_move(array, turn):
    """Checks if someone already won"""
    #Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if array[r][c] == turn and array[r][c + 1] == turn and array[r][c + 2] == turn and array[r][c + 3] == turn:
                return True

    #Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if array[r][c] == turn and array[r + 1][c] == turn and array[r + 2][c] == turn and array[r + 3][c] == turn:
                return True

    # Check positively sloped diagonal
    for c in range(COLUMN_COUNT - 3):
        if c + 3 != 0:
            for r in range(ROW_COUNT - 3):
                if array[r][c] == turn and array[r + 1][c + 1] == turn and array[r + 2][c + 2] == turn and \
                        array[r + 3][c + 3] == turn:
                    return True

    # Check negatively sloped diagonal
    for c in range(COLUMN_COUNT - 3):
        if c + 3 != 0:
            for r in range(3, ROW_COUNT):
                if array[r][c] == turn and array[r - 1][c + 1] == turn and array[r - 2][c + 2] == turn and \
                        array[r - 3][c + 3] == turn:
                    return True


def check_draw(array):
    """Checks if there is draw on a board and there are no free moves left"""
    flag = 0
    for x in range(0, COLUMN_COUNT):
        for y in range(1, ROW_COUNT):
            if array[x][y] == 0:
                flag = 1
    if flag == 0:
        return False
    else:
        return True


def main():
    """Main function"""
    pygame.init()
    centerx = 85
    centery = 85
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    board = pygame.Rect(BOARD_POS, BOARD_POS, BOARD_SIZE, BOARD_SIZE)
    choice_background = pygame.Rect(BOARD_POS, BOARD_POS, BOARD_SIZE, CHOICE_BACKGROUND_WIDTH)
    position_x_draw = 10
    position_y_draw = 10
    turn = -1
    game_over = False
    x_array_position = 0
    my_font = pygame.font.SysFont("monospace", 50)
    array = numpy.zeros([ROW_COUNT, COLUMN_COUNT])
    print(array)
    while not game_over:
        screen.fill(Colors.BACKGROUND)
        #Handle Events

        for event in pygame.event.get():
            # Closing game
            if event.type == pygame.QUIT:
                sys.exit(0)
            # Right movement
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if centerx == MAX_RIGHT:
                    centerx = MAX_LEFT
                    x_array_position = 0
                else:
                    centerx += MOVEMENT_DISTANCE
                    x_array_position += 1
            # Left movement
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if centerx == MAX_LEFT:
                    centerx = MAX_RIGHT
                    x_array_position = 6
                else:
                    centerx -= MOVEMENT_DISTANCE
                    x_array_position -= 1
            # Making a move
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if check(array, x_array_position, my_font, screen):
                    make_a_move(array, turn, x_array_position)
                    print(array)
                else:
                    turn = turn * (-1)
                if not winning_move(array, turn) and check_draw(array):
                    turn = next_turn(turn)
                else:
                    if not check_draw(array):
                        label = my_font.render("DRAW", 1, Colors.YELLOW)
                    elif turn == -1:
                        label = my_font.render("Player Red wins!!", 1, Colors.RED)
                    else:
                        label = my_font.render("Player Yellow wins!!", 1, Colors.YELLOW)
                    screen.blit(label, (SCREEN_SIZE // 2 - label.get_width() // 2, SCREEN_SIZE // 2 - label.get_height() // 2))
                    game_over = True
                    pygame.display.flip()
                    pygame.time.wait(3000)




            # drawing
            draw(position_x_draw, position_y_draw, screen, board, choice_background, array)
            chip(centerx, centery, turn, screen)
            pygame.display.flip()
            if game_over:
                pygame.time.wait(2000)


if __name__ == '__main__':
    main()
