from rest_framework import generics


from api.v1.serializers import SchulteSerializer, StroopSerializer
from games.models import SchulteModel, StroopModel


class SchulteApiView(generics.ListCreateAPIView):

    queryset = SchulteModel.objects.raw(
            """ WITH table1 AS (SELECT MIN("games_schulte"."record") as "record", "Users"."username"
                FROM "games_schulte"
                JOIN "Users"
                ON "games_schulte"."user_id" = "Users"."id"
                GROUP BY "Users"."username")
                SELECT 1 as id, record, username FROM table1
                ORDER BY "record"
            """
        )
    serializer_class = SchulteSerializer


class StroopApiView(generics.ListCreateAPIView):

    queryset = StroopModel.objects.raw(
            """ WITH table1 AS (SELECT MIN("games_stroop"."score") as "score", "Users"."username", "games_stroop"."record"
                FROM "games_stroop"
                JOIN "Users" ON "games_stroop"."user_id" = "Users"."id"
                GROUP BY "Users"."username", "games_stroop"."record")
                SELECT 1 as id, score, record, username FROM table1
                ORDER BY "score" DESC
            """
        )
    serializer_class = StroopSerializer

