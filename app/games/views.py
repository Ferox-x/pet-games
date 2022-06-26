from django.shortcuts import render, redirect
from django.views import View

from games.models import SchulteModel


class SchulteGame(View):

    def get(self, request):
        records = reversed(SchulteModel.objects.filter(user_id=request.user.id))
        return render(request, 'games/schulte/index.html', {'records': records})

    def post(self, request):
        time = int(request.POST.get('time'))

        dec_sec = time % 100
        seconds = time // 100 % 60
        minutes = time // 6000

        dec_sec = dec_sec if dec_sec > 10 else '0' + str(dec_sec)
        seconds = seconds if seconds > 10 else '0' + str(seconds)
        minutes = minutes if minutes > 10 else '0' + str(minutes)

        time = '{}:{}:{}'.format(minutes, seconds, dec_sec)
        SchulteModel(record=time, user=request.user).save()


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
