from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_front, name='home'),
    path('grid', views.touch_case, name='grid'),
    path('grid/<int:x>/<int:y>', views.touch_case, name='grid')
]
