from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def editor_home(request):
    return render(request, 'editor_home.html')

def create_workout(request):
    return HttpResponse("Create Workout Page")

def edit_workout(request, workout_id):
    return HttpResponse(f"Edit Workout Page for workout ID: {workout_id}")

def my_workouts(request):
    return HttpResponse("My Workouts Page")
