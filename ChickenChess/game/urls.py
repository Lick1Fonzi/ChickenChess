from django.urls import path
from .views import *

app_name = 'game'

urlpatterns = [
 path("<str:inviting>/<str:color>/", game ,name="game"),
 path('lobby/', LobbyView.as_view() , name='lobby'),
 path('creategame/', creategame, name='creategame'),



]