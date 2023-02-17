from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('football/', views.football, name='football'),
    path('loaderio-6f638dd217ebc0c6ad2e477d8e9e2e8c/', views.loaderio,
         name='loaderio'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('score/', views.score, name='score'),
]
