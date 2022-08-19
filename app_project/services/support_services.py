from django.db.models import QuerySet
from django.utils.formats import localize

from support.models import Chat, SupportTicket
from users.models import Users


class BaseSupport:
    """Базовый класс поддержки."""

    def __init__(self, user: Users, post: dict):
        self.chat_message = None
        self.ticket_id = None
        self.last_message = None
        self.user = user
        self.post_data = post

    def _convert_last_message_to_dict(self) -> dict:
        """Преобразует последнее сообщение от пользователя в словарь."""

        date = localize(self.last_message.date)
        dict_last_message = {
            'username': self.user.username,
            'message': self.last_message.message,
            'date': date
        }
        return dict_last_message

    def _get_chat(self, chat_id: int) -> dict:
        """Достает из базы данных выбранный чат со службой поддержки,
         для конкретного пользователя."""

        chat = Chat.objects.select_related(
            'user'
        ).values(
            'message', 'date', 'user__username', 'id', 'user__image'
        ).filter(
            ticket_id=chat_id
        ).order_by(
            'date'
        ).all()

        chat = self._chat_to_dict(chat, chat_id)
        return chat

    def _chat_to_dict(self, chat: QuerySet, chat_id: int) -> dict:
        """Преобразовывает Chat в словарь."""

        chat = list(chat)
        length = len(chat)
        for message in chat:
            message['date'] = localize(message['date'])
        json_chat = {key: value for key, value in enumerate(chat)}
        json_chat['len'] = length
        json_chat['ticket'] = self._get_ticket_on_id(chat_id)
        return json_chat

    @staticmethod
    def _get_ticket_on_id(ticket_id: int) -> SupportTicket:
        """Достает тикет из базы данных по id."""
        ticket = SupportTicket.objects.select_related(
            'user'
        ).filter(
            id=ticket_id
        ).values(
            'header', 'date', 'first_message', 'status', 'user__image'
        ).first()

        ticket['date'] = localize(ticket.get('date'))

        return ticket

    @staticmethod
    def _get_sorted_tickets(tickets: QuerySet) -> dict[str, list[dict]]:
        """Сортирует тикеты по статусу."""
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


class Support(BaseSupport):
    """Класс Support отвечает за формирование чатов службы поддержки
    (для пользователя)."""

    def __init__(self, user: Users, post: dict):
        super().__init__(user, post)

    def manager(self) -> dict | None:
        """Метод-менеджер."""
        if self.post_data.get('get_chat_from_ticket'):
            return self._get_chat(self.post_data.get('ticket_id'))
        elif self.post_data.get('create_ticket'):
            header = self.post_data.get('header')
            chat_message = self.post_data.get('chat_message')
            self._create_ticket_in_db(header, chat_message)
        elif self.post_data.get('add_message_to_chat'):
            self.chat_message = self.post_data.get('chat_message')
            self.ticket_id = self.post_data.get('ticket_id')
            self._add_message_to_ticket()
            return self._convert_last_message_to_dict()

    def get_tickets(self) -> dict[str, list[SupportTicket]]:
        """Достает из БД все тикеты для конкретного пользователя."""
        tickets = SupportTicket.objects.select_related(
            'user'
        ).filter(
            user_id=self.user.id
        ).values(
            'header', 'date', 'status', 'first_message', 'id'
        ).all()

        return self._get_sorted_tickets(tickets)

    def _create_ticket_in_db(self, header: str, chat_message: str) -> None:
        """Создает тикет."""
        self.ticket = SupportTicket.objects.create(
            user=self.user, header=header, first_message=chat_message
        ).id


class SupportStaff(BaseSupport):

    def __init__(self, user: Users, post: dict):
        super().__init__(user, post)

    def manager(self) -> dict:
        """Метод-менеджер. Возвращает Json"""
        if self.post_data.get('change_status'):
            ticket_id = self.post_data.get('ticket_id')
            status = self.post_data.get('status')
            return self._change_status(ticket_id, status)
        if self.post_data.get('get_chat_from_ticket'):
            return self._get_chat(self.post_data.get('ticket_id'))
        elif self.post_data.get('add_message_to_chat'):
            self.chat_message = self.post_data.get('chat_message')
            self.ticket_id = self.post_data.get('ticket_id')
            self._add_message_to_ticket()
            return self._convert_last_message_to_dict()

    def get_tickets(self) -> dict[str, list[SupportTicket]]:
        """Достает из БД все тикеты."""
        tickets = SupportTicket.objects.select_related(
            'user'
        ).values(
            'header', 'date', 'status', 'first_message', 'id'
        ).all()

        return self._get_sorted_tickets(tickets)

    @staticmethod
    def _change_status(ticket_id: int, status: str) -> dict:
        """Меняет статус тикета."""
        ticket = SupportTicket.objects.get(id=ticket_id)
        ticket.status = status
        ticket.save(update_fields=['status'])
        return {}
