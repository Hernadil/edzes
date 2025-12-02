from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Weight(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=10)
    set = models.CharField(max_length=20)
    weight = models.IntegerField()

class PreviousWorkouts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    workout_type = models.CharField(max_length=10)
    timer = models.IntegerField()
    comment = models.CharField(max_length=200)