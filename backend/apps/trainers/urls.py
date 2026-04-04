from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('gender/', views.gender_drill_view, name='gender_drill'),
    path('gender/check/', views.gender_check_view, name='gender_check'),
    path('gender/next/', views.gender_next_view, name='gender_next'),
    path('cases/', views.case_drill_view, name='case_drill'),
    path('cases/check/', views.case_check_view, name='case_check'),
    path('cases/next/', views.case_next_view, name='case_next'),
]
