from django.urls import path
from . import views


urlpatterns = [
    path('', views.choose, name='choose'),
    path('previous/', views.previous, name='previous'),
    path('new/<int:workout_id>/', views.new, name='new'),
    path('start/<int:workout_id>/', views.start, name='start'),
    path('save_progress/<int:workout_id>/', views.save_workout_progress, name='save_progress'),
    path('delete/<int:workout_id>/', views.delete, name='delete'),
]
