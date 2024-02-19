from django.db import models
import random


def ship_placement(n, n_min, L_ship = [4, 3, 3, 2, 2, 2, 1]):
    """Fonction pour générer une grille de bateaux correspondant aux contraintes.

    Args:
        n (int): La taille de la grille (qui contient donc n * n cases)
        n_min (int): La taille minimale de la grille qui assure un placement
        L_ship (list(int)): Liste des bateaux à placer

    Returns:
        grid: Grille avec les bateaux placés
    """

    
    if n < n_min:
        return -1
    
    grid = [[0 for i in range(n)] for j in range(n)]
    for ship_size in L_ship:
        direction = random.randint(0, 1)

        # L_case représente la liste des cases possibles où un bateau peut être placé. La case à tester est ensuite choisie aléatoirement dans cette liste
        L_case = [i * n + j for i in range(n) for j in range(n) if grid[i][j] == 0
                   and j + ((direction + 1) % 2) * ship_size <= n
                   and i + (direction % 2) * ship_size <= n]

        random_index = random.choice(L_case)
        while not valid_ship(grid, random_index, ship_size, direction):
            L_case.remove(random_index)
            if L_case == []:
                return ship_placement(n, n_min, L_ship)
            random_index = random.choice(L_case)
        row, column = random_index // n, random_index % n
        for i in range(ship_size):
            grid[row + (direction % 2) * i][column + ((direction + 1) % 2) * i] = 1
    return grid


def check_grid(n, L_ship = [4, 3, 3, 2, 2, 2, 1]):
    """Fonction pour savoir s'il est possible d'avoir une grille de taille n.

    Args:
        n (int): La taille de la grille (qui contient donc n * n cases)
        L_ship (list(int)): Liste des bateaux à placer

    Returns:
        int: -1 si il n'y a aucun placement possible, 0 sinon
    """
    
    grid = [[0 for i in range(n)] for j in range(n)]
    for ship_size in L_ship:
        direction = random.randint(0, 1)
        L_case = [i * n + j for i in range(n) for j in range(n) if grid[i][j] == 0
                   and j + ((direction + 1) % 2) * ship_size <= n
                   and i + (direction % 2) * ship_size <= n]

        try:
            random_index = random.choice(L_case)
        except IndexError as e:
            return -1
        
        while not valid_ship(grid, random_index, ship_size, direction):
            L_case.remove(random_index)
            if L_case == []:
                return -1
            random_index = random.choice(L_case)
        row, column = random_index // n, random_index % n
        for i in range(ship_size):
            grid[row + (direction % 2) * i][column + ((direction + 1) % 2) * i] = 1
    return 0


def valid_case(grid, case):
    """Fonction pour savoir si une case n'a aucune case voisine d'occupée.

    Args:
        grid (list(list(int))): Grille contenant les bateaux
        case (int): Numéro de la case à vérifier

    Returns:
        bool: False si la case n'est pas valide, True si elle l'est
    """
        
    n = len(grid)
    i, j = case // n, case % n
    neighbors = []

    # Les voisins d'une case sont moins nombreux si la case est située sur un bord ou sur un coin.
    # On s'assure d'itérer sur les bonnes valeurs en fonction de la position de la case.
    for x in range(0 if i == 0 else -1, 1 if i + 1 == n else 2):    
        for y in range(0 if j == 0 else -1, 1 if j + 1 == n else 2):
            if x == 0 and y == 0:
                pass
            else:
                neighbors.append(grid[i+ x][j + y])
                
    if 1 in neighbors or -1 in neighbors:
        return False
    return True


def valid_ship(grid, case, length, direction):
    """Fonction pour savoir si un bateau peut être placée sur une case avec une direction donnée.
    La case est préalablement choisie de telle sorte que le bateau ne dépasse pas de la grille.

    Args:
        grid (list(list(int))): Grille contenant les bateaux
        case (int): Numéro de la case où le bateau est placé
        length (int): Longueur du bateau
        direction : Sens de placement du bateau (0 = horizontal, 1 = vertical)

    Returns:
        bool: False si le bateau ne peut pas être placé sur cette case, True si il peut
    """

    n = len(grid)
    if direction == 0:
        for i in range(length):
            if not(valid_case(grid, case + i)):
                   return False
    else:
        for j in range(length):
            if not(valid_case(grid, case + j * n)):
                   return False
    return True
                

def get_n_min(L_ship):
    """Fonction pour déterminer la taille minimale d'une grille selon les bateaux à placer

    Args:
        L_ship (list(int)): Liste des bateaux à placer

    Returns:
        int: Taille minimale de la grille selon cette configuration
    """

    L_min = []
    for i in range(100):
        n = 1
        while check_grid(n, L_ship) == -1:
            n += 1
        L_min.append(n)
    return round(sum(L_min) / len(L_min))
