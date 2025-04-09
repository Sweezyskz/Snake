import pygame
import random
import sys

pygame.init()

# Configuration de la fenêtre
WINDOW_SIZE = 600
win = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

SQUARE_SIZE = 20
SPACING = 2
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Configurations des touches
controls_presets = {
    "arrows": {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
    "zqsd": {"up": pygame.K_z, "down": pygame.K_s, "left": pygame.K_q, "right": pygame.K_d},
    "wasd": {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
}

# Variable pour le meilleur score
best_score = 0

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(
            win, (0, 255, 0),
            (segment[0] + SPACING, segment[1] + SPACING,
             SQUARE_SIZE - SPACING * 2, SQUARE_SIZE - SPACING * 2)
        )

def draw_food(foods):
    for food in foods:
        pygame.draw.rect(win, (255, 0, 0), (*food, SQUARE_SIZE, SQUARE_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(text, (WINDOW_SIZE - text.get_width() - 10, 10))

def draw_best_score():
    best_score_text = font.render(f"Meilleur Score: {best_score}", True, (255, 255, 255))
    win.blit(best_score_text, (WINDOW_SIZE - best_score_text.get_width() - 10, 40))

def draw_game_over_menu(score):
    win.fill((0, 0, 0))
    over_text = big_font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    replay_text = font.render("Appuie sur R pour rejouer", True, (200, 200, 200))
    quit_text = font.render("Appuie sur Q pour quitter", True, (200, 200, 200))

    win.blit(over_text, ((WINDOW_SIZE - over_text.get_width()) // 2, 180))
    win.blit(score_text, ((WINDOW_SIZE - score_text.get_width()) // 2, 230))
    win.blit(replay_text, ((WINDOW_SIZE - replay_text.get_width()) // 2, 270))
    win.blit(quit_text, ((WINDOW_SIZE - quit_text.get_width()) // 2, 300))
    pygame.display.update()

def draw_control_menu():
    win.fill((0, 0, 0))
    title = big_font.render("Choisis tes touches", True, (255, 255, 255))
    opt1 = font.render("1 - Flèches directionnelles", True, (200, 200, 200))
    opt2 = font.render("2 - ZQSD", True, (200, 200, 200))
    opt3 = font.render("3 - WASD", True, (200, 200, 200))
    win.blit(title, ((WINDOW_SIZE - title.get_width()) // 2, 80))
    win.blit(opt1, ((WINDOW_SIZE - opt1.get_width()) // 2, 150))
    win.blit(opt2, ((WINDOW_SIZE - opt2.get_width()) // 2, 190))
    win.blit(opt3, ((WINDOW_SIZE - opt3.get_width()) // 2, 230))
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

def spawn_foods(snake, count):
    foods = []
    while len(foods) < count:
        pos = [
            random.randint(0, WINDOW_SIZE // SQUARE_SIZE - 1) * SQUARE_SIZE,
            random.randint(0, WINDOW_SIZE // SQUARE_SIZE - 1) * SQUARE_SIZE
        ]
        if pos not in snake and pos not in foods:
            foods.append(pos)
    return foods

def draw_credits():
    credit_text = font.render("Speed Group © 2025", True, (200, 200, 200))
    win.blit(credit_text, ((WINDOW_SIZE - credit_text.get_width()) // 2, WINDOW_SIZE - 30))  # En bas, centré

def run_game(controls):
    global best_score
    speed = 6  # Vitesse réduite ici
    snake = [[100, 100]]
    direction = [SQUARE_SIZE, 0]
    next_direction = direction.copy()
    score = 0

    food_count = 3  # On veut toujours 3 blocs de nourriture
    foods = spawn_foods(snake, food_count)

    running = True
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == controls["up"] and direction != [0, SQUARE_SIZE]:
                    next_direction = [0, -SQUARE_SIZE]
                elif event.key == controls["down"] and direction != [0, -SQUARE_SIZE]:
                    next_direction = [0, SQUARE_SIZE]
                elif event.key == controls["left"] and direction != [SQUARE_SIZE, 0]:
                    next_direction = [-SQUARE_SIZE, 0]
                elif event.key == controls["right"] and direction != [-SQUARE_SIZE, 0]:
                    next_direction = [SQUARE_SIZE, 0]

        direction = next_direction
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        if new_head in snake or not (0 <= new_head[0] < WINDOW_SIZE) or not (0 <= new_head[1] < WINDOW_SIZE):
            break

        snake.insert(0, new_head)
        if new_head in foods:
            score += 1
            foods.remove(new_head)
            # Assurer qu'il y a toujours 3 blocs de nourriture
            foods += spawn_foods(snake, 1)  # Ajouter un bloc de nourriture supplémentaire
            if len(foods) > 3:
                foods = foods[:3]  # Si on a plus de 3, on garde que les 3 premiers

        else:
            snake.pop()

        # Mise à jour du meilleur score
        if score > best_score:
            best_score = score

        win.fill((0, 0, 0))
        draw_snake(snake)
        draw_food(foods)
        draw_score(score)
        draw_best_score()  # Affiche le meilleur score en dessous du score actuel
        draw_credits()  # Affiche les crédits en bas de la fenêtre
        pygame.display.update()

    while True:
        draw_game_over_menu(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            run_game(controls)
            return
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

# Lancement du jeu
controls = select_controls()
run_game(controls)
