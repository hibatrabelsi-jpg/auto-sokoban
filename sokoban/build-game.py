#Constantes
wall = -1
empty = 0
target = 1
box = 2
player = 3
box_on_target = 4
player_on_target = 5

# grille de test
# On utilise une matrice (liste de listes) pour représenter l'entrepôt [cite: 5, 17]
matrix = [
    [wall, wall, wall, wall, wall],
    [wall, target, empty, empty, wall],
    [wall, empty, player, box, wall],
    [wall, box, target, empty, wall],
    [wall, wall, wall, wall, wall]
]

def move_player(matrix, direction):
    # 1. Trouver où est le joueur (on cherche 3 ou 5)
    curr_x, curr_y = None, None
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] in [player, player_on_target]:
                curr_x, curr_y = r, c
                break
    
    # 2. Définir la direction
    dx, dy = 0, 0
    if direction == "UP": dx = -1
    elif direction == "DOWN": dx = 1
    elif direction == "LEFT": dy = -1
    elif direction == "RIGHT": dy = 1

    # Coordonnées de la case visée (nx, ny) et de la case d'après (ax, ay)
    nx, ny = curr_x + dx, curr_y + dy
    ax, ay = nx + dx, ny + dy

    # 3. Sécurité : on ne traverse pas les murs [cite: 7]
    if matrix[nx][ny] == wall:
        return matrix

    # 4. Logique de déplacement
    target_cell = matrix[nx][ny]

    # CAS A : On marche sur du vide ou une cible
    if target_cell in [empty, target]:
        update_cell(matrix, curr_x, curr_y, nx, ny)

    # CAS B : On pousse une caisse [cite: 6]
    elif target_cell in [box, box_on_target]:
        # On ne peut pousser que si la case derrière est libre [cite: 7]
        if matrix[ax][ay] in [empty, target]:
            push_box(matrix, nx, ny, ax, ay)
            update_cell(matrix, curr_x, curr_y, nx, ny)

    return matrix

def update_cell(matrix, x, y, nx, ny):
    # Le joueur quitte sa case actuelle
    if matrix[x][y] == player_on_target:
        matrix[x][y] = target
    else:
        matrix[x][y] = empty

    # Le joueur arrive sur la nouvelle case
    if matrix[nx][ny] == target:
        matrix[nx][ny] = player_on_target
    else:
        matrix[nx][ny] = player

def push_box(matrix, nx, ny, ax, ay):
    # On déplace la caisse vers sa nouvelle position
    if matrix[ax][ay] == target:
        matrix[ax][ay] = box_on_target
    else:
        matrix[ax][ay] = box
    # Note : La case (nx, ny) sera remplacée par le joueur juste après dans update_cell


