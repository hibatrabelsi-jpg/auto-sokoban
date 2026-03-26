import copy

class SudokuGrid:
    def __init__(self, filename):
        self.grid = []
        self.initial_grid = [] 
        self.load_file(filename)

    def load_file(self, filename):
        """Importe et parse la grille depuis le fichier .txt"""
        with open(filename, 'r') as f:
            for line in f:
                # On transforme '_' en 0 pour les calculs
                row = [int(c) if c.isdigit() else 0 for c in line.strip() if c in "_123456789"]
                if row:
                    self.grid.append(row)
        # On garde une copie de la grille de départ pour l'affichage
        self.initial_grid = copy.deepcopy(self.grid)

    def is_valid(self, row, col, n):
        """Vérifie si le chiffre n peut être placé à la position (row, col)"""
        # Vérification Ligne et Colonne
        for i in range(9):
            if self.grid[row][i] == n or self.grid[i][col] == n:
                return False
        
        # Vérification du carré 3x3
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == n:
                    return False
        return True

    def display_terminal(self):
        """Affiche la grille dans la console avec des couleurs"""
        for r in range(9):
            if r % 3 == 0 and r != 0: 
                print("-" * 21)
            line = ""
            for c in range(9):
                if c % 3 == 0 and c != 0: 
                    line += "| "
                val = self.grid[r][c]
                if val == 0: 
                    line += ". "
                elif self.initial_grid[r][c] != 0: 
                    line += f"\033[1m{val}\033[0m " # Gras pour les chiffres de départ
                else: 
                    line += f"\033[94m{val}\033[0m " # Bleu pour les chiffres trouvés
            print(line)

    def solve_logic_elimination(self):
        """Algorithme Bonus : Remplit les cases n'ayant qu'une seule solution possible"""
        changed = False
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    candidates = [n for n in range(1, 10) if self.is_valid(r, c, n)]
                    if len(candidates) == 1:
                        self.grid[r][c] = candidates[0]
                        changed = True
        return changed

    def solve_brute_force(self, index=0, counter=0):
        """Algorithme de Force Brute (ton travail principal)"""
        # Sécurité pour ne pas bloquer l'ordinateur
        if counter > 500000: 
            return False, counter

        # Si index arrive à 81, on a parcouru toutes les cases
        if index == 81:
            return True, counter

        row, col = index // 9, index % 9

        # Si la case n'est pas vide (déjà remplie par l'énoncé ou l'élimination)
        if self.grid[row][col] != 0:
            return self.solve_brute_force(index + 1, counter)

        # On teste les chiffres de 1 à 9
        for n in range(1, 10):
            if self.is_valid(row, col, n):
                self.grid[row][col] = n
                # Appel récursif
                success, final_counter = self.solve_brute_force(index + 1, counter + 1)
                if success: 
                    return True, final_counter
                # Si ça échoue plus loin, on remet à zéro (Backtrack)
                self.grid[row][col] = 0
            
            # On incrémente le compteur d'essais pour les stats
            counter += 1
            
        return False, counter