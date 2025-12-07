from django.urls import path
from . import views


urlpatterns = [
    path('', views.choose, name='choose'),
    path('new/<int:workout_id>/', views.new, name='new'),
    path('start/<int:workout_id>/', views.start, name='start'),
]
