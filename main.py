import pygame
import random
import sys
import base64
import os
from datetime import datetime

# Paramètres du jeu
WINDOW_SIZE = 600
SQUARE_SIZE = 20
SNAKE_SIZE = 15  # Taille du serpent plus petite que la nourriture
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()

# Initialisation de la fenêtre
win = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")

# Police pour afficher le texte
font = pygame.font.SysFont("Arial", 24)

# Paramètres du jeu
clock = pygame.time.Clock()

# Contrôles par défaut
controls = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}

# Fonction pour générer la nourriture en évitant les zones d'écriture
def generate_food(snake, score, best_score):
    while True:
        # Nourriture générée près du bord, mais pas dans la zone d'affichage du score
        food_x = random.choice([0, WINDOW_SIZE - SQUARE_SIZE])
        food_y = random.choice([0, WINDOW_SIZE - SQUARE_SIZE])

        # Vérifier si la nourriture est dans la zone du texte
        if (0 <= food_x < (WINDOW_SIZE // SQUARE_SIZE)) and (0 <= food_y < (WINDOW_SIZE // SQUARE_SIZE)):
            if food_x not in [score, best_score]:  # Eviter la zone d'affichage des scores
                return (food_x, food_y)
                
        food = (random.randint(0, (WINDOW_SIZE // SQUARE_SIZE) - 1) * SQUARE_SIZE,
                random.randint(0, (WINDOW_SIZE // SQUARE_SIZE) - 1) * SQUARE_SIZE)
        if food not in snake:
            return food

# Déplacer le serpent
def move_snake(head, direction):
    if head is None:
        return head  # Si la tête est None, ne pas déplacer
    x, y = head
    if direction == controls['up']:
        return (x, y - SQUARE_SIZE)
    elif direction == controls['down']:
        return (x, y + SQUARE_SIZE)
    elif direction == controls['left']:
        return (x - SQUARE_SIZE, y)
    elif direction == controls['right']:
        return (x + SQUARE_SIZE, y)

# Vérifier les collisions
def check_collision(snake):
    if not snake:  # Si la liste du serpent est vide, il y a une erreur
        return True
    head = snake[0]
    if head is None:  # Vérifier si la tête est valide
        return True

    if head[0] < 0 or head[1] < 0 or head[0] >= WINDOW_SIZE or head[1] >= WINDOW_SIZE:
        return True
    if head in snake[1:]:
        return True
    return False

# Dessiner la fenêtre du jeu
def draw_game_window(snake, food, score, best_score):
    win.fill(BLACK)

    for block in snake:
        pygame.draw.rect(win, GREEN, (block[0], block[1], SNAKE_SIZE, SNAKE_SIZE))

    for f in food:
        pygame.draw.rect(win, RED, (f[0], f[1], SQUARE_SIZE, SQUARE_SIZE))

    score_text = font.render(f"Score: {score}", True, WHITE)
    best_score_text = font.render(f"Meilleur Score: {best_score}", True, WHITE)

    win.blit(score_text, (10, 10))
    win.blit(best_score_text, (WINDOW_SIZE - best_score_text.get_width() - 10, 10))

    # Crédits en bas de la fenêtre
    credit_text = font.render("Speed Group © 2025", True, WHITE)
    win.blit(credit_text, (WINDOW_SIZE // 2 - credit_text.get_width() // 2, WINDOW_SIZE - 30))

    pygame.display.update()

# Enregistrer le meilleur score (crypté)
def save_best_score(best_score):
    encrypted_score = base64.b64encode(str(best_score).encode()).decode()
    with open("best_score.txt", "w") as f:
        f.write(encrypted_score)

# Fonction pour charger le meilleur score (décrypté)
def load_best_score():
    if not os.path.exists("best_score.txt"):
        return 0  # Si le fichier n'existe pas, retourner un score de 0

    try:
        with open("best_score.txt", "r") as f:
            encrypted_score = f.read().strip()
            # Vérifier si la chaîne est bien encodée en base64
            if len(encrypted_score) % 4 == 0:
                try:
                    decrypted_score = base64.b64decode(encrypted_score).decode()
                    return int(decrypted_score)
                except (base64.binascii.Error, ValueError):
                    # Si le décodage échoue, réinitialiser le score
                    return 0
            else:
                return 0  # Si la chaîne n'est pas valide en base64, réinitialiser
    except Exception as e:
        print(f"Erreur lors du chargement du meilleur score: {e}")
        return 0  # Si une autre erreur se produit, réinitialiser le score

# Fonction qui enregistre les événements dans le log
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        with open("log.txt", "a", encoding='utf-8') as log_file:
            log_file.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du log: {e}")

# Fonction pour afficher le menu principal
def draw_main_menu():
    win.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    play_button = font.render("Jouer", True, WHITE)
    quit_button = font.render("Quitter", True, WHITE)
    controls_button = font.render("Choisir les contrôles", True, WHITE)

    win.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))
    win.blit(play_button, (WINDOW_SIZE // 2 - play_button.get_width() // 2, 200))
    win.blit(quit_button, (WINDOW_SIZE // 2 - quit_button.get_width() // 2, 300))
    win.blit(controls_button, (WINDOW_SIZE // 2 - controls_button.get_width() // 2, 400))

    pygame.display.update()

    return play_button, quit_button, controls_button

# Fonction pour afficher le menu des contrôles
def draw_controls_menu():
    win.fill(BLACK)
    title_text = font.render("Choisir les contrôles", True, WHITE)
    arrow_controls_button = font.render("Flèches Directionnelles", True, WHITE)
    zqsd_controls_button = font.render("ZQSD", True, WHITE)
    wasd_controls_button = font.render("WASD", True, WHITE)
    back_button = font.render("Retour", True, WHITE)

    win.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))
    win.blit(arrow_controls_button, (WINDOW_SIZE // 2 - arrow_controls_button.get_width() // 2, 200))
    win.blit(zqsd_controls_button, (WINDOW_SIZE // 2 - zqsd_controls_button.get_width() // 2, 250))
    win.blit(wasd_controls_button, (WINDOW_SIZE // 2 - wasd_controls_button.get_width() // 2, 300))
    win.blit(back_button, (WINDOW_SIZE // 2 - back_button.get_width() // 2, 350))

    pygame.display.update()

    return arrow_controls_button, zqsd_controls_button, wasd_controls_button, back_button

# Fonction pour gérer les événements du menu
def main_menu():
    play_button, quit_button, controls_button = draw_main_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Le jeu a été fermé par l'utilisateur.")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if play_button.get_rect(topleft=(WINDOW_SIZE // 2 - play_button.get_width() // 2, 200)).collidepoint(mouse_x, mouse_y):
                    log_event("Lancement de la partie")
                    return "play"
                if quit_button.get_rect(topleft=(WINDOW_SIZE // 2 - quit_button.get_width() // 2, 300)).collidepoint(mouse_x, mouse_y):
                    log_event("Fermeture du jeu")
                    pygame.quit()
                    sys.exit()
                if controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - controls_button.get_width() // 2, 400)).collidepoint(mouse_x, mouse_y):
                    log_event("Ouverture du menu de choix des contrôles")
                    return "controls"

# Fonction pour gérer les événements du menu des contrôles
def controls_menu():
    arrow_controls_button, zqsd_controls_button, wasd_controls_button, back_button = draw_controls_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if arrow_controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - arrow_controls_button.get_width() // 2, 200)).collidepoint(mouse_x, mouse_y):
                    log_event("Contrôles changés en flèches directionnelles.")
                    controls['up'] = pygame.K_UP
                    controls['down'] = pygame.K_DOWN
                    controls['left'] = pygame.K_LEFT
                    controls['right'] = pygame.K_RIGHT
                    return

                if zqsd_controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - zqsd_controls_button.get_width() // 2, 250)).collidepoint(mouse_x, mouse_y):
                    log_event("Contrôles changés en ZQSD.")
                    controls['up'] = pygame.K_z
                    controls['down'] = pygame.K_s
                    controls['left'] = pygame.K_q
                    controls['right'] = pygame.K_d
                    return

                if wasd_controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - wasd_controls_button.get_width() // 2, 300)).collidepoint(mouse_x, mouse_y):
                    log_event("Contrôles changés en WASD.")
                    controls['up'] = pygame.K_w
                    controls['down'] = pygame.K_s
                    controls['left'] = pygame.K_a
                    controls['right'] = pygame.K_d
                    return

                if back_button.get_rect(topleft=(WINDOW_SIZE // 2 - back_button.get_width() // 2, 350)).collidepoint(mouse_x, mouse_y):
                    return

# Boucle principale du jeu
def game_loop():
    score = 0
    best_score = load_best_score()

    snake = [(WINDOW_SIZE // 2, WINDOW_SIZE // 2)]
    direction = controls['right']
    food = [generate_food(snake, score, best_score)]

    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == controls['up']:
                        direction = controls['up']
                    if event.key == controls['down']:
                        direction = controls['down']
                    if event.key == controls['left']:
                        direction = controls['left']
                    if event.key == controls['right']:
                        direction = controls['right']

            # Déplacer le serpent
            head = move_snake(snake[0], direction)
            snake.insert(0, head)

            # Vérifier si le serpent mange la nourriture
            if head in food:
                food.remove(head)
                food.append(generate_food(snake, score, best_score))
                score += 1
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)
                    log_event(f"Nouveau meilleur score: {score}")

            else:
                snake.pop()

            # Vérifier la collision
            if check_collision(snake):
                log_event("Game Over - Collision avec un mur ou la queue")
                return

            draw_game_window(snake, food, score, best_score)

            clock.tick(5)  # Réduire la vitesse du serpent

        except Exception as e:
            log_event(f"Erreur pendant le jeu: {e}")
            return
