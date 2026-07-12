from django import forms
from .models import Workout, Goal, Exercise

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'date', 'duration_minutes', 'notes']
        widgets = {
            'date': forms.DateInput(attrs = {'type': 'date'}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'target_date', 'achieved']
        widgets = {
            'target_date': forms.DateInput(attrs = {'type': 'date'}),
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'sets', 'reps', 'weight_kg']