from http import HTTPStatus

from django.core.paginator import Paginator
from django.db.models import Subquery
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
        leaderboards = SchulteModel.objects.raw(
            """ WITH table1 AS (SELECT MIN("games_schulte"."record") as "record", "Users"."username"
                FROM games_schulte
                JOIN "Users"
                ON "games_schulte"."user_id" = "Users"."id"
                GROUP BY "Users"."username")
                SELECT 1 as id, record, username FROM table1
                ORDER BY "record"
            """
        )

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

    # def get(self, request, game):
    #     model = None
    #     order_by = list()
    #     distinct = ['user__username']
    #     if game:
    #         values = ['record', 'user__username']
    #         if game == 'schulte':
    #             model = SchulteModel
    #             order_by.append('record')
    #             distinct.append('record')
    #         elif game == 'stroop':
    #             model = StroopModel
    #             values.append('score')
    #             order_by.append('score')
    #             distinct.append('score')
    #
    #
    #         if model:
    #             leaderboards = model.objects.select_related(
    #                 'user'
    #             ).values(
    #                 'user__username', 'record'
    #             ).distinct(
    #                 'record', 'user__username',
    #             ).order_by(
    #                 'record'
    #             ).all()
    #
    #             paginator = Paginator(leaderboards, 25)
    #             page = request.GET.get('page') or 1
    #             leaderboards = paginator.get_page(page)
    #             pages = paginator.page_range
    #
    #             context = {
    #                 'leaderboards': leaderboards,
    #                 'page': int(page),
    #                 'pages': pages,
    #                 'game': game
    #             }
    #
    #             return render(request, 'games/leaderboards/leaderboards.html',
    #                           context)
    #
    #     return HttpResponse(status=404)
