from django.contrib import admin
from .models import CreatedWorkouts, PreviousWorkouts, Excercises

admin.site.register(CreatedWorkouts)
admin.site.register(PreviousWorkouts)
admin.site.register(Excercises)