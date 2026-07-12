from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Workout, Exercise, Goal, CoachAssignment, Feedback
from .forms import WorkoutForm, GoalForm, ExerciseForm


@login_required
@login_required
def home(request):
    workouts = Workout.objects.filter(user = request.user).order_by('-date')[:5]
    goals = Goal.objects.filter(user = request.user)
    # riepilogo per la home: totale allenamenti e obiettivi raggiunti
    total_workouts = Workout.objects.filter(user = request.user).count()
    total_goals = goals.count()
    achieved_goals = goals.filter(achieved=True).count()
    if total_goals > 0:
        goals_percentage = round((achieved_goals / total_goals) * 100)
    else:
        goals_percentage = 0
    return render(request, 'workout/home.html', {
        'workouts': workouts,
        'goals': goals,
        'total_workouts': total_workouts,
        'total_goals': total_goals,
        'achieved_goals': achieved_goals,
        'goals_percentage': goals_percentage,
    })

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workout/workout_list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        # ogni utente vede solo i propri allenamenti
        return Workout.objects.filter(user = self.request.user).order_by('-date')

@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit = False)
            workout.user = request.user
            workout.save()
            return redirect('workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'workout/workout_form.html', {'form': form})

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk = pk)
    is_owner = workout.user == request.user
    is_assigned_coach = CoachAssignment.objects.filter(coach = request.user, athlete = workout.user).exists()
    if not is_owner and not is_assigned_coach:
        raise PermissionDenied
    return render(request, 'workout/workout_detail.html', {'workout': workout, 'is_owner': is_owner})

@login_required
def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk = pk, user = request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance = workout)
        if form.is_valid():
            form.save()
            return redirect('workout_detail', pk = pk)
    else:
        form = WorkoutForm(instance = workout)
    return render(request, 'workout/workout_form.html', {'form': form})

@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk = pk, user = request.user)
    if request.method == 'POST':
        workout.delete()
        return redirect('workout_list')
    return render(request, 'workout/workout_confirm_delete.html', {'workout': workout})

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user = request.user)
    return render(request, 'workout/goal_list.html', {'goals': goals})

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit = False)
            goal.user = request.user
            goal.save()
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'workout/goal_form.html', {'form': form})

@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk = pk, user = request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance = goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = GoalForm(instance = goal)
    return render(request, 'workout/goal_form.html', {'form': form})

@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk = pk, user = request.user)
    return render(request, 'workout/goal_detail.html', {'goal': goal})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk = pk, user = request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'workout/goal_confirm_delete.html', {'goal': goal})

@login_required
def coach_dashboard(request):
    if request.user.role != 'coach':
        raise PermissionDenied
    assignments = CoachAssignment.objects.filter(coach = request.user)
    #Per ogni atleta assegnato al coach, prendo i suoi ultimi allenamenti
    athletes_data = []
    for assignment in assignments:
        workouts = Workout.objects.filter(user = assignment.athlete).order_by('-date')[:5].prefetch_related('feedbacks')
        athletes_data.append({'athlete': assignment.athlete, 'workouts': workouts})
    return render(request, 'workout/coach_dashboard.html', {'athletes_data': athletes_data})

@login_required
def give_feedback(request, pk):
    if request.user.role != 'coach':
        raise PermissionDenied
    workout = get_object_or_404(Workout, pk = pk)
    #Controllo che il coach sia davvero assegnato all'atleta proprietario del workout
    is_assigned = CoachAssignment.objects.filter(coach = request.user, athlete = workout.user).exists()
    if not is_assigned:
        raise PermissionDenied
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        if comment:
            Feedback.objects.create(workout = workout, coach = request.user, comment = comment)
        return redirect('coach_dashboard')
    return render(request, 'workout/give_feedback.html', {'workout': workout})

@login_required
def exercise_add(request, pk):
    # pk è l'id dell'allenamento a cui aggiungere l'esercizio
    workout = get_object_or_404(Workout, pk = pk, user = request.user)
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit = False)
            exercise.workout = workout
            exercise.save()
            return redirect('workout_detail', pk = workout.pk)
    else:
        form = ExerciseForm()
    return render(request, 'workout/exercise_form.html', {'form': form, 'workout': workout})