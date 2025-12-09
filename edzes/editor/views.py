from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from home.models import CreatedWorkouts, Excercises
# Create your views here.


def editor_home(request):
    return render(request, 'editor_home.html')

def create_workout(request):
    if request.method == 'POST':
        workout_name = request.POST.get('workout_name', '').strip()
        
        if not workout_name:
            return render(request, 'create_workout.html', {'error': 'Az edzésterv neve nem lehet üres!'})
        
        # Edzésterv létrehozása - itt kapja meg az ID-t az adatbázistól
        workout = CreatedWorkouts.objects.create(
            userid=request.user,
            name=workout_name
        )
        
        # workout.id már elérhető itt, az adatbázis generálta
        return redirect('edit_workout', workout_id=workout.id)
    else:
        return render(request, 'create_workout.html')

def edit_workout(request, workout_id):
    if request.method == 'POST':
        workout = CreatedWorkouts.objects.get(id=workout_id, userid=request.user)
        excercises = Excercises.objects.filter(workoutid_id=workout_id)
        
        # Meglévő feladatok frissítése
        for excercise in excercises:
            name = request.POST.get(f'excercise_name_{excercise.id}')
            sets = request.POST.get(f'excercise_sets_{excercise.id}')
            reps = request.POST.get(f'excercise_reps_{excercise.id}')
            
            if name and sets and reps:
                excercise.name = name
                excercise.sets = int(sets)
                excercise.reps = int(reps)
                excercise.save()
        
        # Új feladatok létrehozása
        # Iterálunk az összes POST adaton és keresünk új_name-eket
        for key in request.POST:
            if key.startswith('new_excercise_name_'):
                new_id = key.replace('new_excercise_name_', '')
                name = request.POST.get(f'new_excercise_name_{new_id}')
                sets = request.POST.get(f'new_excercise_sets_{new_id}')
                reps = request.POST.get(f'new_excercise_reps_{new_id}')
                
                if name and sets and reps:
                    try:
                        Excercises.objects.create(
                            workoutid=workout,
                            name=name,
                            sets=int(sets),
                            reps=int(reps)
                        )
                    except ValueError:
                        pass
        
        return redirect('my_workouts')
    else:
        exc = Excercises.objects.filter(workoutid_id=workout_id)
        return render(request, 'edit.html', {'workout_id': workout_id, 'excercises': exc})
    

def my_workouts(request):
    workouts = CreatedWorkouts.objects.filter(userid=request.user).annotate(
        excercise_count=Count('excercises')
    )
    
    return render(request, 'my_workouts.html', {'workouts': workouts})


def delete_workout(request, workout_id):
    CreatedWorkouts.objects.filter(userid=request.user, id=workout_id).delete()
    return redirect('my_workouts')


def delete_excercise(request, excercise_id):
    excercise = Excercises.objects.get(id=excercise_id)
    workout_id = excercise.workoutid.id
    excercise.delete()
    return redirect('edit_workout', workout_id=workout_id)