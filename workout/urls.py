from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('workout/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workout/new/', views.workout_create, name = 'workout_create'),
    path('workout/<int:pk>/', views.workout_detail, name = 'workout_detail'),
    path('workout/<int:pk>/edit/', views.workout_edit, name = 'workout_edit'),
    path('workout/<int:pk>/delete/', views.workout_delete, name = 'workout_delete'),
    path('goals/', views.goal_list, name = 'goal_list'),
    path('goals/new/', views.goal_create, name = 'goal_create'),
    path('goals/<int:pk>/', views.goal_detail, name = 'goal_detail'),
    path('goals/<int:pk>/edit/', views.goal_edit, name = 'goal_edit'),
    path('goals/<int:pk>/delete/', views.goal_delete, name = 'goal_delete'),
    path('coach/', views.coach_dashboard, name = 'coach_dashboard'),
    path('coach/feedback/<int:pk>/', views.give_feedback, name = 'give_feedback'),
    path('workout/<int:pk>/exercise/new/', views.exercise_add, name = 'exercise_add'),
]