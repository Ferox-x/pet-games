
from django.core.paginator import Paginator

from games.models import StroopModel, SchulteModel
from users.models import Users


class Leaderboards:
    """Класс Leaderboards отвечает за формирование таблицы лидеров."""

    def __init__(self, game):
        self.game = game

    @staticmethod
    def _get_stroop_leaderboard() -> StroopModel:
        """Совершает запрос в базу данных в таблицу games_stroop, и получает рейтинг 100
         лучших результатов."""
        stroop_leaderboard = StroopModel.objects.raw(
            """
            WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_stroop.id, score,record, date, username FROM games_stroop
            INNER JOIN "users" ON user_id = "users"."id"
            ORDER BY user_id, score DESC)
            SELECT id, score, record, date, username FROM table1
            ORDER BY score DESC
            LIMIT 100
            """
        )
        return stroop_leaderboard

    @staticmethod
    def _get_schulte_leaderboard() -> SchulteModel:
        """Совершает запрос в базу данных в таблицу games_schulte, и получает рейтинг 100
        лучших результатов."""
        schulte_leaderboard = SchulteModel.objects.raw(
            """
            WITH table1 AS (SELECT DISTINCT ON (user_id) user_id, games_schulte.id, record, date, username FROM games_schulte
            INNER JOIN "users" ON user_id = "users"."id"
            ORDER BY user_id, record)
            SELECT id, record, date, username FROM table1
            ORDER BY record
            LIMIT 100
            """
        )
        return schulte_leaderboard

    def get_leaderboard(self) -> SchulteModel | StroopModel | bool:
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


class Achievements:
    """Класс Achievements отвечает за сохранение и извлечение
    результатов пользователя из бд."""

    def __init__(self, game: str, user: Users):
        self.game = game
        self.user = user

    def get_achievements(self) -> SchulteModel | StroopModel:
        """Менеджер получения результатов."""
        if self.game == 'schulte':
            return self._get_schulte_achievements()
        elif self.game == 'stroop':
            return self._get_stroop_achievements()

    def save_achievement(self, achievement: str) -> None:
        """Менеджер сохранения результатов."""
        if self.game == 'schulte':
            return self._save_schulte_achievement(achievement)
        elif self.game == 'stroop':
            return self._save_stroop_achievement(achievement)

    def _get_schulte_achievements(self) -> SchulteModel:
        """Получает результаты пользователя в игре Schulte."""
        records = SchulteModel.objects.order_by('date').values(
            'record').filter(
            user_id=self.user.id).reverse().all()
        return records

    def _get_stroop_achievements(self) -> StroopModel:
        """Получает результаты пользователя в игре Stroop."""
        records = StroopModel.objects.order_by('date').values('record').filter(
            user_id=self.user.id).all().reverse()
        return records

    def _save_schulte_achievement(self, achievement: str) -> None:
        """Сохраняет результат в бд games_schulte."""
        minute, sec, milsec = map(int, achievement.split(':'))
        time = minute * 60 * 100 + sec * 100 + milsec
        SchulteModel(record=time, user=self.user).save()

    def _save_stroop_achievement(self, achievement: str) -> None:
        """Сохраняет результат в бд games_stroop."""
        StroopModel(record=achievement, user=self.user).save()
