import pygame
import heapq
import time
from copy import deepcopy
import os

# Import des fonctions et logique de jeu
from build_game import move_player, load_level, wall, empty, target, box, player, box_on_target, player_on_target
from display_game import draw_grid, TILE_SIZE

#L'ALGORITHME A* (LE CERVEAU)

def get_distance_manhattan(matrix):
    boxes = []
    targets = []
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] in [box, box_on_target]:
                boxes.append((r, c))
            if matrix[r][c] in [target, box_on_target, player_on_target]:
                targets.append((r, c))
    
    total_dist = 0
    for bx, by in boxes:
        dists = [abs(bx - tx) + abs(by - ty) for tx, ty in targets]
        if dists:
            total_dist += min(dists)
    return total_dist

def a_star_solver(initial_matrix):
    # (f_score, g_score, matrice, chemin)
    start_node = (get_distance_manhattan(initial_matrix), 0, initial_matrix, [])
    queue = [start_node]
    visited = set()

    while queue:
        f, g, current_matrix, path = heapq.heappop(queue)
        state_hash = tuple(tuple(row) for row in current_matrix)
        
        if state_hash in visited: continue
        visited.add(state_hash)

        if not any(box in row for row in current_matrix):
            return path

        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            new_matrix = move_player(current_matrix, direction)
            new_hash = tuple(tuple(row) for row in new_matrix)
            if new_hash not in visited:
                new_g = g + 1
                new_h = get_distance_manhattan(new_matrix)
                heapq.heappush(queue, (new_g + new_h, new_g, new_matrix, path + [direction]))
    return None

#BOUCLE DE JEU

def main():
    pygame.init()
    
    # Chargement du niveau
    level_path = "levels/level1.txt"
    if not os.path.exists(level_path):
        print("Erreur : Créez un dossier 'levels' avec un fichier 'level1.txt'")
        return
        
    matrix = load_level(level_path)
    initial_state = deepcopy(matrix)
    
    screen = pygame.display.set_mode((len(matrix[0]) * TILE_SIZE, len(matrix) * TILE_SIZE))
    pygame.display.set_caption("Sokoban IA")
    
    font = pygame.font.SysFont("Arial", 24, bold=True)
    moves_count = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                old_matrix = deepcopy(matrix)
                
                # Commandes manuelles
                if event.key == pygame.K_UP:    matrix = move_player(matrix, "UP")
                if event.key == pygame.K_DOWN:  matrix = move_player(matrix, "DOWN")
                if event.key == pygame.K_LEFT:  matrix = move_player(matrix, "LEFT")
                if event.key == pygame.K_RIGHT: matrix = move_player(matrix, "RIGHT")
                
                if matrix != old_matrix:
                    moves_count += 1

                if event.key == pygame.K_r: # Reset
                    matrix = deepcopy(initial_state)
                    moves_count = 0

                if event.key == pygame.K_a: # IA
                    solution = a_star_solver(matrix)
                    if solution:
                        for move in solution:
                            matrix = move_player(matrix, move)
                            moves_count += 1
                            screen.fill((0, 0, 0))
                            draw_grid(screen, matrix)
                            txt = font.render(f"Coups : {moves_count}", True, (255, 255, 0))
                            screen.blit(txt, (15, 15))
                            pygame.display.flip()
                            time.sleep(0.2)

        screen.fill((0, 0, 0))
        draw_grid(screen, matrix)
        score_text = font.render(f"Coups : {moves_count}", True, (255, 255, 0))
        screen.blit(score_text, (15, 15))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()