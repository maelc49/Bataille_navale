from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('grille', views.grille, name='grille'),
    path('grille/<int:x>/<int:y>', views.grille, name='grille')
]
