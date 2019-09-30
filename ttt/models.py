from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grid = models.CharField(max_length=100, default=[' ']*9)
    winner = models.CharField(max_length=1, default=' ')
