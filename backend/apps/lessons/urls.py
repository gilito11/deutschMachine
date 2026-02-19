from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lessons_list_view, name='list'),
    path('<slug:slug>/', views.lesson_detail_view, name='detail'),
    path('<slug:lesson_slug>/next/', views.next_exercise_view, name='next_exercise'),
    path('<slug:lesson_slug>/restart/', views.restart_lesson_view, name='restart'),
    path('check/<int:exercise_id>/', views.check_answer_view, name='check_answer'),
]
