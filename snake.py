import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 400, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

SQUARE_SIZE = 20
SPACING = 2
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Mapping des contrôles
controls_presets = {
    "arrows": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT
    },
    "zqsd": {
        "up": pygame.K_z,
        "down": pygame.K_s,
        "left": pygame.K_q,
        "right": pygame.K_d
    },
    "wasd": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d
    }
}

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(
            win, (0, 255, 0),
            (segment[0] + SPACING, segment[1] + SPACING,
             SQUARE_SIZE - SPACING * 2, SQUARE_SIZE - SPACING * 2)
        )

def draw_food(food):
    pygame.draw.rect(win, (255, 0, 0), (*food, SQUARE_SIZE, SQUARE_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(text, (WIDTH - text.get_width() - 10, 10))

def draw_game_over_menu(score):
    win.fill((0, 0, 0))
    over_text = big_font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    replay_text = font.render("Appuie sur R pour rejouer", True, (200, 200, 200))
    quit_text = font.render("Appuie sur Q pour quitter", True, (200, 200, 200))

    win.blit(over_text, ((WIDTH - over_text.get_width()) // 2, HEIGHT // 2 - 60))
    win.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 - 20))
    win.blit(replay_text, ((WIDTH - replay_text.get_width()) // 2, HEIGHT // 2 + 20))
    win.blit(quit_text, ((WIDTH - quit_text.get_width()) // 2, HEIGHT // 2 + 50))
    pygame.display.update()

def draw_control_menu():
    win.fill((0, 0, 0))
    title = big_font.render("Choisis tes touches", True, (255, 255, 255))
    opt1 = font.render("1 - Flèches directionnelles", True, (200, 200, 200))
    opt2 = font.render("2 - ZQSD", True, (200, 200, 200))
    opt3 = font.render("3 - WASD", True, (200, 200, 200))

    win.blit(title, ((WIDTH - title.get_width()) // 2, 80))
    win.blit(opt1, ((WIDTH - opt1.get_width()) // 2, 150))
    win.blit(opt2, ((WIDTH - opt2.get_width()) // 2, 190))
    win.blit(opt3, ((WIDTH - opt3.get_width()) // 2, 230))
    pygame.display.update()

def select_controls():
    while True:
        draw_control_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return controls_presets["arrows"]
        elif keys[pygame.K_2]:
            return controls_presets["zqsd"]
        elif keys[pygame.K_3]:
            return controls_presets["wasd"]

def run_game():
    controls = select_controls()

    snake = [[100, 100]]
    direction = [SQUARE_SIZE, 0]
    food = [random.randint(0, WIDTH // SQUARE_SIZE - 1) * SQUARE_SIZE,
            random.randint(0, HEIGHT // SQUARE_SIZE - 1) * SQUARE_SIZE]
    score = 0
    running = True

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[controls["up"]] and direction != [0, SQUARE_SIZE]:
            direction = [0, -SQUARE_SIZE]
        if keys[controls["down"]] and direction != [0, -SQUARE_SIZE]:
            direction = [0, SQUARE_SIZE]
        if keys[controls["left"]] and direction != [SQUARE_SIZE, 0]:
            direction = [-SQUARE_SIZE, 0]
        if keys[controls["right"]] and direction != [-SQUARE_SIZE, 0]:
            direction = [SQUARE_SIZE, 0]

        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        if new_head in snake or not (0 <= new_head[0] < WIDTH) or not (0 <= new_head[1] < HEIGHT):
            break

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = [random.randint(0, WIDTH // SQUARE_SIZE - 1) * SQUARE_SIZE,
                    random.randint(0, HEIGHT // SQUARE_SIZE - 1) * SQUARE_SIZE]
        else:
            snake.pop()

        win.fill((0, 0, 0))
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.update()

    # Menu Game Over
    while True:
        draw_game_over_menu(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            run_game()
            return
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

# Lancer le jeu avec menu de choix de contrôles
run_game()
