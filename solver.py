# ============================================================
#  solver.py  –  Solveur A* pour Sokoban
# ============================================================
import heapq
from copy import deepcopy
from build_game import (move_player, BOX, TARGET, BOX_ON_TARGET,
                        PLAYER_ON_TARGET, WALL, is_solved, has_deadlock,
                        _find_player)


def heuristic(matrix):
    """Distance de Manhattan minimale caisse→cible la plus proche."""
    boxes, targets = [], []
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == BOX:
                boxes.append((r, c))
            if cell in (TARGET, BOX_ON_TARGET, PLAYER_ON_TARGET):
                targets.append((r, c))
    if not targets or not boxes:
        return 0
    return sum(min(abs(bx-tx)+abs(by-ty) for tx,ty in targets)
               for bx, by in boxes)


def matrix_hash(matrix):
    """Hash compact : positions des caisses + position du joueur."""
    boxes  = []
    player = None
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == BOX:
                boxes.append((r, c))
            elif cell == BOX_ON_TARGET:
                boxes.append((r, c))   # caisse placée compte aussi
            if cell in (3, 5):         # PLAYER ou PLAYER_ON_TARGET
                player = (r, c)
    return (tuple(sorted(boxes)), player)


def a_star_solver(initial_matrix):
    """
    Retourne la liste de directions qui résout le niveau, ou None.
    Utilise visited avec g_score pour gérer les cycles correctement.
    """
    start_h = heuristic(initial_matrix)
    queue   = [(start_h, 0, initial_matrix, [])]
    visited = {matrix_hash(initial_matrix): 0}  # état -> meilleur g connu

    while queue:
        f, g, current, path = heapq.heappop(queue)

        if is_solved(current):
            return path

        for direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            new_matrix, moved = move_player(current, direction)
            if not moved:
                continue
            if has_deadlock(new_matrix):
                continue

            state = matrix_hash(new_matrix)
            new_g = g + 1

            if state in visited and visited[state] <= new_g:
                continue

            visited[state] = new_g
            h = heuristic(new_matrix)
            heapq.heappush(queue, (new_g + h, new_g, new_matrix, path + [direction]))

    return None