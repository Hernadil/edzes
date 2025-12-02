from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def loginpage(request):
    return render(request, "loginpage.html")

def registerpage(request):
    return render(request, "registerpage.html")