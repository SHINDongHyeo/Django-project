from django.urls import path
from . import views

app_name = "point"
urlpatterns = [
    path('', views.index, name="index"),
    path('gain/', views.point_gain, name="point_gain"),
    path('lose/', views.point_lose, name="point_lose"),
]