from django.urls import path

from games.views import SchulteGame, StroopGame, AllGames, LeaderboardsView


urlpatterns = [
    path('schulte/', SchulteGame.as_view(), name='schulte'),
    path('stroop/', StroopGame.as_view(), name='stroop'),
    path('allgames/', AllGames.as_view(), name='allgames'),
    path('leaderboards/<str:game>/', LeaderboardsView.as_view(),
         name='leaderboards'
         )
]
