from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    rating = models.IntegerField(default=500)
    profileimg = models.ImageField(default='default.jpg')
    lowest_rating = models.IntegerField(default=500)
    highest_rating = models.IntegerField(default=500)
    victories = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)


class Game(models.Model):
    White = models.ForeignKey(profile, on_delete=models.CASCADE,related_name='White')
    Black = models.ForeignKey(profile,on_delete=models.CASCADE,related_name='Black')
    outcome = models.CharField(default='',max_length=8)
    time = models.IntegerField()
    increment = models.IntegerField()
    moves = models.CharField(default='',max_length=1000)


