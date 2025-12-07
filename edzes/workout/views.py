from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import CreatedWorkouts, Excercises, Weights, PreviousWorkouts
# Create your views here.


def choose(request):
    workouts = CreatedWorkouts.objects.all()
    if not workouts.exists():
        return redirect('home')
    return render(request, 'choose_workout.html', {'workouts': workouts})

def new(request, workout_id):
    if request.method == 'POST':
        excercises = Excercises.objects.filter(workoutid_id=workout_id)
        for excercise in excercises:
            weight_value = request.POST.get(f'weight_{excercise.id}')
            if weight_value:
                weight = Weights(
                    workoutid_id=workout_id,
                    userid=request.user,
                    excerciseid=excercise,
                    weight=int(weight_value)
                )
                weight.save()
        return redirect('start', workout_id=workout_id)
    weights = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
    display_excercises = Excercises.objects.filter(workoutid_id=workout_id)
    if not weights.exists():
        return render(request, 'new_plan.html', {'excercises': display_excercises, 'workout_id': workout_id})
    else:
        return redirect('start', workout_id=workout_id)

def start(request, workout_id):
    if request.method == 'POST':
        excercises = Excercises.objects.filter(workoutid_id=workout_id)
        elapsed_time = request.POST.get('elapsed_time', 0)
        comment = request.POST.get('notes')  # Retrieve the comment from the form
        
        for excercise in excercises:
            new_weight_value = request.POST.get(f'new_weight_{excercise.id}')
            if new_weight_value:
                weight_obj = Weights.objects.get(
                    workoutid_id=workout_id,
                    userid=request.user,
                    excerciseid=excercise
                )
                weight_obj.weight = float(new_weight_value)
                weight_obj.save()
        
        workout_record = PreviousWorkouts(
            userid=request.user,
            workout_type=CreatedWorkouts.objects.get(id=workout_id).name,
            timer=int(elapsed_time),
            comment = comment # Placeholder comment
        )
        workout_record.save()
        return redirect('home')
    else:
        weights = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
        if not weights.exists():
            return redirect('new', workout_id=workout_id)
        else:
            excercises = Excercises.objects.filter(workoutid_id=workout_id)
            return render(request, 'workout.html', {'excercises': excercises, 'weights': weights, 'workout_id': workout_id})