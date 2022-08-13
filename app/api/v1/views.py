from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.v1.serializers import SchulteSerializer, StroopSerializer
from services.code_database import Leaderboards


class SchulteApiView(ListModelMixin, GenericAPIView):
    """Класс отображения API Schulte."""
    queryset = Leaderboards('schulte').get_leaderboard()
    serializer_class = SchulteSerializer

    def get(self, request):
        return self.list(request)


class StroopApiView(ListModelMixin, GenericAPIView):
    """Класс отображения API Stroop."""
    queryset = Leaderboards('stroop').get_leaderboard()
    serializer_class = StroopSerializer

    def get(self, request):
        return self.list(request)

