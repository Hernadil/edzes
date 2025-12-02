from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PreviousWorkouts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    workout_type = models.CharField(max_length=10)
    timer = models.IntegerField()
    comment = models.CharField(max_length=200)

class CreatedWorkouts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Excercises(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    workoutid = models.ForeignKey(CreatedWorkouts, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()