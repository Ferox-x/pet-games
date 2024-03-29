import logging

from django.core.paginator import Paginator
from django.db.models.query import RawQuerySet, QuerySet

from games.models import SchulteModel, StroopModel
from users.models import Users

logger = logging.getLogger('main')


class Leaderboards:
    """Класс Leaderboards отвечает за формирование таблицы лидеров."""

    def __init__(self, game):
        self.game = game

    def get_leaderboard(self) -> RawQuerySet | bool:
        """Возвращает таблицу лидеров."""
        if self.game == 'schulte':
            leaderboard = self._get_schulte_leaderboard()
        elif self.game == 'stroop':
            leaderboard = self._get_stroop_leaderboard()
        else:
            return False
        return leaderboard

    def get_leaderboard_with_paginator(self) -> Paginator | bool:
        """Возвращает таблицу лидеров с пагинатором."""
        leaderboard = self.get_leaderboard()
        if leaderboard:
            paginator = Paginator(leaderboard, 25)
            return paginator
        return False

    @staticmethod
    def _get_stroop_leaderboard() -> RawQuerySet:
        """Совершает запрос в базу данных в таблицу games_stroop, и получает рейтинг 100
         лучших результатов."""
        stroop_leaderboard = StroopModel.objects.raw(
            """
            WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_stroop.id, score,record, date, username, country FROM games_stroop
            INNER JOIN "users" ON user_id = "users"."id"
            ORDER BY user_id, score DESC)
            SELECT id, score, record, date, username, country FROM table1
            ORDER BY score DESC
            LIMIT 100
            """
        )

        return stroop_leaderboard

    @staticmethod
    def _get_schulte_leaderboard() -> RawQuerySet:
        """Совершает запрос в базу данных в таблицу games_schulte, и получает рейтинг 100
        лучших результатов."""
        schulte_leaderboard = SchulteModel.objects.raw(
            """
            WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_schulte.id, record, date, username, country FROM games_schulte
            INNER JOIN "users" ON user_id = "users"."id"
            ORDER BY user_id, record)
            SELECT id, record, date, username, country FROM table1
            ORDER BY record
            LIMIT 100
            """
        )
        return schulte_leaderboard


class Achievements:
    """Класс Achievements отвечает за сохранение и извлечение
    результатов пользователя из бд."""

    def __init__(self, game: str, user: Users):
        self.game = game
        self.user = user

    def get_achievements(self) -> QuerySet:
        """Менеджер получения результатов."""
        if self.game == 'schulte':
            return self._get_schulte_achievements()
        elif self.game == 'stroop':
            return self._get_stroop_achievements()

    def save_achievement(self, achievement: str, score: int = None) -> None:
        """Менеджер сохранения результатов."""
        if self.game == 'schulte':
            return self._save_schulte_achievement(achievement)
        elif self.game == 'stroop':
            return self._save_stroop_achievement(achievement, score)

    def _get_schulte_achievements(self) -> QuerySet:
        """Получает результаты пользователя в игре Schulte."""
        records = SchulteModel.objects.order_by('date').values(
            'record').filter(
            user_id=self.user.id).reverse().all()
        return records

    def _get_stroop_achievements(self) -> QuerySet:
        """Получает результаты пользователя в игре Stroop."""
        records = StroopModel.objects.order_by('date').values('record', 'score').filter(
            user_id=self.user.id).all().reverse()
        return records

    def _save_schulte_achievement(self, achievement: str) -> None:
        """Сохраняет результат в бд games_schulte."""
        minute, sec, milsec = map(int, achievement.split(':'))
        time = minute * 60 * 100 + sec * 100 + milsec
        SchulteModel(record=time, user=self.user).save()

    def _save_stroop_achievement(self, achievement: str, score: int) -> None:
        """Сохраняет результат в бд games_stroop."""
        StroopModel(record=achievement, score=score, user=self.user).save()
