from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.chat, name="chat"),
    path('start/', views.chat_start, name="chat_start"),
    path('start/check', views.chat_check, name="chat_check"),
    path('<int:room_id>', views.chat_room, name="chat_room"),
]