from django.core.paginator import Paginator

from games.models import StroopModel, SchulteModel
from support.models import Chat, SupportTicket


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
            INNER JOIN "Users" ON user_id = "Users"."id"
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
            INNER JOIN "Users" ON user_id = "Users"."id"
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

    def __init__(self, game, user):
        self.game = game
        self.user = user

    def get_achievements(self) -> SchulteModel | StroopModel:
        """Менеджер получения результатов."""
        if self.game == 'schulte':
            return self._get_schulte_achievements()
        elif self.game == 'stroop':
            return self._get_stroop_achievements()

    def save_achievement(self, achievement) -> None:
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

    def _save_schulte_achievement(self, achievement) -> None:
        """Сохраняет результат в бд games_schulte."""
        time = achievement.split(':')
        time = int(time[0]) * 60 * 100 + int(time[1]) * 100 + int(time[2])
        SchulteModel(record=time, user=self.user).save()

    def _save_stroop_achievement(self, achievement) -> None:
        """Сохраняет результат в бд games_stroop."""
        StroopModel(record=achievement, user=self.user).save()


class Support:
    """Класс Support отвечает за формирование чатов службе поддержки."""

    def __init__(self, user, post):
        self.user = user
        self.post_data = post

    def get_chats(self) -> Chat:
        """Достает из базы данных все чаты со службой поддержки,
         для конкретного пользователя."""

        chats = Chat.objects.select_related(
            'ticket', 'user'
        ).values(
            'ticket__header', 'ticket__date', 'ticket__status', 'message',
            'date', 'user__username'
        ).filter(
            ticket__user_id=self.user.id
        ).all()
        return chats

    def create_ticket_or_add_message(self) -> None:
        """Вызывает метод _unpacking_post_data."""
        self._unpacking_post_data()

    def _unpacking_post_data(self) -> None:
        """Распаковывает данные из POST в атрибуты класса. И создает тикет,
        или добавляет к нему сообщение."""
        if self.post_data.get('create_ticket', False):
            self.header = self.post_data.get('header')
            self.chat_message = self.post_data.get('chat_message')
            self._create_ticket_in_db()
        elif self.post_data.get('chat', False):
            self.chat_message = self.post_data.get('chat_message')
            self.ticket_id = self.post_data.get('ticket_id')
            self._add_message_to_ticket()
        else:
            pass
            # логирование не не правильную POST DATA

    def _create_ticket_in_db(self) -> None:
        """Создает тикет."""
        self.ticket = SupportTicket.objects.create(
            user=self.user, header=self.header
        )

    def _add_message_to_ticket(self) -> None:
        """Добавляет сообщение к тикету."""
        self.last_message = Chat.objects.create(
            ticket_id=self.ticket.id, message=self.chat_message, user=self.user
        )
