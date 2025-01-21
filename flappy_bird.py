import pygame
import sys
import random

# Initialization
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game Variables
gravity = 0.5
bird_movement = 0
bird = pygame.Rect(100, 300, 30, 30)

PIPE_WIDTH = 50
PIPE_HEIGHT = 400
pipe_list = []
pipe_spawn_time = 1200
pipe_gap = 200

# Timer for spawning pipes
spawn_pipe_timer = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_timer, pipe_spawn_time)


def create_pipe():
    # Randomize the pipe positions
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(SCREEN_WIDTH, height - pipe_gap - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height, PIPE_WIDTH, PIPE_HEIGHT)
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > 0]


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            pygame.draw.rect(screen, GREEN, pipe)
        else:
            pygame.draw.rect(screen, RED, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= SCREEN_HEIGHT:
        return True
    return False


# Game Loop
game_active = True

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                bird.center = (100, 300)
                bird_movement = 0
                pipe_list.clear()

        if event.type == spawn_pipe_timer and game_active:
            pipe_list.extend(create_pipe())

    if game_active:
        # Fill the background
        screen.fill(BLUE)

        # Bird Movement
        bird_movement += gravity
        bird.centery += bird_movement
        pygame.draw.ellipse(screen, BLACK, bird)

        # Pipes Movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Check Collision
        game_active = not check_collision(pipe_list)

    else:
        # Fill screen in game over
        screen.fill(WHITE)
        font = pygame.font.Font(None, 54)
        text = font.render("Game Over! Press Space", True, BLACK)
        screen.blit(text, (20, SCREEN_HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(FPS)
