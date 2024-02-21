from django.urls import path
from . import views

app_name = "community"
urlpatterns = [
    path('overseas/', views.overseas, name="overseas"),
    path('domestic/', views.domestic, name="domestic"),
    path('writepost/', views.write, name="write"),
    path('check', views.check, name="check"),
    path('post/<int:id>', views.post, name="post"),
    path('likeit', views.likeit, name="likeit"),
    path('commenting', views.commenting, name="commenting"),
#     path('recommenting/<int:id>', views.recommenting, name="recommenting"),
]