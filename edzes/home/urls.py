from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home'),
    path('redirect/<str:view_name>/', views.redirectview, name='redirectview'),
]
