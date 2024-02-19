from django.shortcuts import render
from django.http import HttpResponse
from .models import get_n_min, ship_placement

# Create your views here.

def home(request):
    L_ship = [4, 3, 3, 2, 2, 2, 1]
    n_min = get_n_min(L_ship)
    n = n_min

    if request.method == "POST":
        n = int(request.POST["n"])

    request.session["n_min"] = n_min
    request.session["n"] = n
    request.session["grid"] = None
    request.session["nb_try"] = 0
    
    return render(request, "app_data/home.html", context={"n_min": n_min, "n_max": 2 * n_min, "n": n, "grid": [[0 for i in range(n)] for j in range(n)]})


def grid(request, x = None, y = None):
    n = request.session["n"]
    n_min = request.session["n_min"]
    win = False

    if not request.session.get("grid"):
        grid = ship_placement(n, n_min)
        request.session["grid"] = grid
    else:
        grid = request.session["grid"]

    if x != None:
        request.session["nb_try"] += 1
        if grid[y][x] == 0: # Dans l'eau
            grid[y][x] = 2
        elif grid[y][x] == 1: # Touché
            grid[y][x] = 3
        request.session["grid"] = grid

    if not any(1 in line for line in grid):
        win = True
    
    return render(request, "app_data/grille.html", context={"grid": grid, "nb_coups": request.session["nb_try"], "win": win})
