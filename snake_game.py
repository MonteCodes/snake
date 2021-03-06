import pygame
import sys

from pygame.locals import *

from snake import Snake
from apple import Apple


WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 800

CELL_SIZE   = 20
CELL_WIDTH  = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

# The four possible frame rates/speeds
SLOW   = 10
MEDIUM = 15
FAST   = 25
WHY    = 60

#               R    G    B
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
DARK_GREEN  = (  0, 155,   0)
DARK_GRAY   = ( 40,  40,  40)

BACKGROUND_COLOR = BLACK

# The directions
UP    = 'up'
DOWN  = 'down'
LEFT  = 'left'
RIGHT = 'right'


def main():
    """The main game loop."""
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    show_start_screen()
    frames_per_second = show_speed_menu()
    while True:
        run_game(frames_per_second)
        if show_game_over_screen():
            frames_per_second = show_speed_menu()


def run_game(fps):
    """Runs the game."""
    snake = Snake(CELL_WIDTH, CELL_HEIGHT)
    apple = Apple(CELL_WIDTH, CELL_HEIGHT)

    while True:
        check_for_movement(snake)

        if snake.check_collisions():
            return

        if snake.check_apple_collision(apple):
            apple.move()
        else:
            del snake.coords[-1]

        snake.change_directions()

        DISPLAY_SURFACE.fill(BACKGROUND_COLOR)
        draw_grid()
        snake.draw(DISPLAY_SURFACE, CELL_SIZE)
        apple.draw(DISPLAY_SURFACE, CELL_SIZE)
        draw_score(len(snake.coords) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(fps)


def check_for_key_press():
    """Checks for user keyboard activity."""
    for event in pygame.event.get():
        if event.type == KEYUP:
            return True
        if event.type == QUIT:
            terminate()
    return False


def check_for_mouse_click():
    """Checks for user keyboard activity."""
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos()
    return 0, 0


def check_for_movement(snake):
    """Checks for arrow key or WASD-key events."""
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and snake.direction != RIGHT:
                snake.direction = LEFT
            elif (event.key == K_RIGHT or event.key == K_d) and snake.direction != LEFT:
                snake.direction = RIGHT
            elif (event.key == K_UP or event.key == K_w) and snake.direction != DOWN:
                snake.direction = UP
            elif (event.key == K_DOWN or event.key == K_s) and snake.direction != UP:
                snake.direction = DOWN


def show_start_screen():
    """Displays the start screen of the game."""
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface_one = title_font.render('Snake!', True, WHITE, DARK_GREEN)
    title_surface_two = title_font.render('Snake!', True, GREEN)

    degrees_one = 0
    degrees_two = 0

    while True:
        DISPLAY_SURFACE.fill(BACKGROUND_COLOR)

        rotated_surface_one = pygame.transform.rotate(title_surface_one, degrees_one)
        rotated_rect_one = rotated_surface_one.get_rect()
        rotated_rect_one.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY_SURFACE.blit(rotated_surface_one, rotated_rect_one)

        rotated_surface_two = pygame.transform.rotate(title_surface_two, degrees_two)
        rotated_rect_two = rotated_surface_two.get_rect()
        rotated_rect_two.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY_SURFACE.blit(rotated_surface_two, rotated_rect_two)

        draw_press_key_message()

        if check_for_key_press():
            pygame.event.get()
            return
        pygame.display.update()
        FPS_CLOCK.tick(20)
        degrees_one += 3
        degrees_two += 7


def show_speed_menu():
    """Displays the menu screen of the game and lets the player choose game speed."""
    main_menu_font = pygame.font.Font('freesansbold.ttf', 50)
    main_menu_surface = main_menu_font.render('Menu:', True, WHITE, DARK_GREEN)
    main_menu_rect = main_menu_surface.get_rect()
    main_menu_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)

    sub_menu_font = pygame.font.Font('freesansbold.ttf', 30)

    sub_menu_surface_one = sub_menu_font.render('Slow', True, WHITE)
    sub_menu_rect_one = sub_menu_surface_one.get_rect()
    sub_menu_rect_one.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 50)

    sub_menu_surface_two = sub_menu_font.render('Medium', True, WHITE)
    sub_menu_rect_two = sub_menu_surface_two.get_rect()
    sub_menu_rect_two.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 100)

    sub_menu_surface_three = sub_menu_font.render('Fast', True, WHITE)
    sub_menu_rect_three = sub_menu_surface_three.get_rect()
    sub_menu_rect_three.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 150)

    sub_menu_surface_four = sub_menu_font.render('Are You Sure About This?', True, WHITE)
    sub_menu_rect_four = sub_menu_surface_four.get_rect()
    sub_menu_rect_four.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 200)

    while True:
        DISPLAY_SURFACE.fill(BACKGROUND_COLOR)

        DISPLAY_SURFACE.blit(main_menu_surface, main_menu_rect)
        DISPLAY_SURFACE.blit(sub_menu_surface_one, sub_menu_rect_one)
        DISPLAY_SURFACE.blit(sub_menu_surface_two, sub_menu_rect_two)
        DISPLAY_SURFACE.blit(sub_menu_surface_three, sub_menu_rect_three)
        DISPLAY_SURFACE.blit(sub_menu_surface_four, sub_menu_rect_four)

        mouse_loc = check_for_mouse_click()
        if mouse_loc != (0, 0):
            if sub_menu_rect_one.collidepoint(mouse_loc):
                return SLOW
            elif sub_menu_rect_two.collidepoint(mouse_loc):
                return MEDIUM
            elif sub_menu_rect_three.collidepoint(mouse_loc):
                return FAST
            elif sub_menu_rect_four.collidepoint(mouse_loc):
                return WHY

        pygame.display.update()


def show_game_over_screen():
    """Displays the game over screen."""
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)

    game_surface = game_over_font.render('GAME', True, WHITE)
    game_rect = game_surface.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150)

    over_surface = game_over_font.render('OVER', True, WHITE)
    over_rect = over_surface.get_rect()
    over_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)

    DISPLAY_SURFACE.blit(game_surface, game_rect)
    DISPLAY_SURFACE.blit(over_surface, over_rect)
    draw_press_key_message()

    settings_surface = BASIC_FONT.render('Change settings', True, WHITE)
    settings_rect = settings_surface.get_rect()
    settings_rect.topright = (175, WINDOW_HEIGHT - 30)
    DISPLAY_SURFACE.blit(settings_surface, settings_rect)

    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()

    while True:
        if settings_rect.collidepoint(check_for_mouse_click()):
            return True
        if check_for_key_press():
            pygame.event.get()
            return False


def draw_press_key_message():
    """Displays the message to press a key."""
    press_key_surface = BASIC_FONT.render('Press any key to play.', True, WHITE)
    press_key_rect = press_key_surface.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAY_SURFACE.blit(press_key_surface, press_key_rect)


def draw_grid():
    """Draws the board grid of cells."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(DISPLAY_SURFACE, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(DISPLAY_SURFACE, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_score(score):
    """Displays the current player score."""
    score_surface = BASIC_FONT.render('Score: %s' % score, True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY_SURFACE.blit(score_surface, score_rect)


def terminate():
    """Ends the game."""
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
