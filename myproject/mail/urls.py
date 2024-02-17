from django.urls import path
from . import views

app_name = "mail"
urlpatterns = [
    path('receive/', views.mail_receive_list, name="mail_receive_list"),
    path('receive/detail/<int:id>', views.mail_receive_detail, name="mail_receive_detail"),
    path('sent/', views.mail_sent_list, name="mail_sent_list"),
    path('sent/detail/<int:id>', views.mail_sent_detail, name="mail_sent_detail"),

    path('write/', views.mail_write, name="mail_write"),
    path('write/check', views.mail_write_check, name="mail_write_check"),
]