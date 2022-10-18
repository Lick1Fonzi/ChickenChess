from django.contrib import admin
from django.urls import path,re_path
from . import views

app_name = 'players'

urlpatterns = [
    path("", views.ListUserView.as_view(), name='listagiocatori' ),
    path("profiloutente/<pk>/", views.DetailProfileView.as_view(), name='profile'),
    
    
]