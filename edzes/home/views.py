from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CreatedWorkouts, Excercises
# Create your views here.

@login_required(login_url="login")
def homepage(request):
    workouts = CreatedWorkouts.objects.all()
    ki = []
    all = False
    
    if workouts.exists():
        for workout in workouts:
            has_excercises = Excercises.objects.filter(workoutid_id=workout.id).exists()
            if has_excercises:
                ki.append(workout)
            else:
                continue
    
    if len(ki) > 0:
        all = True

    return render(request, 'homepage.html', {'all': all})

def redirectview(request, view_name):
    return redirect(view_name)  