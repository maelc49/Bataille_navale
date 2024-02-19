from django.shortcuts import render
from django.http import HttpResponse
from .models import get_n_min, placement_bateaux

# Create your views here.

def accueil(request):
    L_bateaux = [4, 3, 3, 2, 2, 2, 1]
    n_min = get_n_min(L_bateaux)
    n = n_min

    if request.method == "POST":
        n = int(request.POST["n"])

    request.session["n_min"] = n_min
    request.session["n"] = n
    request.session["grille"] = None
    request.session["nb_coups"] = 0
    
    return render(request, "app_data/home.html", context={"n_min": n_min, "n_max": 2 * n_min, "n": n, "grille": [[0 for i in range(n)] for j in range(n)]})


def grille(request, x = None, y = None):
    n = request.session["n"]
    n_min = request.session["n_min"]
    win = False

    if not request.session.get("grille"):
        grille = placement_bateaux(n, n_min)
        request.session["grille"] = grille
    else:
        grille = request.session["grille"]

    if x != None:
        request.session["nb_coups"] += 1
        if grille[y][x] == 0: # Dans l'eau
            grille[y][x] = 2
        elif grille[y][x] == 1: # Touché
            grille[y][x] = 3
        request.session["grille"] = grille

    if not any(1 in ligne for ligne in grille):
        win = True
    
    return render(request, "app_data/grille.html", context={"grille": grille, "nb_coups": request.session["nb_coups"], "win": win})
