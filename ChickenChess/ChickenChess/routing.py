from django.urls import path
from .consumers import WSConsumerChess

ws_urlpatterns = [
 path("ws/gamews/<str:inviting>/<str:color>/", WSConsumerChess.as_asgi()),

]