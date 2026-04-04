from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('new/', views.new_session_view, name='new_session'),
    path('<int:session_id>/', views.session_view, name='session'),
    path('<int:session_id>/send/', views.send_message_view, name='send_message'),
]
