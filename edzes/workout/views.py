from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from home.models import CreatedWorkouts, Excercises, Weights, PreviousWorkouts
import json
# Create your views here.


def choose(request):
    # Azok az edzéstervek, amelyekhez már van súly az adott felhasználónak
    workouts = CreatedWorkouts.objects.all()
    ki = []
    
    for workout in workouts:
        has_excercises = Excercises.objects.filter(workoutid_id=workout.id).exists()
        if has_excercises:
            ki.append(workout)
        else:
            continue
            
    if len(ki) == 0:
        return redirect('home')
    else:
        return render(request, 'choose_workout.html', {'workouts': ki})

def new(request, workout_id):
    all_excercises = Excercises.objects.filter(workoutid_id=workout_id)
    existing_weights = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
    existing_weight_ids = existing_weights.values_list('excerciseid_id', flat=True)
    missing_excercises = all_excercises.exclude(id__in=existing_weight_ids)
    
    # Súlyok létrehozása az összes hiányzó gyakorlathoz 0 értékkel
    for excercise in missing_excercises:
        Weights.objects.create(
            workoutid_id=workout_id,
            userid=request.user,
            excerciseid=excercise,
            weight=0
        )
    
    # Session reset - új edzés kezdése
    request.session['is_active'] = False
    request.session['save_id'] = 0
    
    return redirect('start', workout_id=workout_id)

def start(request, workout_id):
    if request.method == 'POST':
        save_id = request.session.get('save_id', 0)
        
        excercises = Excercises.objects.filter(workoutid_id=workout_id)
        elapsed_time = request.POST.get('elapsed_time', 0)
        comment = request.POST.get('notes')
        
        # Súlyok frissítése
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
        
        # PreviousWorkout frissítése (a save_id azonosítja a frissítendő edzést)
        if save_id:
            previous_workout = PreviousWorkouts.objects.get(
                userid=request.user,
                id=save_id
            )
            previous_workout.timer = elapsed_time
            if comment:
                previous_workout.comment = comment
            previous_workout.save()
        
        return redirect('home')
    else:
        # GET - edzés oldalának megjelenítése
        save_id = request.session.get('save_id', 0)
        
        all_excercises = Excercises.objects.filter(workoutid_id=workout_id)
        existing_weights = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
        
        # Ellenőrizd, hogy van-e súly az összes gyakorlatra
        existing_weight_ids = existing_weights.values_list('excerciseid_id', flat=True)
        missing_excercises = all_excercises.exclude(id__in=existing_weight_ids)
        
        # Automatikusan hozz létre súlyokat a hiányzó gyakorlatokhoz
        for excercise in missing_excercises:
            Weights.objects.create(
                workoutid_id=workout_id,
                userid=request.user,
                excerciseid=excercise,
                weight=0
            )
        
        # Frissítsd a weights lekérdezést az új súlyokkal
        existing_weights = Weights.objects.filter(workoutid_id=workout_id, userid=request.user)
        
        if save_id == 0:
            # Új edzés kezdése
            request.session['is_active'] = False
            request.session['save_id'] = 0
            
            # Hozz létre egy új PreviousWorkout bejegyzést
            previous_workout = PreviousWorkouts(
                userid=request.user,
                workout=CreatedWorkouts.objects.get(id=workout_id),
                timer=0,
                comment=''
            )
            previous_workout.save()
            save_id = previous_workout.id
            request.session['save_id'] = save_id
            timer = 0
            comment = ''
            completed_sets = '{}'
        else:
            # Korábbi edzés folytatása - betöltsd az előző adatokat
            try:
                previous_workout = PreviousWorkouts.objects.get(
                    userid=request.user,
                    id=save_id
                )
                timer = previous_workout.timer
                comment = previous_workout.comment
                completed_sets = previous_workout.completed_sets
            except PreviousWorkouts.DoesNotExist:
                # Fallback: új edzés, ha nem találjuk az előzőt
                request.session['is_active'] = False
                request.session['save_id'] = 0
                previous_workout = PreviousWorkouts(
                    userid=request.user,
                    workout=CreatedWorkouts.objects.get(id=workout_id),
                    timer=0,
                    comment=''
                )
                previous_workout.save()
                save_id = previous_workout.id
                request.session['save_id'] = save_id
                timer = 0
                comment = ''
                completed_sets = '{}'
        
        return render(request, 'workout.html', {'excercises': all_excercises, 'weights': existing_weights, 'workout_id': workout_id, 'timer': timer, 'comment': comment, 'save_id': save_id, 'is_active': False, 'completed_sets': completed_sets})

@require_http_methods(["POST"])
def save_workout_progress(request, workout_id):
    """AJAX endpoint az edzés előrehaladásának mentéséhez"""
    try:
        is_active = request.session.get('is_active', False)
        save_id = request.session.get('save_id', 0)
        
        data = json.loads(request.body)
        elapsed_time = data.get('elapsed_time', 0)
        comment = data.get('comment', '')
        weights = data.get('weights', {})  # {'excercise_id': weight_value}
        completed_sets = data.get('completed_sets', {})  # {'exerciseId': [setNum1, setNum2, ...]}
        
        # Súlyok mentése
        for excercise_id, weight_value in weights.items():
            try:
                weight_obj = Weights.objects.get(
                    workoutid_id=workout_id,
                    userid=request.user,
                    excerciseid_id=int(excercise_id)
                )
                weight_obj.weight = float(weight_value)
                weight_obj.save()
            except Weights.DoesNotExist:
                pass
        
        # PreviousWorkout frissítése
        if is_active and save_id:
            previous_workout = PreviousWorkouts.objects.get(
                userid=request.user,
                workout_id=workout_id,
                id=save_id
            )
            previous_workout.timer = elapsed_time
            if comment:
                previous_workout.comment = comment
            previous_workout.completed_sets = json.dumps(completed_sets)
            previous_workout.save()
        elif save_id:
            # Nem aktív, de van save_id
            previous_workout = PreviousWorkouts.objects.get(
                userid=request.user,
                id=save_id
            )
            previous_workout.timer = elapsed_time
            if comment:
                previous_workout.comment = comment
            previous_workout.completed_sets = json.dumps(completed_sets)
            previous_workout.save()
        
        return JsonResponse({'status': 'success', 'message': 'Adatok mentve'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
                
def previous(request):
    if request.method == 'POST':
        workout_type_id = request.POST.get('workout_type_id')
        request.session['is_active'] = request.POST.get('is_active') == 'true'
        request.session['save_id'] = int(request.POST.get('save_id', 0))
        return redirect('start', workout_id=int(workout_type_id))
    
    previous_workouts = PreviousWorkouts.objects.filter(userid=request.user).order_by('-id')
    return render(request, 'previous.html', {'previous_workouts': previous_workouts})

def delete(request, workout_id):
    PreviousWorkouts.objects.filter(userid=request.user, id=workout_id).delete()
    return redirect('previous')