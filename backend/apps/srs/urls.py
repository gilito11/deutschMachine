from django.urls import path
from . import views

app_name = 'srs'

urlpatterns = [
    path('', views.review_session_view, name='session'),
    path('card/<int:card_id>/front/', views.card_front_partial, name='card_front'),
    path('card/<int:card_id>/back/', views.card_back_partial, name='card_back'),
    path('card/<int:card_id>/rate/', views.rate_card_view, name='rate_card'),
    path('add-topic/<slug:topic_slug>/', views.add_topic_cards_view, name='add_topic'),
    path('stats/', views.review_stats_view, name='stats'),
]
