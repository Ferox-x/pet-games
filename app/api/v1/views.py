from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from api.v1.serializers import SchulteSerializer, StroopSerializer
from games.models import SchulteModel, StroopModel


class SchulteApiView(ListModelMixin, GenericAPIView):

    queryset = SchulteModel.objects.raw(
            """
            WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_schulte.id, record, date, username FROM games_schulte
            INNER JOIN "Users" ON user_id = "Users"."id"
            ORDER BY user_id, record)
            SELECT id, record, date, username FROM table1
            ORDER BY record
            LIMIT 100
            """
        )
    serializer_class = SchulteSerializer

    def get(self, request):
        return self.list(request)


class StroopApiView(ListModelMixin, GenericAPIView):
    queryset = StroopModel.objects.raw(
        """
        WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_stroop.id, score,record, date, username FROM games_stroop
        INNER JOIN "Users" ON user_id = "Users"."id"
        ORDER BY user_id, score DESC)
        SELECT id, score, record, date, username FROM table1
        ORDER BY score DESC
        LIMIT 100
        """
    )
    serializer_class = StroopSerializer

    def get(self, request):
        return self.list(request)

