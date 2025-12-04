from django.urls import path
from . import views


urlpatterns = [
    path('', views.choose_workout, name='workout_home'),
]
