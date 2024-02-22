from django.urls import path
from . import views

app_name = "point"
urlpatterns = [
    path('', views.index, name="index"),
    path('gain/', views.point_gain, name="point_gain"),
    path('lose/', views.point_lose, name="point_lose"),
    path('roulette/', views.roulette, name="roulette"),
    path('rouletteBat/', views.rouletteBat, name="rouletteBat"),
    path('rouletteBat/save/', views.save, name="save"),
    path('hardRoulette/', views.hardRoulette, name="hardRoulette"),
    path('hardRouletteBat/', views.hardRouletteBat, name="hardRouletteBat"),
    path('matchBat/', views.matchBat, name="matchBat"),
]