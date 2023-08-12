import pygame
import os
from random import randint
from math import ceil
pygame.init()

# DEFINING WINDOW
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# DEFINING GAME NAME
pygame.display.set_caption("FlappyBird")
# DEFINING GAME ICON
GAME_ICON = pygame.image.load(os.path.join("sprites", "bird1.png"))
pygame.display.set_icon(GAME_ICON)
FPS = 60
FLAP_SOUND = pygame.mixer.Sound("audio/wing.wav")
DIE_SOUND = pygame.mixer.Sound("audio/die.wav")
HIT_SOUND = pygame.mixer.Sound("audio/hit.wav")
SCORE_INCREMENT_SOUND = pygame.mixer.Sound("audio/point.wav")

# DEFINING LIST FOR UPPER PIPES AND LOWER PIPES SO THAT THEY CAN BLIT IN ORDER OR WHEN THE EVENT IS TRIGGERED TO APPEND THEM TO LIST
UPPER_PIPES = []
LOWER_PIPES = []
# DEFINING A BOOLEAN  FOR GAME LOGIC
Game_active = False  # why false becuase if the user want to restart the game but don't want quit and run the program , then this will help in creating logic
is_from_window = False
is_game_over = False
# A VARIABLE IN ORDER TO SHOW THE SCORE
SCORE = 0
# DEFINING A METHOD IN ORDER TO SHOW THE SCORE ON THE WINDOW


def show_score_window():
    global SCORE
    score = FONT.render(f"Score: {SCORE}", False, (0, 0, 0))
    score_rect = score.get_rect(center=(WIDTH/2, 80))
    WIN.blit(score, score_rect)


# -------------------------------- DEFINING METHOD IN ORDER TO DISPLAY GAME OVER--------------------------------------------------------------


def game_over():
    global is_from_window
    game_over = FONT.render("Game Over", False, (0, 0, 0))
    game_over_rect = game_over.get_rect(center=(WIDTH/2, 200))
    WIN.blit(game_over, game_over_rect)
    DIE_SOUND.play()
    is_from_window = True


# -----------------------DEFINING A METHOD IN ORDER TO MOVE THE PIPES----------------
IS_BIRD_PASSED_PIPES = pygame.USEREVENT + 4


def move_the_pipes_and_check_if_bird_collide(PIPE_SCROLL, BIRD_RECT):
    global UPPER_PIPES, LOWER_PIPES, Game_active, SCORE, is_game_over
    for upper_pipe in UPPER_PIPES:
        upper_pipe.x += PIPE_SCROLL
        if BIRD_RECT.colliderect(upper_pipe):
            HIT_SOUND.play()
            is_game_over = True
            Game_active = False
        WIN.blit(PIPE_INVERTED, upper_pipe)
        if upper_pipe.left < BIRD_RECT.x + BIRD_RECT.width and upper_pipe.left >= BIRD_RECT.x + BIRD_RECT.width - 3:
            pygame.event.post(pygame.event.Event(IS_BIRD_PASSED_PIPES))

    for lower_pipe in LOWER_PIPES:
        lower_pipe.x += PIPE_SCROLL
        WIN.blit(PIPE, lower_pipe)

        if BIRD_RECT.colliderect(lower_pipe):
            HIT_SOUND.play()
            is_game_over = True
            Game_active = False
    LOWER_PIPES = [
        lower_pipe for lower_pipe in LOWER_PIPES if lower_pipe.right > -5]
    UPPER_PIPES = [
        upper_pipe for upper_pipe in UPPER_PIPES if upper_pipe.right >= -5]


# ----------------------DEFINING A FUNCTION IN ORDER TO SHOW CHANGES OCCUR ON TO THE WINDOW-----------------------------------------------------------
# ------------------ BACKGROUND FOR THE GAME ------------------------------
BACKGROUND_SURFACE = pygame.image.load(
    os.path.join("sprites", "background.png"))
BACKGROUND_SURFACE = pygame.transform.smoothscale(
    BACKGROUND_SURFACE, (WIDTH, HEIGHT-100))
# -------------- BOTTOM BASE --------------------------
BOTTOM_SUFACE = pygame.image.load(os.path.join("sprites", "base.png"))
BASE_WIDTH = BOTTOM_SUFACE.get_width()
BASE_HEIGHT = BOTTOM_SUFACE.get_height()
# print(BASE_WIDTH)
# print(HEIGHT - BASE_HEIGHT)
# THIS WILL HELP IN INFINTE SCROLLING OF BASE
TILES_REQUIRED = ceil(WIDTH/BASE_WIDTH) + 1
# print(TILES_REQUIRED)

