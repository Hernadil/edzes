from django.urls import path
from . import views


urlpatterns = [
    path('', views.editor_home, name='editor'),
    path('my_workouts/', views.my_workouts, name='my_workouts'),
    path('create/', views.create_workout, name='create_workout'),
    path('edit/<int:workout_id>/', views.edit_workout, name='edit_workout'),
    path('delete/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('delete_excercise/<int:excercise_id>/', views.delete_excercise, name='delete_excercise'),
]