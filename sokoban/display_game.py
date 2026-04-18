import pygame

# Taille de chaque case en pixels
TILE_SIZE = 50

# Dictionnaire de couleurs (R, G, B)
# On utilise les chiffres définis dans build_game.py
COLORS = {
    0: (220, 220, 220),  # Vide (Gris très clair)
    1: (40, 40, 40),     # Mur (Gris presque noir)
    2: (160, 82, 45),    # Caisse (Sienna / Marron)
    3: (255, 99, 71),    # Cible (Tomate / Rouge)
    4: (30, 144, 255),   # Joueur (DodgerBlue / Bleu)
    5: (50, 205, 50),    # Caisse placée (LimeGreen / Vert)
    6: (0, 191, 255)     # Joueur sur cible (DeepSkyBlue)
}

def draw_grid(screen, matrix):
    #Dessine la matrice sur l'écran Pygame
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            color = COLORS.get(cell, (0, 0, 0)) # Noir par défaut si inconnu
            
            # Position (x, y) et taille (largeur, hauteur)
            rect = (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            # On dessine le carré plein
            pygame.draw.rect(screen, color, rect)
            
            # On dessine une bordure blanche très fine pour la grille
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)