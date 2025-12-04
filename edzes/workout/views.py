from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import CreatedWorkouts, Excercises
# Create your views here.


def choose_workout(request):
    workouts = CreatedWorkouts.objects.all()
    if not workouts.exists():
        return redirect('home')
    return render(request, 'choose_workout.html', {'workouts': workouts})

def start_workout(request, workout_id):
    excercises = Excercises.objects.filter(workoutid=workout_id)
    