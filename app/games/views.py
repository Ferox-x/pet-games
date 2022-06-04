from django.shortcuts import render
from django.views import View


class SchulteGame(View):

    def get(self, request):
        return render(request, 'games/schulte.html', {})


class StroopGame(View):

    def get(self, request):
        return render(request, 'games/stroop.html', {})


class AllGames(View):

    def get(self, request):
        return render(request, 'games/allgames.html', {})


class LeaderboardsView(View):

    def get(self, request):
        return render(request, 'leaderboards/leaderboard.html', {})
