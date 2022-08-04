from http import HTTPStatus
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
            records = list(reversed(SchulteModel.objects.values('record').filter(
                user_id=request.user.id)))[:20]
        return render(request, 'games/schulte/index.html',
                      {'records': records})

    def post(self, request):
        if request.user.is_authenticated and is_ajax(request):
            time = request.POST.get('time')
            SchulteModel(record=time, user=request.user).save()
            return HttpResponse(HTTPStatus.OK)


class StroopGame(View):

    def get(self, request):
        records = None
        if request.user.is_authenticated:
            records = list(reversed(StroopModel.objects.values('record').
                                    filter(user_id=request.user.id)))[:20]
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

    def get(self, request):
        return render(request, 'leaderboards/leaderboard.html', {})
