from typing_extensions import Required
from django.db import models
from players.models import profile


# Create your models here.
class Pending_Game(models.Model):
    WHITE = 'white'
    BLACK = 'black'
    COLOR_PLAYER = [(WHITE,'white'),(BLACK,'black')]

    inviting = models.CharField(default= '',max_length=30)
    invited = models.CharField(default= '',max_length=30) 
    color_inviting = models.CharField(choices=COLOR_PLAYER, max_length=5)
    time = models.IntegerField()
    increment = models.IntegerField()