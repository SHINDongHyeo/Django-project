from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name="home"),
    path('nickname/', views.nickname, name="nickname"),
    path('nickname/check', views.nickname_check, name="nickname_check"),
]