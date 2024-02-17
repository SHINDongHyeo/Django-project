from django.urls import path
from . import views

app_name = "football"
urlpatterns = [
    path('<str:league_name>/', views.api_league, name="api_league"),
    path('championship_league/1', views.championship_league, name="championship_league"),
    path('k/1/', views.k1_league, name="k1_league"),
    path('k/2/', views.k2_league, name="k2_league"),
]