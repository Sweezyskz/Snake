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

# Langue actuelle (Français par défaut)
current_language = 'fr'

# Textes dans différentes langues
texts = {
    'fr': {
        'title': "Snake Game",
        'play': "Jouer",
        'quit': "Quitter",
        'controls': "Choisir les contrôles",
        'language': "Langue",
        'score': "Score",
        'best_score': "Meilleur Score",
        'controls_title': "Choisir les contrôles",
        'arrow_controls': "Flèches Directionnelles",
        'zqsd_controls': "ZQSD",
        'wasd_controls': "WASD",
        'back': "Retour",
        'credits': "Speed Group © 2025"
    },
    'en': {
        'title': "Snake Game",
        'play': "Play",
        'quit': "Quit",
        'controls': "Choose Controls",
        'language': "Language",
        'score': "Score",
        'best_score': "Best Score",
        'controls_title': "Choose Controls",
        'arrow_controls': "Arrow Keys",
        'zqsd_controls': "ZQSD",
        'wasd_controls': "WASD",
        'back': "Back",
        'credits': "Speed Group © 2025"
    }
}

# Fonction pour générer la nourriture en évitant les zones d'écriture
def generate_food(snake, score, best_score):
    while True:
        # Générer aléatoirement la position de la nourriture
        food_x = random.randint(0, (WINDOW_SIZE // SQUARE_SIZE) - 1) * SQUARE_SIZE
        food_y = random.randint(0, (WINDOW_SIZE // SQUARE_SIZE) - 1) * SQUARE_SIZE

        # Vérifier si la nourriture est dans une zone où on affiche le score ou les crédits
        if (food_x >= 10 and food_x <= (WINDOW_SIZE - 10 - SQUARE_SIZE)) and (food_y >= 50 and food_y <= (WINDOW_SIZE - 50 - SQUARE_SIZE)):
            # Vérifier si la position de la nourriture ne chevauche pas le serpent
            if (food_x, food_y) not in snake:
                return (food_x, food_y)

# Déplacer le serpent
def move_snake(head, direction):
    if head is None:
        return head
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
    if not snake:  
        return True
    head = snake[0]
    if head is None:  
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

    score_text = font.render(f"{texts[current_language]['score']}: {score}", True, WHITE)
    best_score_text = font.render(f"{texts[current_language]['best_score']}: {best_score}", True, WHITE)

    win.blit(score_text, (10, 10))
    win.blit(best_score_text, (WINDOW_SIZE - best_score_text.get_width() - 10, 10))

    credit_text = font.render(texts[current_language]['credits'], True, WHITE)
    win.blit(credit_text, (WINDOW_SIZE // 2 - credit_text.get_width() // 2, WINDOW_SIZE - 30))

    pygame.display.update()

# Enregistrer le meilleur score (crypté)
def save_best_score(best_score):
    encrypted_score = base64.b64encode(str(best_score).encode()).decode()
    try:
        with open("best_score.txt", "w") as f:
            f.write(encrypted_score)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du meilleur score: {e}")



# Fonction pour charger le meilleur score (décrypté)
def load_best_score():
    if not os.path.exists("best_score.txt"):
        return 0  

    try:
        with open("best_score.txt", "r") as f:
            encrypted_score = f.read().strip()
            if len(encrypted_score) % 4 == 0:
                try:
                    decrypted_score = base64.b64decode(encrypted_score).decode()
                    return int(decrypted_score)
                except (base64.binascii.Error, ValueError):
                    return 0
            else:
                return 0  
    except Exception as e:
        print(f"Erreur lors du chargement du meilleur score: {e}")
        return 0  

# Fonction qui enregistre les événements dans le log
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        with open("log.txt", "a", encoding='utf-8') as log_file:
            log_file.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du log: {e}")

# Fonction pour afficher le menu principal avec bouton "Langue"
def draw_main_menu():
    win.fill(BLACK)
    title_text = font.render(texts[current_language]['title'], True, WHITE)
    play_button = font.render(texts[current_language]['play'], True, WHITE)
    quit_button = font.render(texts[current_language]['quit'], True, WHITE)
    controls_button = font.render(texts[current_language]['controls'], True, WHITE)
    language_button = font.render(texts[current_language]['language'], True, WHITE)

    win.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))
    win.blit(play_button, (WINDOW_SIZE // 2 - play_button.get_width() // 2, 150))
    win.blit(controls_button, (WINDOW_SIZE // 2 - controls_button.get_width() // 2, 200))
    win.blit(language_button, (WINDOW_SIZE // 2 - language_button.get_width() // 2, 250))
    win.blit(quit_button, (WINDOW_SIZE // 2 - quit_button.get_width() // 2, 300))

    pygame.display.update()

    return play_button, quit_button, controls_button, language_button

# Fonction pour afficher le menu des contrôles
def draw_controls_menu():
    win.fill(BLACK)
    title_text = font.render(texts[current_language]['controls_title'], True, WHITE)
    arrow_controls_button = font.render(texts[current_language]['arrow_controls'], True, WHITE)
    zqsd_controls_button = font.render(texts[current_language]['zqsd_controls'], True, WHITE)
    wasd_controls_button = font.render(texts[current_language]['wasd_controls'], True, WHITE)
    back_button = font.render(texts[current_language]['back'], True, WHITE)

    win.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))
    win.blit(arrow_controls_button, (WINDOW_SIZE // 2 - arrow_controls_button.get_width() // 2, 200))
    win.blit(zqsd_controls_button, (WINDOW_SIZE // 2 - zqsd_controls_button.get_width() // 2, 250))
    win.blit(wasd_controls_button, (WINDOW_SIZE // 2 - wasd_controls_button.get_width() // 2, 300))
    win.blit(back_button, (WINDOW_SIZE // 2 - back_button.get_width() // 2, 350))

    pygame.display.update()

    return arrow_controls_button, zqsd_controls_button, wasd_controls_button, back_button

# Fonction pour gérer les événements du menu principal
def main_menu():
    play_button, quit_button, controls_button, language_button = draw_main_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Le jeu a été fermé par l'utilisateur.")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if play_button.get_rect(topleft=(WINDOW_SIZE // 2 - play_button.get_width() // 2, 150)).collidepoint(mouse_x, mouse_y):
                    log_event("Lancement de la partie")
                    return "play"
                if quit_button.get_rect(topleft=(WINDOW_SIZE // 2 - quit_button.get_width() // 2, 300)).collidepoint(mouse_x, mouse_y):
                    log_event("Fermeture du jeu")
                    pygame.quit()
                    sys.exit()
                if controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - controls_button.get_width() // 2, 200)).collidepoint(mouse_x, mouse_y):
                    log_event("Ouverture du menu de choix des contrôles")
                    return "controls"
                if language_button.get_rect(topleft=(WINDOW_SIZE // 2 - language_button.get_width() // 2, 250)).collidepoint(mouse_x, mouse_y):
                    log_event("Ouverture du menu de sélection de la langue")
                    return "language"

# Fonction pour gérer le changement de langue
def language_menu():
    global current_language
    win.fill(BLACK)
    title_text = font.render(texts[current_language]['language'], True, WHITE)
    french_button = font.render("Français", True, WHITE)
    english_button = font.render("English", True, WHITE)
    back_button = font.render(texts[current_language]['back'], True, WHITE)

    win.blit(title_text, (WINDOW_SIZE // 2 - title_text.get_width() // 2, 100))
    win.blit(french_button, (WINDOW_SIZE // 2 - french_button.get_width() // 2, 200))
    win.blit(english_button, (WINDOW_SIZE // 2 - english_button.get_width() // 2, 250))
    win.blit(back_button, (WINDOW_SIZE // 2 - back_button.get_width() // 2, 300))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if french_button.get_rect(topleft=(WINDOW_SIZE // 2 - french_button.get_width() // 2, 200)).collidepoint(mouse_x, mouse_y):
                    current_language = 'fr'
                    return
                if english_button.get_rect(topleft=(WINDOW_SIZE // 2 - english_button.get_width() // 2, 250)).collidepoint(mouse_x, mouse_y):
                    current_language = 'en'
                    return
                if back_button.get_rect(topleft=(WINDOW_SIZE // 2 - back_button.get_width() // 2, 300)).collidepoint(mouse_x, mouse_y):
                    return

# Fonction pour gérer le changement des contrôles
def controls_menu():
    global controls
    arrow_controls_button, zqsd_controls_button, wasd_controls_button, back_button = draw_controls_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if arrow_controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - arrow_controls_button.get_width() // 2, 200)).collidepoint(mouse_x, mouse_y):
                    controls = {
                        'up': pygame.K_UP,
                        'down': pygame.K_DOWN,
                        'left': pygame.K_LEFT,
                        'right': pygame.K_RIGHT
                    }
                    return
                if zqsd_controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - zqsd_controls_button.get_width() // 2, 250)).collidepoint(mouse_x, mouse_y):
                    controls = {
                        'up': pygame.K_z,
                        'down': pygame.K_s,
                        'left': pygame.K_q,
                        'right': pygame.K_d
                    }
                    return
                if wasd_controls_button.get_rect(topleft=(WINDOW_SIZE // 2 - wasd_controls_button.get_width() // 2, 300)).collidepoint(mouse_x, mouse_y):
                    controls = {
                        'up': pygame.K_w,
                        'down': pygame.K_s,
                        'left': pygame.K_a,
                        'right': pygame.K_d
                    }
                    return
                if back_button.get_rect(topleft=(WINDOW_SIZE // 2 - back_button.get_width() // 2, 350)).collidepoint(mouse_x, mouse_y):
                    return

# Fonction principale du jeu
def game_loop():
    snake = [(300, 300), (280, 300), (260, 300)]
    food = [generate_food(snake, 0, 0)]
    score = 0
    best_score = load_best_score()
    direction = controls['right']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Le jeu a été fermé par l'utilisateur.")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == controls['up'] and direction != controls['down']:
                    direction = controls['up']
                elif event.key == controls['down'] and direction != controls['up']:
                    direction = controls['down']
                elif event.key == controls['left'] and direction != controls['right']:
                    direction = controls['left']
                elif event.key == controls['right'] and direction != controls['left']:
                    direction = controls['right']

        # Déplacer le serpent
        new_head = move_snake(snake[0], direction)
        snake = [new_head] + snake[:-1]

        # Vérifier si le serpent mange la nourriture
        if snake[0] == food[0]:
            score += 1
            snake.append(snake[-1])
            food = [generate_food(snake, score, best_score)]

        # Vérifier les collisions
        if check_collision(snake):
            log_event(f"Game Over! Score final: {score}")
            if score > best_score:
                best_score = score
                save_best_score(best_score)
            return  # Retourner au menu principal après la fin du jeu

        # Dessiner l'écran
        draw_game_window(snake, food, score, best_score)
        clock.tick(10)

# Lancer le jeu
def run_game():
    while True:
        choice = main_menu()
        if choice == "play":
            game_loop()
        elif choice == "controls":
            controls_menu()
        elif choice == "language":
            language_menu()

run_game()
