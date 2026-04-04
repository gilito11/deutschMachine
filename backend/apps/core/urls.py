from django.urls import path
from django.http import JsonResponse
from . import views


def health_check(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('healthz', health_check, name='health_check'),
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
