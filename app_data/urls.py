from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('grid', views.grid, name='grid'),
    path('grid/<int:x>/<int:y>', views.grid, name='grid')
]
