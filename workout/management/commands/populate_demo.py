from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workout.models import Workout, Exercise, Goal, CoachAssignment
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Popola il database con dati demo'
    def handle(self, *args, **kwargs):

        #creo utenti demo,se non esistono già

        admin, created = User.objects.get_or_create(username = 'admin_demo', defaults = {'role': 'user', 'is_staff': True, 'is_superuser': True})
        admin.set_password('admin12345')
        admin.save()

        user, created = User.objects.get_or_create(username = 'user_demo', defaults = {'role': 'user'})
        user.set_password('user12345')
        user.save()

        coach, created = User.objects.get_or_create(username = 'coach_demo', defaults = {'role': 'coach'})
        coach.set_password('coach12345')
        coach.save()

        #collego il coach all'utente demo

        CoachAssignment.objects.get_or_create(coach = coach, athlete = user)

        #creo un allenamento con un esercizio dentro
        workout = Workout.objects.create(
            user = user,
            title = 'Allenamento gambe',
            date = datetime.date.today(),
            duration_minutes = 45,
            notes = 'Sessione di forza sulle gambe',
        )
        Exercise.objects.create(workout = workout, name = 'Squat', sets = 4, reps = 10, weight_kg = 60)
        Exercise.objects.create(workout = workout, name = 'Affondi', sets = 3, reps = 12)

        #creo un obiettivo

        Goal.objects.create(
            user = user,
            title = 'Correre 10km',
            description = 'Obiettivo di resistenza per fine mese',
            target_date = datetime.date.today() + datetime.timedelta(days = 30),
        )

        self.stdout.write(self.style.SUCCESS('Dati demo creati con successo'))