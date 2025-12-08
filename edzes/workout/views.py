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
        is_active = request.POST.get('is_active') == 'true'
        save_id = int(request.POST.get('save_id', 0))
        
        # Mentsd el a session-be
        request.session['is_active'] = is_active
        request.session['save_id'] = save_id
        
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
    
    weight_objs = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
    display_excercises = Excercises.objects.filter(workoutid_id=workout_id)
    if not weight_objs.exists():
        return render(request, 'new_plan.html', {'excercises': display_excercises, 'workout_id': workout_id})
    else:
        return redirect('start', workout_id=workout_id)

def start(request, workout_id):
    is_active = request.session.get('is_active', False)
    save_id = request.session.get('save_id', 0)
    
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
        
        if is_active:
            
            previous_workout = PreviousWorkouts.objects.get(userid=request.user, workout_id=workout_id, id=save_id)
            previous_workout.timer = elapsed_time
            if comment:
                previous_workout.comment = comment
            previous_workout.save()
            
        else:
            previous_workout = PreviousWorkouts(
                userid=request.user,
                workout=CreatedWorkouts.objects.get(id=workout_id),
                timer=elapsed_time,
                comment=comment
            )
            previous_workout.save()
        return redirect('home')
    else:
        weights = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
        if not weights.exists():
            return redirect('new', workout_id=workout_id)
        else:
            if is_active:
                previous_workout = PreviousWorkouts.objects.get(userid=request.user, workout_id=workout_id, id=save_id)
                return render(request, 'workout.html', {'excercises': Excercises.objects.filter(workoutid_id=workout_id), 'weights': weights, 'workout_id': workout_id, 'timer': previous_workout.timer, 'comment': previous_workout.comment})
            else:
                excercises = Excercises.objects.filter(workoutid_id=workout_id)
                return render(request, 'workout.html', {'excercises': excercises, 'weights': weights, 'workout_id': workout_id, 'timer': 0, 'comment': ''})

def previous(request):
    if request.method == 'POST':
        workout_type_id = request.POST.get('workout_type_id')
        request.session['is_active'] = request.POST.get('is_active') == 'true'
        request.session['save_id'] = int(request.POST.get('save_id', 0))  # Konvertáld int-re
        return redirect('new', workout_id=int(workout_type_id))
    
    previous_workouts = PreviousWorkouts.objects.filter(userid=request.user)
    return render(request, 'previous.html', {'previous_workouts': previous_workouts})

def delete(request, workout_id):
    PreviousWorkouts.objects.filter(userid=request.user, id=workout_id).delete()
    return redirect('previous')