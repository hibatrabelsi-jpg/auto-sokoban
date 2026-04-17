import pygame
import sys
# On importe la logique et les constantes du fichier build-game.py
from build_game import move_player, wall, empty, target, box, player, box_on_target, player_on_target

# CONFIGURATION INITIALE
pygame.init()
TILE_SIZE = 50  # Taille d'une case

# CHARGEMENT DES IMAGES (TILES)
def load_images():
    # Associe chaque chiffre de la matrice à une image réelle
    images = {
        wall: pygame.image.load("wall.png"),
        empty: pygame.image.load("floor.png"),
        target: pygame.image.load("target.png"),
        box: pygame.image.load("box.png"),
        player: pygame.image.load("player.png"),
        box_on_target: pygame.image.load("box_on_target.png"),
        player_on_target: pygame.image.load("player.png") # Le perso cache la cible
    }
    
    # Redimensionnement automatique de toutes les images à la taille TILE_SIZE
    for key in images:
        images[key] = pygame.transform.scale(images[key], (TILE_SIZE, TILE_SIZE))
    return images

# Création du dictionnaire global des images
TILE_IMAGES = load_images()

# FONCTIONS D'AFFICHAGE
def draw_grid(screen, matrix):
    """Parcourt la matrice et dessine l'image correspondante à chaque case."""
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            img = TILE_IMAGES.get(cell)
            if img:
                # blit dessine l'image aux coordonnées (x, y)
                screen.blit(img, (c * TILE_SIZE, r * TILE_SIZE))

# BOUCLE PRINCIPALE (LE CŒUR DU JEU)
def main(matrix):
    # On ajuste la taille de la fenêtre à la taille de la matrice [cite: 17, 18]
    width = len(matrix[0]) * TILE_SIZE
    height = len(matrix) * TILE_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mon Auto-Sokoban")

    running = True
    while running:
        # Gestion des événements (clavier, souris, fermeture) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # On appelle ta logique de build-game.py à chaque pression
                if event.key == pygame.K_UP:    matrix = move_player(matrix, "UP")
                if event.key == pygame.K_DOWN:  matrix = move_player(matrix, "DOWN")
                if event.key == pygame.K_LEFT:  matrix = move_player(matrix, "LEFT")
                if event.key == pygame.K_RIGHT: matrix = move_player(matrix, "RIGHT")

        # Dessin du jeu
        screen.fill((0, 0, 0)) # Fond noir
        draw_grid(screen, matrix)
        pygame.display.flip() # Met à jour l'affichage

    pygame.quit()
    sys.exit()

# LANCEMENT
if __name__ == "__main__":
    # Exemple de matrice de départ pour tester
    test_matrix = [
        [wall, wall, wall, wall, wall],
        [wall, target, empty, empty, wall],
        [wall, empty, player, box, wall],
        [wall, wall, wall, wall, wall]
    ]
    main(test_matrix)