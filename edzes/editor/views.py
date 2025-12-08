from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import CreatedWorkouts, Excercises
# Create your views here.


def editor_home(request):
    return render(request, 'editor_home.html')

def create_workout(request):
    return HttpResponse("Create Workout Page")

def edit_workout(request, workout_id):
    return HttpResponse(f"Edit Workout Page for workout ID: {workout_id}")

def my_workouts(request):
    workouts = CreatedWorkouts.objects.filter(userid=request.user)
    return render(request, 'my_workouts.html', {'workouts': workouts})


def delete_workout(request, workout_id):
    CreatedWorkouts.objects.filter(userid=request.user, id=workout_id).delete()
    return redirect('my_workouts')