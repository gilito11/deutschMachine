from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('vocabulary/', include('vocabulary.urls')),
    path('review/', include('srs.urls')),
    path('lessons/', include('lessons.urls')),
    path('conversations/', include('conversations.urls')),
    path('stats/', include('stats.urls')),
    path('trainers/', include('trainers.urls')),
]
