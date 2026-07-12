from django.db import models
from django.conf import settings

class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length = 200)
    date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank = True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.date})"

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete = models.CASCADE, related_name = 'exercises')
    name = models.CharField(max_length = 200)
    sets = models.PositiveIntegerField(default = 1)
    reps = models.PositiveIntegerField(default = 1)
    weight_kg = models.FloatField(null = True, blank = True)

    def __str__(self):
        return f"{self.name} ({self.workout})"

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length = 200)
    description = models.TextField(blank = True)
    target_date = models.DateField(null = True, blank = True)
    achieved = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class CoachAssignment(models.Model):
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'coached_users')
    athlete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'coaches')

    def __str__(self):
        return f"{self.coach.username} → {self.athlete.username}"

class Feedback(models.Model):
    workout = models.ForeignKey(Workout, on_delete = models.CASCADE, related_name = 'feedbacks')
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'given_feedbacks')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Feedback di {self.coach.username} su {self.workout}"