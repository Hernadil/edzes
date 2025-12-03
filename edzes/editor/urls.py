from django.urls import path
from . import views


urlpatterns = [
    path('', views.editor_home, name='editor_home'),
    path('create/', views.create_workout, name='create_workout'),
    path('edit/<int:workout_id>/', views.edit_workout, name='edit_workout'),
]