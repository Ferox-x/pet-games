from json import dumps
from typing import Dict

from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import render
from django.utils.formats import localize

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
        minute, sec, milsec = map(int, achievement.split(':'))
        time = minute * 60 * 100 + sec * 100 + milsec
        SchulteModel(record=time, user=self.user).save()

    def _save_stroop_achievement(self, achievement) -> None:
        """Сохраняет результат в бд games_stroop."""
        StroopModel(record=achievement, user=self.user).save()


class BaseSupport:

    def __init__(self, user, post):
        self.chat_message = None
        self.ticket_id = None
        self.last_message = None
        self.user = user
        self.post_data = post

    def manager(self):
        """Метод-менеджер."""
        if self.post_data.get('get_chat_from_ticket'):
            return self._get_chat(self.post_data.get('ticket_id'))
        elif self.post_data.get('create_ticket', False):
            header = self.post_data.get('header')
            chat_message = self.post_data.get('chat_message')
            self._create_ticket_in_db(header, chat_message)
        elif self.post_data.get('add_message_to_chat', False):
            self.chat_message = self.post_data.get('chat_message')
            self.ticket_id = self.post_data.get('ticket_id')
            self._add_message_to_ticket()
            return self._convert_last_message_to_dict()
        else:
            pass

    def _convert_last_message_to_dict(self) -> Dict:
        """Преобразует последнее сообщение от пользователя в словарь."""
        date = localize(self.last_message.date)
        dict_last_message = {
            'username': self.user.username,
            'message': self.last_message.message,
            'date': date
        }
        return dict_last_message

    def _get_chat(self, chat_id):
        """Достает из базы данных выбранный чат со службой поддержки,
         для конкретного пользователя."""

        chat = Chat.objects.select_related(
            'user'
        ).values(
            'message', 'date', 'user__username', 'id'
        ).filter(
            ticket_id=chat_id
        ).order_by(
            'date'
        ).all()
        chat = list(chat)
        length = len(chat)
        for message in chat:
            message['date'] = localize(message['date'])
        json_dict = {key: value for key, value in enumerate(chat)}
        json_dict['len'] = length
        json_dict['ticket'] = self._get_ticket_on_id(chat_id)
        return json_dict

    @staticmethod
    def _get_ticket_on_id(ticket_id):
        ticket = SupportTicket.objects.filter(
            id=ticket_id
        ).values(
            'header', 'date', 'first_message', 'status'
        ).first()

        ticket['date'] = localize(ticket.get('date'))

        return ticket

    @staticmethod
    def _get_sorted_tickets(tickets):

        open_tickets = list()
        in_progress_tickets = list()
        closed_tickets = list()

        for ticket in tickets:
            if ticket.get('status') == 'OP':
                open_tickets.append(ticket)
            elif ticket.get('status') == 'IP':
                in_progress_tickets.append(ticket)
            elif ticket.get('status') == 'CL':
                closed_tickets.append(ticket)

        sorted_tickets = {
            'op': open_tickets,
            'ip': in_progress_tickets,
            'cl': closed_tickets,
        }

        return sorted_tickets

    def _add_message_to_ticket(self) -> None:
        """Добавляет сообщение к тикету."""
        self.last_message = Chat.objects.create(
            ticket_id=self.ticket_id, message=self.chat_message, user=self.user
        )

    def _create_ticket_in_db(self, header, chat_message):
        pass


class Support(BaseSupport):
    """Класс Support отвечает за формирование чатов службы поддержки
    (для пользователя)."""

    def __init__(self, user, post):
        super().__init__(user, post)

    def get_tickets(self):
        """Достает из БД все тикеты для конкретного пользователя."""
        tickets = SupportTicket.objects.select_related(
            'user'
        ).filter(
            user_id=self.user.id
        ).values(
            'header', 'date', 'status', 'first_message', 'id'
        ).all()

        return self._get_sorted_tickets(tickets)

    def _create_ticket_in_db(self, header, chat_message) -> None:
        """Создает тикет."""
        self.ticket = SupportTicket.objects.create(
            user=self.user, header=header, first_message=chat_message
        ).id


class SupportStaff(BaseSupport):

    def __init__(self, user, post):
        super().__init__(user, post)

    def get_tickets(self):
        """Достает из БД все тикеты."""
        tickets = SupportTicket.objects.select_related(
            'user'
        ).values(
            'header', 'date', 'status', 'first_message', 'id'
        ).all()

        return self._get_sorted_tickets(tickets)

    @staticmethod
    def change_status(ticket_id, status):
        ticket = SupportTicket.objects.get(id=ticket_id)
        ticket.status = status
        ticket.save(update_fields=['status'])


def render_support_page(request):
    support = Support(request.user, request.POST)
    tickets = support.get_tickets()
    context = {
        'tickets': tickets,
    }

    return render(request, 'support/support.html', context)
