from http import HTTPStatus
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
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
            records = list(reversed(SchulteModel.objects.values('record').filter(
                    user_id=request.user.id)))[:20]
            json_records = dict()
            for index, record in enumerate(records):
                json_records[str(index)] = record.get('record')
            return JsonResponse(json_records, status=HTTPStatus.OK)


class StroopGame(View):

    def get(self, request):
        records = None
        if request.user.is_authenticated:
            records = StroopModel.objects.values('record').filter(
                user_id=request.user.id)
        template = 'games/stroop/index.html'
        context = {'records': records}
        return render(request, template, context)

    def post(self, request):
        if request.user.is_authenticated and is_ajax(request):
            record = request.POST.get('record')
            StroopModel(record=record, user=request.user).save()
            records = list(StroopModel.objects.values('record').filter(
                user_id=request.user.id))[:20]
            json_records = dict()
            for index, record in enumerate(records):
                json_records[str(index)] = record.get('record')
            return JsonResponse(json_records, status=HTTPStatus.OK)




class AllGames(View):

    def get(self, request):
        return render(request, 'games/allgames.html', {})


class LeaderboardsView(View):

    def get(self, request):
        return render(request, 'leaderboards/leaderboard.html', {})
