from http import HTTPStatus
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from games.models import SchulteModel, StroopModel


def is_ajax(request):
    return request.POST.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class SchulteGame(View):

    def get(self, request):
        records = None

        if request.user.is_authenticated:
            records = list(
                reversed(SchulteModel.objects.values('record').filter(
                    user_id=request.user.id)))[:20]

        context = {'records': records}

        return render(request, 'games/schulte/index.html', context)

    def post(self, request):

        if request.user.is_authenticated and is_ajax(request):
            time = request.POST.get('time').split(':')
            time = int(time[0]) * 60 * 100 + int(time[1]) * 100 + int(time[2])
            SchulteModel(record=time, user=request.user).save()

            return HttpResponse(HTTPStatus.OK)


class StroopGame(View):

    def get(self, request):
        records = None

        if request.user.is_authenticated:
            records = list(reversed(
                StroopModel.objects.values('record').filter(
                    user_id=request.user.id)))[:20]

        template = 'games/stroop/index.html'
        context = {'records': records}

        return render(request, template, context)

    def post(self, request):

        if request.user.is_authenticated and is_ajax(request):
            record = request.POST.get('record')
            StroopModel(record=record, user=request.user).save()

            return HttpResponse(HTTPStatus.OK)


class AllGames(View):

    def get(self, request):
        return render(request, 'games/allgames.html', {})


class LeaderboardsView(View):

    def get(self, request, game):

        leaderboards = False

        if game == 'schulte':

            leaderboards = SchulteModel.objects.raw(
                """
                WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_schulte.id, record, date, username FROM games_schulte
                INNER JOIN "Users" ON user_id = "Users"."id"
                ORDER BY user_id, record)
                SELECT id, record, date, username FROM table1
                ORDER BY record
                LIMIT 100
                """
            )

        elif game == 'stroop':
            leaderboards = StroopModel.objects.raw(
                """
                WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_stroop.id, score,record, date, username FROM games_stroop
                INNER JOIN "Users" ON user_id = "Users"."id"
                ORDER BY user_id, score DESC)
                SELECT id, score, record, date, username FROM table1
                ORDER BY score DESC
                LIMIT 100
                """
            )

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
            return render(request, 'games/leaderboards/leaderboards.html', context)

        return HttpResponse(404)
