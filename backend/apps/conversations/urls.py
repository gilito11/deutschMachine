from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.chat_view, name='chat'),
]
