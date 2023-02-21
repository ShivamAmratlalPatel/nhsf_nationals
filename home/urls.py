import debug_toolbar
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('football/', views.football, name='football'),
    path('netball/', views.netball, name='netball'),
    path('kho/', views.kho, name='kho'),
    path('kabaddi/', views.kabaddi, name='kabaddi'),
    path('cricket/', views.cricket, name='cricket'),
    path('badminton/', views.badminton, name='badminton'),
    path('loaderio-6f638dd217ebc0c6ad2e477d8e9e2e8c/', views.loaderio,
         name='loaderio'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('scorefootball/', views.scorefootball, name='scorefootball'),
    path('scorekho/', views.scorekho, name='scorekho'),
    path('scorekabaddi/', views.scorekabaddi, name='scorekabaddi'),
    path('scorecricket/', views.scorecricket, name='scorecricket'),
    path('scorebadminton/', views.scorebadminton, name='scorebadminton'),
    path('scorenetball/', views.scorenetball, name='scorenetball'),
    path('__debug__/', include(debug_toolbar.urls)),
]
