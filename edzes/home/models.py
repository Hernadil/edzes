from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CreatedWorkouts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Excercises(models.Model):
    workoutid = models.ForeignKey(CreatedWorkouts, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    sets = models.IntegerField()
    reps = models.IntegerField()

class Weights(models.Model):
    workoutid = models.ForeignKey(CreatedWorkouts, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    excerciseid = models.ForeignKey(Excercises, on_delete=models.CASCADE)
    weight = models.IntegerField()

class PreviousWorkouts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(CreatedWorkouts, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True)
    timer = models.IntegerField()
    comment = models.CharField(max_length=200)