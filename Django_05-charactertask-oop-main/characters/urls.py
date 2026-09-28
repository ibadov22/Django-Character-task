from django.urls import path

from . import views

app_name = 'characters'

urlpatterns = [
    path('', views.characters_list, name='characters_list'),
    path('create/', views.character_create, name='character_create'),
    path('attack/', views.character_attack, name='character_attack'),
    path('demo/', views.oop_demo, name='oop_demo'),
]
