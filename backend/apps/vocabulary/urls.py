from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('', views.browse_view, name='browse'),
    path('topic/<slug:slug>/', views.topic_detail_view, name='topic_detail'),
]
