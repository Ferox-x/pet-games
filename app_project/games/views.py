from http import HTTPStatus
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from services.games_services import Leaderboards, Achievements
from services.generic_services import is_ajax


class SchulteGame(View):
    """Представление отображающее SchulteGame."""
    def get(self, request):
        records = None

        if request.user.is_authenticated:
            records = Achievements('schulte', request.user).get_achievements()

        context = {
            'records': records
        }

        return render(request, 'games/schulte/index.html', context)

    def post(self, request):

        if request.user.is_authenticated and is_ajax(request):
            achievement = request.POST.get('time')
            Achievements('schulte', request.user).save_achievement(achievement)

            return HttpResponse(HTTPStatus.OK)
        elif not request.user.is_authenticated:
            return HttpResponse(HTTPStatus.OK)


class StroopGame(View):
    """Представление отображающее StroopGame."""
    def get(self, request):
        records = None

        if request.user.is_authenticated:

            records = Achievements('stroop', request.user).get_achievements()

        template = 'games/stroop/index.html'
        context = {
            'records': records
        }

        return render(request, template, context)

    def post(self, request):

        if request.user.is_authenticated and is_ajax(request):
            achievement = request.POST.get('record')
            score = request.POST.get('score')
            Achievements('stroop', request.user).save_achievement(achievement, score)

            return HttpResponse(HTTPStatus.OK)
        elif not request.user.is_authenticated:
            return HttpResponse(HTTPStatus.OK)


class AllGames(View):
    """Представление отображающее AllGames."""
    def get(self, request):
        return render(request, 'games/allgames.html', {})


class LeaderboardsView(View):
    """Представление отображающее Leaderboard по конкретной игре,
    у которой есть рейтинговая система."""
    def get(self, request, game):
        page = request.GET.get('page') or 1
        leaderboard = Leaderboards(game).get_leaderboard_with_paginator()

        if leaderboard:
            context = {
                'leaderboards': leaderboard.get_page(page),
                'page': int(page),
                'pages': leaderboard.page_range,
                'game': game
            }
            return render(request, 'games/leaderboards/leaderboards.html',
                          context)

        return render(request, 'core/error_page/404.html')
