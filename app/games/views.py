from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from games.models import SchulteModel


def is_ajax(request):
    return request.POST.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class SchulteGame(View):

    def get(self, request):
        records = list(reversed(SchulteModel.objects.values('record').filter(
            user_id=request.user.id)))[:20]
        return render(request, 'games/schulte/index.html',
                      {'records': records})

    def post(self, request):
        if is_ajax(request):
            time = request.POST.get('time')
            SchulteModel(record=time, user=request.user).save()
            records = list(reversed(SchulteModel.objects.values('record').filter(
                    user_id=request.user.id)))[:20]
            json_records = dict()
            for index, record in enumerate(records):
                json_records[str(index)] = record.get('record')
            return JsonResponse(json_records, status=200)


class StroopGame(View):

    def get(self, request):
        template = 'games/stroop/index.html'
        context = {}
        return render(request, template, context)


class AllGames(View):

    def get(self, request):
        return render(request, 'games/allgames.html', {})


class LeaderboardsView(View):

    def get(self, request):
        return render(request, 'leaderboards/leaderboard.html', {})
