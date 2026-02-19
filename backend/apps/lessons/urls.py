from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lessons_list_view, name='list'),
]