#  ------------BIRD ON THE GAME WINDOW----------
BIRD1 = pygame.image.load(os.path.join("sprites", "bird1.png")).convert_alpha()
BIRD2 = pygame.image.load(os.path.join("sprites", "bird2.png")).convert_alpha()
BIRD_WIDTH = 35
BIRD_HEIGHT = 40
BIRD1 = pygame.transform.smoothscale(BIRD1, (BIRD_WIDTH, BIRD_HEIGHT))
BIRD2 = pygame.transform.smoothscale(BIRD2, (BIRD_WIDTH, BIRD_HEIGHT))
BIRD_RECT = BIRD1.get_rect(center=(760, 150))
BIRD_CHANGE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(BIRD_CHANGE_EVENT, 200)
BIRD_LIST = [BIRD1, BIRD2]
BIRD_INDEX = 0
BIRD_PLACED = BIRD_LIST[BIRD_INDEX]

# ------------------ PIPES ON TO THE SCREEN -----------------------
PIPE = pygame.image.load(os.path.join("sprites", "pipe.png")).convert_alpha()
PIPE_RECT = PIPE.get_rect(midbottom=(WIDTH/2, 500))
PIPE_INVERTED = pygame.image.load(
    os.path.join("sprites", "pipe.png"))
PIPE_INVERTED = pygame.transform.rotate(PIPE_INVERTED, 180).convert_alpha()
PIPE_INVERTED_RECT = PIPE_INVERTED.get_rect(midtop=(WIDTH/2, -270))
PIPE_HEIGHT_LIST = [480, 490, 500, 510, 520, 530, 540, 550, 560, 570,
                    580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680]
OBSTACLE_TIMER = pygame.USEREVENT + 3
pygame.time.set_timer(OBSTACLE_TIMER, 1500)


# print(PIPE.get_width())
# print(PIPE.get_height())


def show_changes_on_window(BOTTOM_SCROLL, BIRD_PLACED, BIRD_RECT, PIPE_SCROLL):
    global is_game_over
    WIN.fill((0, 0, 0))
    WIN.blit(BACKGROUND_SURFACE, (0, 0))
    move_the_pipes_and_check_if_bird_collide(
        PIPE_SCROLL, BIRD_RECT)
    for i in range(0, TILES_REQUIRED):
        WIN.blit(BOTTOM_SUFACE, (i*BASE_WIDTH+BOTTOM_SCROLL, 388))
    WIN.blit(BIRD_PLACED, BIRD_RECT)
    show_score_window()
    if is_game_over:
        game_over()

    pygame.display.update()  # WITH THE HELP OF THIS STATEMENT WE CAN SEE CHANGES
    if is_from_window:
        print("iam in")
        pygame.time.delay(2000)


# DEFINING A METHOD , SO THAT PLAYER COULD KNOW HOW START THE GAME
FONT = pygame.font.SysFont("font/Pixeltype.ttf", 80)
GAME_NAME = FONT.render("Flappy Bird", False, (0, 0, 0))
GAME_NAME_RECT = GAME_NAME.get_rect(center=(WIDTH/2, 80))
GAME_ICON_BIRD = pygame.image.load(os.path.join("sprites", "bird1.png"))
GAME_ICON_BIRD_WIDTH = 200
GAME_ICON_BIRD_HEIGHT = 200
GAME_ICON_BIRD = pygame.transform.smoothscale(
    GAME_ICON_BIRD, (GAME_ICON_BIRD_WIDTH, GAME_ICON_BIRD_HEIGHT))
GAME_ICON_BIRD_SECOND = pygame.image.load(os.path.join("sprites", "bird2.png"))
GAME_ICON_BIRD_SECOND = pygame.transform.smoothscale(
    GAME_ICON_BIRD_SECOND, (GAME_ICON_BIRD_WIDTH, GAME_ICON_BIRD_HEIGHT))
GAME_ICON_BIRD_RECT = GAME_ICON_BIRD.get_rect(center=(WIDTH/2, HEIGHT/2))
ANIME_ON_START = pygame.USEREVENT + 1
pygame.time.set_timer(ANIME_ON_START, 300)
GAME_ICON_ANIME_LIST = [GAME_ICON_BIRD, GAME_ICON_BIRD_SECOND]
ICON_INDEX = 0
BIRD_ICON_TO_BE_PLACED = GAME_ICON_ANIME_LIST[ICON_INDEX]
HINT_TO_START = FONT.render("PRESS SHIFT TO RUN GAME", False, (0, 0, 0))
HINT_TO_START_RECT = HINT_TO_START.get_rect(center=(WIDTH/2, 440))


def start_the_game(score, BIRD_ICON_TO_BE_PLACED):
    WIN.fill("darksalmon")
    WIN.blit(GAME_NAME, GAME_NAME_RECT)
    WIN.blit(BIRD_ICON_TO_BE_PLACED, GAME_ICON_BIRD_RECT)
    if score == 0:
        WIN.blit(HINT_TO_START, HINT_TO_START_RECT)
    else:
        SCORE_TO_DISPLAYED = FONT.render(
            f"YOUR SCORE: {score}", False, (0, 0, 0))
        SCORE_TO_DISPLAYED_RECT = SCORE_TO_DISPLAYED.get_rect(
            center=(WIDTH/2, 440))
        WIN.blit(SCORE_TO_DISPLAYED, SCORE_TO_DISPLAYED_RECT)
    pygame.display.update()


