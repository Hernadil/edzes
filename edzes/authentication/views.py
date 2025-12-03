from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "loginpage.html", {"error": "Nem megfelelő felhasználónév vagy jelszó."})
    return render(request, "loginpage.html")

# ...existing code...
from django.db import IntegrityError

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('reg-username')
        password = request.POST.get('reg-password')
        password2 = request.POST.get('reg-password2')

        if username == "" or password == "" or password2 == "" or fullname == "":
            return render(request, "registerpage.html", {"error": "A jelszavak nem egyeznek!"})
        elif password != password2:
            return render(request, "registerpage.html", {"error": "Kérlek mindent töltsél ki!"})
        else:
            try:
                user = User.objects.create_user(username=username, password=password, first_name=fullname)
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, "registerpage.html", {"error": "A felhasználónév már foglalt."})
    return render(request, "registerpage.html")


def logoutuser(request):
    logout(request)
    return redirect('login')