from django.db import models
import random

def placement_bateaux(n, n_min, L_bateaux = [4, 3, 3, 2, 2, 2, 1]):
    if n < n_min:
        return -1
    
    grille = [[0 for i in range(n)] for j in range(n)]
    for taille_bateau in L_bateaux:
        direction = random.randint(0, 1)
        L_index = [i * n + j for i in range(n) for j in range(n) if grille[i][j] == 0
                   and j + ((direction + 1) % 2) * taille_bateau <= n
                   and i + (direction % 2) * taille_bateau <= n]

        random_index = random.choice(L_index)
        while not bateau_valide(grille, random_index, taille_bateau, direction):
            L_index.remove(random_index)
            if L_index == []:
                return placement_bateaux(n, n_min, L_bateaux)
            random_index = random.choice(L_index)
        row, column = random_index // n, random_index % n
        for i in range(taille_bateau):
            grille[row + (direction % 2) * i][column + ((direction + 1) % 2) * i] = 1
    return grille


def get_min(n, L_bateaux = [4, 3, 3, 2, 2, 2, 1]):    
    grille = [[0 for i in range(n)] for j in range(n)]
    for taille_bateau in L_bateaux:
        direction = random.randint(0, 1)
        L_index = [i * n + j for i in range(n) for j in range(n) if grille[i][j] == 0
                   and j + ((direction + 1) % 2) * taille_bateau <= n
                   and i + (direction % 2) * taille_bateau <= n]

        try:
            random_index = random.choice(L_index)
        except IndexError as e:
            return -1
        
        while not bateau_valide(grille, random_index, taille_bateau, direction):
            L_index.remove(random_index)
            if L_index == []:
                return -1
            random_index = random.choice(L_index)
        row, column = random_index // n, random_index % n
        for i in range(taille_bateau):
            grille[row + (direction % 2) * i][column + ((direction + 1) % 2) * i] = 1
    return 0


def case_valide(grille, case):
    n = len(grille)
    i, j = case // n, case % n
    neighbors = []

    for x in range(0 if i == 0 else -1, 1 if i + 1 == n else 2):    # Il y a moins de voisins si la case est au bord de la grille
        for y in range(0 if j == 0 else -1, 1 if j + 1 == n else 2):
            if x == 0 and y == 0:
                pass
            else:
                neighbors.append(grille[i+ x][j + y])
                
    if 1 in neighbors or -1 in neighbors:
        return False
    return True


def bateau_valide(grille, case, longueur, direction):
    # Direction 0 : bateau horizontal
    # Direction 1 : bateau vertical
    # La case choisie au préalable nous assure que le bateau ne dépasse pas de la grille
    n = len(grille)
    if direction == 0:
        for i in range(longueur):
            if not(case_valide(grille, case + i)):
                   return False
    else:
        for j in range(longueur):
            if not(case_valide(grille, case + j * n)):
                   return False
    return True
                

def get_n_min(L_bateaux):
    L_min = []
    for i in range(100):
        n = 1
        while get_min(n, L_bateaux) == -1:
            n += 1
        L_min.append(n)
    return round(sum(L_min) / len(L_min))