# DEFINING A FUNCTION IN ORDER TO KNOW IF  BIRD TOUCH THE BASE OR IT ESCAPE VELOCITY GREATER THAN Y = 0
def do_bird_exceed_window_or_ground(Game_active, BIRD_RECT):
    global is_game_over
    if BIRD_RECT.y < -5 or BIRD_RECT.y + BIRD_RECT.height >= 388:
        HIT_SOUND.play()
        is_game_over = True
        pygame.display.update()
        if is_from_window:
            print("iam in")
            pygame.time.delay(2000)
        return not Game_active
    return Game_active


# DEFINING MAIN FUNCTION

def main():
    # DECLARATION OF GLOBAL VARIABLES
    global ICON_INDEX, BIRD_ICON_TO_BE_PLACED, BIRD_INDEX, BIRD_PLACED, BIRD_RECT, UPPER_PIPES, LOWER_PIPES, Game_active, is_from_window, SCORE, is_game_over
    # DEFINING VARIABLES THAT WILL HELP US IN CHOOSING HEIGHT AND GAP FOR THE BIRD TO PASS
    GAP_BETWEEN_PIPES = 130
    TEMP = 0
    CHOOSE_UPPERPIPE_HEIGHT = 0
    PIPE_HEIGHT = PIPE.get_height()
    CHOOSE_LOWERPIPE_HEIGHT = 0
    # A VARIABLE HELPS IN MOVING THE PIPES WITH CERTAIN VELOCITY
    PIPE_SCROLL = -3
    # DEFINING A BOOLEAN  IN ORDER OT RUN THE GAME
    FlappyRun = True
    # DEFINING A BOOLEAN  FOR GAME LOGIC ,A VARIABLE IN ORDER TO LOOK BOTTOM SCROLLING
    BOTTOM_SCROLL = 0

    Clock = pygame.time.Clock()
    Bird_gravity = 0

    # RUNNING THE LOOP
    while FlappyRun:
        Clock.tick(FPS)
        # DEFINING EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                FlappyRun = False
            if Game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    Bird_gravity = -4
                    FLAP_SOUND.play()
                if event.type == BIRD_CHANGE_EVENT:
                    if BIRD_INDEX == 0:
                        BIRD_INDEX = 1
                        BIRD_PLACED = BIRD_LIST[BIRD_INDEX]
                    else:
                        BIRD_INDEX = 0
                        BIRD_PLACED = BIRD_LIST[BIRD_INDEX]
                if event.type == OBSTACLE_TIMER:
                    CHOOSE_LOWERPIPE_HEIGHT = randint(
                        0, len(PIPE_HEIGHT_LIST)-1)
                    LOWER_PIPES.append(PIPE.get_rect(midbottom=(
                        1200, PIPE_HEIGHT_LIST[CHOOSE_LOWERPIPE_HEIGHT])))
                    TEMP = PIPE_HEIGHT_LIST[CHOOSE_LOWERPIPE_HEIGHT] - \
                        PIPE_HEIGHT - GAP_BETWEEN_PIPES
                    CHOOSE_UPPERPIPE_HEIGHT = (PIPE_HEIGHT - TEMP)
                    UPPER_PIPES.append(PIPE_INVERTED.get_rect(
                        midtop=(1200, -CHOOSE_UPPERPIPE_HEIGHT)))
                if event.type == IS_BIRD_PASSED_PIPES:
                    SCORE += 1
                    SCORE_INCREMENT_SOUND.play()

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        Game_active = True
                        BIRD_RECT = BIRD1.get_rect(center=(700, 150))
                        Bird_gravity = 0
                        UPPER_PIPES = []
                        LOWER_PIPES = []
                        is_from_window = False
                        is_game_over = False
                        SCORE = 0
                if event.type == ANIME_ON_START:
                    if ICON_INDEX == 0:
                        ICON_INDEX = 1
                        BIRD_ICON_TO_BE_PLACED = GAME_ICON_ANIME_LIST[ICON_INDEX]
                    else:
                        ICON_INDEX = 0
                        BIRD_ICON_TO_BE_PLACED = GAME_ICON_ANIME_LIST[ICON_INDEX]

        if Game_active:
            if abs(BOTTOM_SCROLL) >= BASE_WIDTH:
                BOTTOM_SCROLL = 0
            BOTTOM_SCROLL -= 3
            Bird_gravity += 0.2  # WHY IAM DECREASING IT BY 0.2 TIMES BECAUSE IT LOOKS LIKE VELOCITY INCREASING WHILE FALLING AND GRAVITY IS MORE
            BIRD_RECT.y += Bird_gravity
            show_changes_on_window(
                BOTTOM_SCROLL, BIRD_PLACED, BIRD_RECT, PIPE_SCROLL)
            Game_active = do_bird_exceed_window_or_ground(
                Game_active, BIRD_RECT)
        else:
            start_the_game(SCORE, BIRD_ICON_TO_BE_PLACED)

    pygame.quit()  # THIS WILL HELP USE IN CLOSING THE WINDOW


if __name__ == "__main__":
    main()
