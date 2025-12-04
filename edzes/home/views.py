from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CreatedWorkouts
# Create your views here.

@login_required(login_url="login")
def homepage(request):
    all = False
    my = False
    workouts = CreatedWorkouts.objects.all()
    myworkouts = CreatedWorkouts.objects.filter(userid=request.user)
    if workouts.exists():
        all = True
    if myworkouts.exists():
        my = True
    return render(request, "homepage.html", {"all": all, "my": my})