from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
    path('progress/', views.progress_view, name='progress'),
]
