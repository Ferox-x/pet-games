from http import HTTPStatus
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from services.code_database import Leaderboards, Achievements


def is_ajax(request):
    return request.POST.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class SchulteGame(View):

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


class StroopGame(View):

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
            Achievements('stroop', request.user).save_achievement(achievement)

            return HttpResponse(HTTPStatus.OK)


class AllGames(View):

    def get(self, request):
        return render(request, 'games/allgames.html', {})


class LeaderboardsView(View):

    def get(self, request, game):
        leaderboards = Leaderboards(game).get_leaderboard()

        if leaderboards:
            paginator = Paginator(leaderboards, 25)
            page = request.GET.get('page') or 1
            leaderboards = paginator.get_page(page)
            pages = paginator.page_range

            context = {
                'leaderboards': leaderboards,
                'page': int(page),
                'pages': pages,
                'game': game
            }
            return render(request, 'games/leaderboards/leaderboards.html',
                          context)

        return HttpResponse(404)
