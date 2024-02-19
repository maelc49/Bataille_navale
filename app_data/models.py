from django.db import models
import random

def ship_placement(n, n_min, L_ship = [4, 3, 3, 2, 2, 2, 1]):
    if n < n_min:
        return -1
    
    grid = [[0 for i in range(n)] for j in range(n)]
    for ship_size in L_ship:
        direction = random.randint(0, 1)
        L_index = [i * n + j for i in range(n) for j in range(n) if grid[i][j] == 0
                   and j + ((direction + 1) % 2) * ship_size <= n
                   and i + (direction % 2) * ship_size <= n]

        random_index = random.choice(L_index)
        while not valid_ship(grid, random_index, ship_size, direction):
            L_index.remove(random_index)
            if L_index == []:
                return placement_bateaux(n, n_min, L_ship)
            random_index = random.choice(L_index)
        row, column = random_index // n, random_index % n
        for i in range(ship_size):
            grid[row + (direction % 2) * i][column + ((direction + 1) % 2) * i] = 1
    return grid


def get_min(n, L_ship = [4, 3, 3, 2, 2, 2, 1]):    
    grid = [[0 for i in range(n)] for j in range(n)]
    for ship_size in L_ship:
        direction = random.randint(0, 1)
        L_index = [i * n + j for i in range(n) for j in range(n) if grid[i][j] == 0
                   and j + ((direction + 1) % 2) * ship_size <= n
                   and i + (direction % 2) * ship_size <= n]

        try:
            random_index = random.choice(L_index)
        except IndexError as e:
            return -1
        
        while not valid_ship(grid, random_index, ship_size, direction):
            L_index.remove(random_index)
            if L_index == []:
                return -1
            random_index = random.choice(L_index)
        row, column = random_index // n, random_index % n
        for i in range(ship_size):
            grid[row + (direction % 2) * i][column + ((direction + 1) % 2) * i] = 1
    return 0


def valid_case(grid, case):
    n = len(grid)
    i, j = case // n, case % n
    neighbors = []

    for x in range(0 if i == 0 else -1, 1 if i + 1 == n else 2):    # Il y a moins de voisins si la case est au bord de la grid
        for y in range(0 if j == 0 else -1, 1 if j + 1 == n else 2):
            if x == 0 and y == 0:
                pass
            else:
                neighbors.append(grid[i+ x][j + y])
                
    if 1 in neighbors or -1 in neighbors:
        return False
    return True


def valid_ship(grid, case, length, direction):
    # Direction 0 : bateau horizontal
    # Direction 1 : bateau vertical
    # La case choisie au préalable nous assure que le bateau ne dépasse pas de la grid
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
    L_min = []
    for i in range(100):
        n = 1
        while get_min(n, L_ship) == -1:
            n += 1
        L_min.append(n)
    return round(sum(L_min) / len(L_min))
